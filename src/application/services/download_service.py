import asyncio
import uuid
from pathlib import Path
from typing import Dict, Optional
from src.domain import (
    DownloadTask, Track, TrackInfo, TrackRepository,
    DownloadStartedEvent, DownloadProgressEvent, DownloadCompletedEvent, DownloadFailedEvent,
    DownloadPausedEvent, DownloadResumedEvent, DownloadCancelledEvent,
    DownloadCommand, PauseDownloadCommand, ResumeDownloadCommand, CancelDownloadCommand,
    AddTrackToLibraryCommand, DownloadError
)
from src.application.event_bus import event_bus
from src.shared.utils import sanitize_filename


class DownloadService:
    """Service for managing music downloads."""

    def __init__(self, track_repository: TrackRepository, download_manager):
        self.track_repository = track_repository
        self.download_manager = download_manager
        self.active_tasks: Dict[str, DownloadTask] = {}

        # Subscribe to download commands
        event_bus.subscribe('DownloadCommand', self._handle_download_command)
        event_bus.subscribe('PauseDownloadCommand', self._handle_pause_command)
        event_bus.subscribe('ResumeDownloadCommand', self._handle_resume_command)
        event_bus.subscribe('CancelDownloadCommand', self._handle_cancel_command)

    def _handle_download_command(self, command: DownloadCommand):
        """Handle download command."""
        asyncio.create_task(self._start_download(command.track_info, command.output_path))

    async def _start_download(self, track_info: TrackInfo, output_path: str):
        """Start a download task."""
        task_id = str(uuid.uuid4())

        # Compute full file path
        output_dir = Path(output_path)
        filename = sanitize_filename(track_info.title) + ".mp3"
        full_path = output_dir / filename

        task = DownloadTask(
            id=task_id,
            track_info=track_info,
            output_path=str(full_path),
            status='pending'
        )
        self.active_tasks[task_id] = task

        # Publish started event
        event_bus.publish(DownloadStartedEvent(task=task))

        try:
            # Start download with progress callback
            await self.download_manager.add_download(
                track_info=track_info,
                output_filepath=full_path,
                callback=self._download_progress_callback(task_id)
            )
        except Exception as e:
            task.status = 'failed'
            task.error_message = str(e)
            event_bus.publish(DownloadFailedEvent(task_id=task_id, error=str(e)))
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]

    def _download_progress_callback(self, task_id: str):
        """Create progress callback for download manager."""
        def callback(progress: float, speed_bps: int, eta_seconds: int):
            if task_id in self.active_tasks:
                task = self.active_tasks[task_id]
                task.progress = progress
                task.speed_bps = speed_bps
                task.eta_seconds = eta_seconds
                event_bus.publish(DownloadProgressEvent(
                    task_id=task_id,
                    progress=progress,
                    speed_bps=speed_bps,
                    eta_seconds=eta_seconds
                ))

                # Handle completion
                if progress >= 1.0:
                    # Download completed
                    task.status = 'completed'
                    # Create Track entity (full path from task.output_path)
                    track = Track(
                        title=task.track_info.title,
                        artist=task.track_info.artist,
                        album=task.track_info.album,
                        duration=task.track_info.duration,
                        file_path=task.output_path,
                        source=task.track_info.source,
                        license=task.track_info.license,
                        genre=task.track_info.genre,
                        year=task.track_info.year,
                        cover_path=None
                    )
                    event_bus.publish(AddTrackToLibraryCommand(track=track))
                    event_bus.publish(DownloadCompletedEvent(task_id=task_id, track=track))
                    del self.active_tasks[task_id]
                elif progress == 0.0:
                    # Download failed
                    task.status = 'failed'
                    task.error_message = task.error_message or "Download failed"
                    event_bus.publish(DownloadFailedEvent(task_id=task_id, error=task.error_message))
                    del self.active_tasks[task_id]
        return callback

    def _handle_pause_command(self, command: PauseDownloadCommand):
        """Handle pause download command."""
        if command.task_id in self.active_tasks:
            self.download_manager.pause_download(command.task_id)
            self.active_tasks[command.task_id].status = 'paused'
            event_bus.publish(DownloadPausedEvent(task_id=command.task_id))

    def _handle_resume_command(self, command: ResumeDownloadCommand):
        """Handle resume download command."""
        if command.task_id in self.active_tasks:
            self.download_manager.resume_download(command.task_id)
            self.active_tasks[command.task_id].status = 'downloading'
            event_bus.publish(DownloadResumedEvent(task_id=command.task_id))

    def _handle_cancel_command(self, command: CancelDownloadCommand):
        """Handle cancel download command."""
        if command.task_id in self.active_tasks:
            self.download_manager.cancel_download(command.task_id)
            self.active_tasks[command.task_id].status = 'cancelled'
            event_bus.publish(DownloadCancelledEvent(task_id=command.task_id))
            del self.active_tasks[command.task_id]

    def get_active_downloads(self) -> Dict[str, DownloadTask]:
        """Get all active download tasks."""
        return self.active_tasks.copy()