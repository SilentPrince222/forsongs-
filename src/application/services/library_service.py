"""Service for managing track library operations."""

from typing import List, Optional
from src.domain import Track, TrackRepository, TrackNotFoundError
from src.application.event_bus import event_bus
from src.domain.events import (
    TrackAddedEvent, TrackDeletedEvent, LibraryScannedEvent,
    AddTrackToLibraryCommand
)


class LibraryService:
    """Service for library-related operations."""

    def __init__(self, track_repository: TrackRepository):
        self.track_repository = track_repository

        # Subscribe to commands
        event_bus.subscribe('AddTrackToLibraryCommand', self._handle_add_track)

    def get_all_tracks(self, limit: int = 100, offset: int = 0) -> List[Track]:
        """Get all tracks with pagination."""
        return self.track_repository.find_all(limit=limit, offset=offset)

    def get_track_by_id(self, track_id: int) -> Optional[Track]:
        """Get track by ID."""
        return self.track_repository.find_by_id(track_id)

    def search_tracks(self, query: str, limit: int = 20) -> List[Track]:
        """Search tracks by title or artist."""
        return self.track_repository.search(query, limit=limit)

    def delete_track(self, track_id: int) -> bool:
        """Delete a track from library."""
        track = self.track_repository.find_by_id(track_id)
        if track:
            success = self.track_repository.delete(track_id)
            if success:
                event_bus.publish(TrackDeletedEvent(track_id=track_id))
            return success
        return False

    def find_duplicate_by_hash(self, file_hash: str) -> Optional[Track]:
        """Find track with same file hash."""
        return self.track_repository.find_by_hash(file_hash)

    def _handle_add_track(self, command: AddTrackToLibraryCommand):
        """Handle add track to library command."""
        try:
            track = self.track_repository.save(command.track)
            event_bus.publish(TrackAddedEvent(track=track))
        except Exception as e:
            print(f"Failed to add track to library: {e}")
