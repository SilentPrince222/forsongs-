import asyncio
import os
from typing import Optional
from pathlib import Path
from src.domain import (
    Track, MetadataError,
    TrackAddedEvent
)
from src.application.event_bus import event_bus
from src.infrastructure.metadata.processor import MetadataProcessor
from src.infrastructure.metadata.cover_downloader import CoverDownloader


class MetadataService:
    """Service for processing track metadata and covers."""

    def __init__(self, track_repository):
        self.track_repository = track_repository
        self.metadata_processor = MetadataProcessor()
        self.cover_downloader = CoverDownloader()

        # Subscribe to track added events (after track is saved to DB)
        event_bus.subscribe('TrackAddedEvent', self._on_track_added)

    def _on_track_added(self, event: TrackAddedEvent):
        """Handle track added event."""
        asyncio.create_task(self._process_track_metadata(event.track))

    async def _process_track_metadata(self, track: Track):
        """Process metadata for a track."""
        try:
            # Add metadata to file
            await self.metadata_processor.add_metadata(track.file_path, {
                'title': track.title,
                'artist': track.artist,
                'album': track.album,
                'genre': track.genre,
                'year': track.year
            })

            # Download and set cover if URL available
            if track.cover_url:
                cover_path = await self._download_cover(track.cover_url, track.file_path)
                if cover_path:
                    track.cover_path = cover_path

            # Save updated track (cover_path) to database
            self.track_repository.save(track)

        except Exception as e:
            # Log error but don't fail the operation
            print(f"Failed to process metadata for {track.title}: {e}")

    async def _download_cover(self, cover_url: str, track_path: str) -> Optional[str]:
        """Download cover image and return local path."""
        try:
            # Generate filename based on track
            track_name = os.path.splitext(os.path.basename(track_path))[0]
            cover_filename = f"{track_name}_cover.jpg"
            cover_dir = Path('data') / 'covers'
            cover_dir.mkdir(parents=True, exist_ok=True)
            cover_path = cover_dir / cover_filename

            success = self.cover_downloader.download_cover(cover_url, cover_path)
            return str(cover_path) if success else None

        except Exception as e:
            print(f"Failed to download cover from {cover_url}: {e}")
            return None

    async def extract_metadata(self, file_path: str) -> dict:
        """Extract metadata from audio file."""
        try:
            return await self.metadata_processor.get_metadata(file_path)
        except Exception as e:
            raise MetadataError(f"Failed to extract metadata from {file_path}: {e}")

    async def update_track_metadata(self, track: Track, metadata: dict):
        """Update track metadata."""
        try:
            track.title = metadata.get('title', track.title)
            track.artist = metadata.get('artist', track.artist)
            track.album = metadata.get('album', track.album)
            track.genre = metadata.get('genre', track.genre)
            track.year = metadata.get('year', track.year)

            await self.metadata_processor.add_metadata(track.file_path, metadata)
        except Exception as e:
            raise MetadataError(f"Failed to update metadata for {track.title}: {e}")