from dataclasses import dataclass
from typing import List, Optional
from .entities import Track, TrackInfo, DownloadTask


# Search Events
@dataclass
class SearchStartedEvent:
    query: str
    source: Optional[str] = None


@dataclass
class SearchCompletedEvent:
    query: str
    results: List[TrackInfo]
    source: Optional[str] = None


@dataclass
class SearchFailedEvent:
    query: str
    error: str
    source: Optional[str] = None


# Download Events
@dataclass
class DownloadStartedEvent:
    task: DownloadTask


@dataclass
class DownloadProgressEvent:
    task_id: str
    progress: float
    speed_bps: int
    eta_seconds: int


@dataclass
class DownloadCompletedEvent:
    task_id: str
    track: Track


@dataclass
class DownloadFailedEvent:
    task_id: str
    error: str


@dataclass
class DownloadPausedEvent:
    task_id: str


@dataclass
class DownloadResumedEvent:
    task_id: str


@dataclass
class DownloadCancelledEvent:
    task_id: str


# Library Events
@dataclass
class TrackAddedEvent:
    track: Track


@dataclass
class TrackDeletedEvent:
    track_id: int


@dataclass
class LibraryScannedEvent:
    new_tracks: List[Track]


# Playlist Events
@dataclass
class PlaylistCreatedEvent:
    playlist: Track


@dataclass
class PlaylistDeletedEvent:
    playlist_id: int


@dataclass
class TrackAddedToPlaylistEvent:
    playlist_id: int
    track_id: int


@dataclass
class TrackRemovedFromPlaylistEvent:
    playlist_id: int
    track_id: int


# Application Events
@dataclass
class ApplicationStartedEvent:
    pass


@dataclass
class ApplicationClosingEvent:
    pass


@dataclass
class SettingsChangedEvent:
    setting_name: str
    new_value: any


# Commands (to trigger actions)
@dataclass
class SearchCommand:
    query: str
    source: Optional[str] = None
    limit: int = 20


@dataclass
class DownloadCommand:
    track_info: TrackInfo
    output_path: str


@dataclass
class PauseDownloadCommand:
    task_id: str


@dataclass
class ResumeDownloadCommand:
    task_id: str


@dataclass
class CancelDownloadCommand:
    task_id: str


@dataclass
class AddTrackToLibraryCommand:
    track: Track


@dataclass
class CreatePlaylistCommand:
    name: str
    description: Optional[str] = None