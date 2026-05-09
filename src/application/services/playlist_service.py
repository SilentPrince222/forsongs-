"""Service for managing playlists."""

from typing import List, Optional
from src.domain import Playlist, PlaylistTrack, PlaylistRepository, PlaylistTrackRepository
from src.application.event_bus import event_bus
from src.domain.events import (
    PlaylistCreatedEvent, PlaylistDeletedEvent,
    TrackAddedToPlaylistEvent, TrackRemovedFromPlaylistEvent,
    CreatePlaylistCommand
)


class PlaylistService:
    """Service for playlist-related operations."""

    def __init__(
        self,
        playlist_repository: PlaylistRepository,
        playlist_track_repository: PlaylistTrackRepository
    ):
        self.playlist_repository = playlist_repository
        self.playlist_track_repository = playlist_track_repository

        # Subscribe to commands
        event_bus.subscribe('CreatePlaylistCommand', self._handle_create_playlist)

    def get_all_playlists(self) -> List[Playlist]:
        """Get all playlists."""
        return self.playlist_repository.find_all()

    def get_playlist_by_id(self, playlist_id: int) -> Optional[Playlist]:
        """Get playlist by ID."""
        return self.playlist_repository.find_by_id(playlist_id)

    def create_playlist(self, name: str, description: Optional[str] = None) -> Playlist:
        """Create a new playlist."""
        playlist = Playlist(name=name, description=description)
        playlist = self.playlist_repository.save(playlist)
        event_bus.publish(PlaylistCreatedEvent(playlist=playlist))
        return playlist

    def delete_playlist(self, playlist_id: int) -> bool:
        """Delete a playlist."""
        success = self.playlist_repository.delete(playlist_id)
        if success:
            event_bus.publish(PlaylistDeletedEvent(playlist_id=playlist_id))
        return success

    def add_track_to_playlist(self, playlist_id: int, track_id: int, position: int = 0) -> bool:
        """Add a track to a playlist."""
        playlist_track = PlaylistTrack(
            playlist_id=playlist_id,
            track_id=track_id,
            position=position
        )
        self.playlist_track_repository.save(playlist_track)
        event_bus.publish(TrackAddedToPlaylistEvent(
            playlist_id=playlist_id,
            track_id=track_id
        ))
        return True

    def remove_track_from_playlist(self, playlist_id: int, track_id: int) -> bool:
        """Remove a track from a playlist."""
        success = self.playlist_track_repository.delete_by_playlist_and_track(
            playlist_id, track_id
        )
        if success:
            event_bus.publish(TrackRemovedFromPlaylistEvent(
                playlist_id=playlist_id,
                track_id=track_id
            ))
        return success

    def get_playlist_tracks(self, playlist_id: int) -> List[PlaylistTrack]:
        """Get all tracks in a playlist."""
        return self.playlist_track_repository.find_by_playlist_id(playlist_id)

    def reorder_tracks(self, playlist_id: int, track_orders: List[tuple]) -> bool:
        """Reorder tracks in playlist. track_orders is list of (track_id, new_position)."""
        return self.playlist_track_repository.reorder_tracks(playlist_id, track_orders)

    def _handle_create_playlist(self, command: CreatePlaylistCommand):
        """Handle create playlist command."""
        self.create_playlist(command.name, command.description)
