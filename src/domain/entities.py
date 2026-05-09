from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Track:
    """Domain entity representing a music track in the library."""
    id: Optional[int] = None
    title: str = ""
    artist: str = ""
    album: Optional[str] = None
    duration: int = 0  # in seconds
    file_path: str = ""
    source: str = ""  # 'fma', 'jamendo', etc.
    license: Optional[str] = None  # CC-BY, CC0, etc.
    genre: Optional[str] = None
    year: Optional[int] = None
    file_hash: Optional[str] = None  # SHA256
    date_added: datetime = None
    cover_path: Optional[str] = None

    def __post_init__(self):
        if self.date_added is None:
            self.date_added = datetime.now()


@dataclass
class Playlist:
    """Domain entity representing a playlist."""
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    date_created: datetime = None

    def __post_init__(self):
        if self.date_created is None:
            self.date_created = datetime.now()


@dataclass
class PlaylistTrack:
    """Domain entity representing a track in a playlist."""
    id: Optional[int] = None
    playlist_id: int = 0
    track_id: int = 0
    position: int = 0


@dataclass
class TrackInfo:
    """Domain entity for track information from search results."""
    title: str = ""
    artist: str = ""
    album: Optional[str] = None
    duration: int = 0  # in seconds
    genre: Optional[str] = None
    year: Optional[int] = None
    license: Optional[str] = None
    cover_url: Optional[str] = None
    source_url: str = ""
    download_url: Optional[str] = None
    source: str = ""  # source identifier

    @classmethod
    def from_raw_data(cls, raw_data: dict) -> 'TrackInfo':
        """Normalize raw data from different sources."""
        return cls(
            title=raw_data.get('title', 'Unknown'),
            artist=raw_data.get('artist', 'Unknown'),
            album=raw_data.get('album'),
            duration=raw_data.get('duration', 0),
            genre=raw_data.get('genre'),
            year=raw_data.get('year'),
            license=raw_data.get('license'),
            cover_url=raw_data.get('cover_url'),
            source_url=raw_data.get('source_url', ''),
            download_url=raw_data.get('download_url'),
            source=raw_data.get('source', '')
        )


@dataclass
class DownloadTask:
    """Domain entity representing a download task."""
    id: str
    track_info: TrackInfo
    output_path: str
    status: str = "pending"  # pending, downloading, completed, failed, paused
    progress: float = 0.0  # 0.0 to 1.0
    downloaded_bytes: int = 0
    total_bytes: int = 0
    speed_bps: int = 0  # bytes per second
    eta_seconds: int = 0  # estimated time of arrival
    error_message: Optional[str] = None