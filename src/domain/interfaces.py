from abc import ABC, abstractmethod
from typing import List, Optional, Protocol
from .entities import Track, Playlist, PlaylistTrack, TrackInfo


class TrackRepository(ABC):
    """Abstract interface for track data operations."""

    @abstractmethod
    def save(self, track: Track) -> Track:
        """Save a track to the database."""
        pass

    @abstractmethod
    def find_by_id(self, track_id: int) -> Optional[Track]:
        """Find a track by ID."""
        pass

    @abstractmethod
    def find_all(self, limit: int = 100, offset: int = 0) -> List[Track]:
        """Find all tracks with pagination."""
        pass

    @abstractmethod
    def search(self, query: str, limit: int = 20) -> List[Track]:
        """Search tracks by title/artist."""
        pass

    @abstractmethod
    def delete(self, track_id: int) -> bool:
        """Delete a track by ID."""
        pass

    @abstractmethod
    def find_by_hash(self, file_hash: str) -> Optional[Track]:
        """Find track by file hash to avoid duplicates."""
        pass


class PlaylistRepository(ABC):
    """Abstract interface for playlist data operations."""

    @abstractmethod
    def save(self, playlist: Playlist) -> Playlist:
        """Save a playlist."""
        pass

    @abstractmethod
    def find_by_id(self, playlist_id: int) -> Optional[Playlist]:
        """Find playlist by ID."""
        pass

    @abstractmethod
    def find_all(self) -> List[Playlist]:
        """Find all playlists."""
        pass

    @abstractmethod
    def delete(self, playlist_id: int) -> bool:
        """Delete playlist by ID."""
        pass


class PlaylistTrackRepository(ABC):
    """Abstract interface for playlist-track relations."""

    @abstractmethod
    def save(self, playlist_track: PlaylistTrack) -> PlaylistTrack:
        """Save playlist-track relation."""
        pass

    @abstractmethod
    def find_by_playlist_id(self, playlist_id: int) -> List[PlaylistTrack]:
        """Find all tracks in a playlist."""
        pass

    @abstractmethod
    def delete_by_playlist_and_track(self, playlist_id: int, track_id: int) -> bool:
        """Remove track from playlist."""
        pass

    @abstractmethod
    def reorder_tracks(self, playlist_id: int, track_orders: List[tuple]) -> bool:
        """Reorder tracks in playlist."""
        pass


class MusicParser(ABC):
    """Abstract interface for music source parsers."""

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Return the name of the music source."""
        pass

    @abstractmethod
    async def search(self, query: str, limit: int = 20) -> List[TrackInfo]:
        """Search for tracks by query."""
        pass

    @abstractmethod
    async def get_download_url(self, track_id: str) -> str:
        """Get direct download URL for a track."""
        pass


class HttpClient(ABC):
    """Abstract interface for HTTP operations."""

    @abstractmethod
    async def get(self, url: str, **kwargs) -> dict:
        """Perform GET request."""
        pass

    @abstractmethod
    async def post(self, url: str, data: dict = None, **kwargs) -> dict:
        """Perform POST request."""
        pass

    @abstractmethod
    async def download_file(self, url: str, output_path: str, progress_callback=None) -> bool:
        """Download file with progress callback."""
        pass


class EventBus(Protocol):
    """Protocol for event bus operations."""

    def publish(self, event):
        """Publish an event to all subscribers."""
        pass

    def subscribe(self, event_type, handler):
        """Subscribe to an event type."""
        pass

    def unsubscribe(self, event_type, handler):
        """Unsubscribe from an event type."""
        pass


class Logger(Protocol):
    """Protocol for logging operations."""

    def info(self, message: str):
        """Log info message."""
        pass

    def error(self, message: str):
        """Log error message."""
        pass

    def debug(self, message: str):
        """Log debug message."""
        pass