"""Asynchronous download manager with queue, progress tracking, and retry logic"""

import asyncio
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable, Dict, Optional, Any
from datetime import datetime

from aiohttp import ClientSession, ClientTimeout

from src.shared import ensure_dir, sanitize_filename
from src.domain.constants import DOWNLOAD_CHUNK_SIZE, DOWNLOAD_TIMEOUT, MAX_RETRIES, RETRY_DELAY
from src.domain import TrackInfo


class DownloadStatus(Enum):
    """Status of a download task."""
    QUEUED = "queued"
    DOWNLOADING = "downloading"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class DownloadTask:
    """Represents a single download task."""
    task_id: str
    track_info: TrackInfo
    output_path: Path
    filename: str
    total_size: int = 0
    downloaded: int = 0
    status: DownloadStatus = DownloadStatus.QUEUED
    error: Optional[str] = None
    retry_count: int = 0
    progress_callback: Optional[Callable] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @property
    def progress_percent(self) -> float:
        if self.total_size <= 0:
            return 0.0
        return (self.downloaded / self.total_size) * 100

    @property
    def is_active(self) -> bool:
        return self.status in [DownloadStatus.QUEUED, DownloadStatus.DOWNLOADING, DownloadStatus.PAUSED]


class DownloadManager:
    """Manages asynchronous downloads with queue and concurrency control."""

    def __init__(self, max_concurrent: int = 3) -> None:
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.queue: asyncio.Queue[DownloadTask] = asyncio.Queue()
        self.active_tasks: Dict[str, DownloadTask] = {}
        self._worker_task: Optional[asyncio.Task] = None
        self._session: Optional[ClientSession] = None
        self._running = False
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    async def start(self) -> None:
        """Start the download worker."""
        if self._running:
            return
        self._running = True
        self._loop = asyncio.get_running_loop()
        self._session = ClientSession(
            timeout=ClientTimeout(total=DOWNLOAD_TIMEOUT),
            headers={"User-Agent": "Forsong/0.1.0"},
        )
        self._worker_task = asyncio.create_task(self._worker())

    async def stop(self) -> None:
        """Stop the download worker gracefully."""
        self._running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
        if self._session:
            await self._session.close()
            self._session = None

    async def add_download(
        self,
        track_info: TrackInfo,
        output_filepath: Path | str,
        callback: Optional[Callable] = None,
    ) -> str:
        """Add a new download to the queue (async)."""
        task_id = str(uuid.uuid4())
        output_filepath = Path(output_filepath)
        output_dir = output_filepath.parent
        filename = output_filepath.name
        ensure_dir(output_dir)

        task = DownloadTask(
            task_id=task_id,
            track_info=track_info,
            output_path=output_dir,
            filename=filename,
            progress_callback=callback,
            start_time=datetime.now(),
            metadata={
                'title': track_info.title,
                'artist': track_info.artist,
                'album': track_info.album,
                'license': track_info.license,
                'genre': track_info.genre,
                'year': track_info.year,
                'source': track_info.source,
                'cover_url': track_info.cover_url,
            }
        )
        self.active_tasks[task_id] = task
        await self.queue.put(task)
        return task_id

    def cancel_download(self, task_id: str) -> bool:
        """Cancel a download task."""
        task = self.active_tasks.get(task_id)
        if task and task.status in [DownloadStatus.QUEUED, DownloadStatus.DOWNLOADING]:
            task.status = DownloadStatus.CANCELLED
            return True
        return False

    def pause_download(self, task_id: str) -> bool:
        """Pause a download."""
        task = self.active_tasks.get(task_id)
        if task and task.status == DownloadStatus.DOWNLOADING:
            task.status = DownloadStatus.PAUSED
            return True
        return False

    def resume_download(self, task_id: str) -> bool:
        """Resume a paused download."""
        task = self.active_tasks.get(task_id)
        if task and task.status == DownloadStatus.PAUSED:
            task.status = DownloadStatus.QUEUED
            asyncio.create_task(self.queue.put(task))
            return True
        return False

    def get_task(self, task_id: str) -> Optional[DownloadTask]:
        """Get task by ID."""
        return self.active_tasks.get(task_id)

    def get_all_tasks(self) -> Dict[str, DownloadTask]:
        """Get all active tasks."""
        return self.active_tasks.copy()

    async def _worker(self) -> None:
        """Main worker loop processing download queue."""
        while self._running:
            try:
                task = await self.queue.get()
                if not self._running:
                    break
                if task.status == DownloadStatus.CANCELLED:
                    self.queue.task_done()
                    continue
                async with self.semaphore:
                    await self._process_task(task)
                self.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception:
                pass

    async def _process_task(self, task: DownloadTask) -> None:
        """Process a single download task."""
        filepath = task.output_path / task.filename
        existing_size = filepath.stat().st_size if filepath.exists() else 0

        for attempt in range(MAX_RETRIES):
            try:
                task.status = DownloadStatus.DOWNLOADING
                task.retry_count = attempt

                headers = {}
                if existing_size > 0:
                    headers["Range"] = f"bytes={existing_size}-"

                async with self._session.get(task.track_info.download_url, headers=headers) as response:
                    response.raise_for_status()
                    total_size = int(response.headers.get("Content-Length", 0))
                    task.total_size = total_size + existing_size if existing_size else total_size

                    mode = "ab" if existing_size > 0 else "wb"
                    with open(filepath, mode) as f:
                        async for chunk in response.content.iter_chunked(DOWNLOAD_CHUNK_SIZE):
                            if task.status == DownloadStatus.PAUSED:
                                await asyncio.sleep(0.1)
                                continue
                            if task.status == DownloadStatus.CANCELLED:
                                if filepath.exists():
                                    filepath.unlink()
                                return
                            f.write(chunk)
                            task.downloaded += len(chunk)
                            # Calculate progress and speed
                            if task.total_size > 0:
                                task.progress = task.downloaded / task.total_size
                                elapsed = (datetime.now() - task.start_time).total_seconds() if task.start_time else 0
                                if elapsed > 0:
                                    task.speed_bps = int(task.downloaded / elapsed)
                                if task.speed_bps > 0:
                                    remaining = task.total_size - task.downloaded
                                    task.eta_seconds = int(remaining / task.speed_bps)
                            else:
                                task.progress = 0.0
                                task.speed_bps = 0
                                task.eta_seconds = 0
                            if task.progress_callback:
                                task.progress_callback(task.progress, task.speed_bps, task.eta_seconds)

                task.status = DownloadStatus.COMPLETED
                task.progress = 1.0
                task.end_time = datetime.now()
                if task.progress_callback:
                    task.progress_callback(1.0, task.speed_bps, 0)
                return

            except Exception as e:
                task.error = str(e)
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                else:
                    task.status = DownloadStatus.FAILED
                    task.end_time = datetime.now()
                    if task.progress_callback:
                        task.progress_callback(0.0, 0, 0)
                    return
