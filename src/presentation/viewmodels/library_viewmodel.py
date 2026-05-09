"""ViewModel for library functionality following MVVM pattern."""

from typing import List, Optional
from src.domain import Track
from src.presentation.di_container import container
from src.domain.events import (
    TrackAddedEvent, TrackDeletedEvent, LibraryScannedEvent
)


class LibraryViewModel:
    """ViewModel for library tab."""

    def __init__(self):
        self.event_bus = container.event_bus
        self.library_service = container.library_service

        # State
        self.all_tracks: List[Track] = []
        self.filtered_tracks: List[Track] = []
        self.search_filter: str = ""

        # Callbacks
        self.on_library_updated = None
        self.on_track_added = None
        self.on_track_removed = None

        # Subscribe to events
        self.event_bus.subscribe('TrackAddedEvent', self._on_track_added)
        self.event_bus.subscribe('TrackDeletedEvent', self._on_track_deleted)

    def load_library(self, limit: int = 100):
        """Load all tracks from library."""
        self.all_tracks = self.library_service.get_all_tracks(limit=limit)
        self._apply_filter()
        self._notify_ui()

    def search_tracks(self, query: str):
        """Search tracks by query."""
        self.search_filter = query
        self._apply_filter()
        self._notify_ui()

    def delete_track(self, track_id: int) -> bool:
        """Delete a track from library."""
        return self.library_service.delete_track(track_id)

    def get_track_by_id(self, track_id: int) -> Optional[Track]:
        """Get track details."""
        for track in self.all_tracks:
            if track.id == track_id:
                return track
        return None

    def _apply_filter(self):
        """Apply search filter to tracks."""
        if not self.search_filter:
            self.filtered_tracks = self.all_tracks.copy()
        else:
            query = self.search_filter.lower()
            self.filtered_tracks = [
                t for t in self.all_tracks
                if query in t.title.lower() or query in t.artist.lower()
            ]

    def _on_track_added(self, event: TrackAddedEvent):
        """Handle track added event."""
        self.all_tracks.insert(0, event.track)
        self._apply_filter()
        if self.on_track_added:
            self.on_track_added(event.track)
        self._notify_ui()

    def _on_track_deleted(self, event):
        """Handle track deleted event."""
        self.all_tracks = [t for t in self.all_tracks if t.id != event.track_id]
        self._apply_filter()
        if self.on_track_removed:
            self.on_track_removed(event.track_id)
        self._notify_ui()

    def _notify_ui(self):
        """Notify UI about changes."""
        if self.on_library_updated:
            self.on_library_updated(self.filtered_tracks)
