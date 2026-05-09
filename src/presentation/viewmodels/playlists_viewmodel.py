"""ViewModel for playlists functionality following MVVM pattern."""

from typing import List, Optional
from src.domain import Playlist, PlaylistTrack
from src.presentation.di_container import container
from src.domain.events import (
    PlaylistCreatedEvent, PlaylistDeletedEvent,
    TrackAddedToPlaylistEvent, TrackRemovedFromPlaylistEvent
)


class PlaylistsViewModel:
    """ViewModel for playlists tab."""

    def __init__(self):
        self.event_bus = container.event_bus
        self.playlist_service = container.playlist_service

        # State
        self.playlists: List[Playlist] = []
        self.selected_playlist: Optional[Playlist] = None
        self.playlist_tracks: List[PlaylistTrack] = []

        # Callbacks
        self.on_playlists_updated = None
        self.on_playlist_selected = None
        self.on_tracks_updated = None

        # Subscribe to events
        self.event_bus.subscribe('PlaylistCreatedEvent', self._on_playlist_created)
        self.event_bus.subscribe('PlaylistDeletedEvent', self._on_playlist_deleted)
        self.event_bus.subscribe('TrackAddedToPlaylistEvent', self._on_track_added)
        self.event_bus.subscribe('TrackRemovedFromPlaylistEvent', self._on_track_removed)

    def load_playlists(self):
        """Load all playlists."""
        self.playlists = self.playlist_service.get_all_playlists()
        self._notify_ui()

    def create_playlist(self, name: str, description: Optional[str] = None) -> Playlist:
        """Create a new playlist."""
        playlist = self.playlist_service.create_playlist(name, description)
        return playlist

    def select_playlist(self, playlist_id: int):
        """Select a playlist to view."""
        self.selected_playlist = self.playlist_service.get_playlist_by_id(playlist_id)
        if self.selected_playlist:
            self.playlist_tracks = self.playlist_service.get_playlist_tracks(playlist_id)
        else:
            self.playlist_tracks = []
        if self.on_playlist_selected:
            self.on_playlist_selected(self.selected_playlist)
        self._notify_tracks_ui()

    def delete_playlist(self, playlist_id: int) -> bool:
        """Delete a playlist."""
        return self.playlist_service.delete_playlist(playlist_id)

    def add_track_to_playlist(self, playlist_id: int, track_id: int) -> bool:
        """Add a track to a playlist."""
        return self.playlist_service.add_track_to_playlist(playlist_id, track_id)

    def remove_track_from_playlist(self, playlist_id: int, track_id: int) -> bool:
        """Remove a track from a playlist."""
        return self.playlist_service.remove_track_from_playlist(playlist_id, track_id)

    def get_playlist_tracks(self, playlist_id: int) -> List[PlaylistTrack]:
        """Get tracks in a playlist."""
        return self.playlist_service.get_playlist_tracks(playlist_id)

    def _on_playlist_created(self, event: PlaylistCreatedEvent):
        """Handle playlist created event."""
        self.load_playlists()

    def _on_playlist_deleted(self, event: PlaylistDeletedEvent):
        """Handle playlist deleted event."""
        self.load_playlists()
        if self.selected_playlist and self.selected_playlist.id == event.playlist_id:
            self.selected_playlist = None
            self.playlist_tracks = []
            self._notify_tracks_ui()

    def _on_track_added(self, event: TrackAddedToPlaylistEvent):
        """Handle track added to playlist event."""
        if self.selected_playlist and self.selected_playlist.id == event.playlist_id:
            self.playlist_tracks = self.playlist_service.get_playlist_tracks(event.playlist_id)
            self._notify_tracks_ui()

    def _on_track_removed(self, event: TrackRemovedFromPlaylistEvent):
        """Handle track removed from playlist event."""
        if self.selected_playlist and self.selected_playlist.id == event.playlist_id:
            self.playlist_tracks = self.playlist_service.get_playlist_tracks(event.playlist_id)
            self._notify_tracks_ui()

    def _notify_ui(self):
        """Notify UI about playlists update."""
        if self.on_playlists_updated:
            self.on_playlists_updated(self.playlists)

    def _notify_tracks_ui(self):
        """Notify UI about tracks update."""
        if self.on_tracks_updated:
            self.on_tracks_updated(self.playlist_tracks)
