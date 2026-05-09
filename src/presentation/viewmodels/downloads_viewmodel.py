from typing import Dict, List
from src.domain import (
    DownloadTask, DownloadStartedEvent, DownloadProgressEvent,
    DownloadCompletedEvent, DownloadFailedEvent, DownloadCancelledEvent,
    PauseDownloadCommand, ResumeDownloadCommand, CancelDownloadCommand
)
from src.presentation.di_container import container


class DownloadsViewModel:
    """ViewModel for downloads functionality."""

    def __init__(self):
        self.event_bus = container.event_bus

        # State
        self.active_downloads: Dict[str, DownloadTask] = {}

        # Callbacks for UI updates
        self.on_downloads_changed = None

        # Subscribe to download events
        self.event_bus.subscribe('DownloadStartedEvent', self._on_download_started)
        self.event_bus.subscribe('DownloadProgressEvent', self._on_download_progress)
        self.event_bus.subscribe('DownloadCompletedEvent', self._on_download_completed)
        self.event_bus.subscribe('DownloadFailedEvent', self._on_download_failed)
        self.event_bus.subscribe('DownloadPausedEvent', self._on_download_paused)
        self.event_bus.subscribe('DownloadResumedEvent', self._on_download_resumed)
        self.event_bus.subscribe('DownloadCancelledEvent', self._on_download_cancelled)

    def get_active_downloads(self) -> List[DownloadTask]:
        """Get list of active downloads for UI."""
        return list(self.active_downloads.values())

    def pause_download(self, task_id: str):
        """Pause a download."""
        pause_cmd = PauseDownloadCommand(task_id=task_id)
        self.event_bus.publish(pause_cmd)

    def resume_download(self, task_id: str):
        """Resume a download."""
        resume_cmd = ResumeDownloadCommand(task_id=task_id)
        self.event_bus.publish(resume_cmd)

    def cancel_download(self, task_id: str):
        """Cancel a download."""
        cancel_cmd = CancelDownloadCommand(task_id=task_id)
        self.event_bus.publish(cancel_cmd)

    def has_active_downloads(self) -> bool:
        """Check if there are active downloads."""
        return len(self.active_downloads) > 0

    def _on_download_started(self, event: DownloadStartedEvent):
        """Handle download started event."""
        self.active_downloads[event.task.id] = event.task
        self._notify_ui()

    def _on_download_progress(self, event: DownloadProgressEvent):
        """Handle download progress event."""
        if event.task_id in self.active_downloads:
            task = self.active_downloads[event.task_id]
            task.progress = event.progress
            task.speed_bps = event.speed_bps
            task.eta_seconds = event.eta_seconds
            self._notify_ui()

    def _on_download_completed(self, event: DownloadCompletedEvent):
        """Handle download completed event."""
        if event.task_id in self.active_downloads:
            del self.active_downloads[event.task_id]
            self._notify_ui()

    def _on_download_failed(self, event: DownloadFailedEvent):
        """Handle download failed event."""
        if event.task_id in self.active_downloads:
            del self.active_downloads[event.task_id]
            self._notify_ui()

    def _on_download_paused(self, event):
        """Handle download paused event."""
        if event.task_id in self.active_downloads:
            self.active_downloads[event.task_id].status = 'paused'
            self._notify_ui()

    def _on_download_resumed(self, event):
        """Handle download resumed event."""
        if event.task_id in self.active_downloads:
            self.active_downloads[event.task_id].status = 'downloading'
            self._notify_ui()

    def _on_download_cancelled(self, event):
        """Handle download cancelled event."""
        if event.task_id in self.active_downloads:
            del self.active_downloads[event.task_id]
            self._notify_ui()

    def _notify_ui(self):
        """Notify UI about changes."""
        if self.on_downloads_changed:
            self.on_downloads_changed()