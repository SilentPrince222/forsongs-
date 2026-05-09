import asyncio
from typing import List, Optional
from urllib.parse import quote
from src.domain import TrackInfo, HttpClient
from .base_parser import BaseMusicParser


class PixabayAudioParser(BaseMusicParser):
    """Parser for Pixabay Audio (free sound effects and music)."""

    def __init__(self, http_client: HttpClient, api_key: Optional[str] = None):
        super().__init__(http_client)
        self._source_name = 'pixabay'
        self.api_key = api_key or 'your_pixabay_api_key'  # Replace with actual API key
        self.base_url = 'https://pixabay.com/api/'

    async def search(self, query: str, limit: int = 20) -> List[TrackInfo]:
        """Search Pixabay for audio tracks."""
        try:
            # Encode query for URL
            encoded_query = quote(query)

            # Build search URL
            search_url = (
                f"{self.base_url}?key={self.api_key}"
                f"&q={encoded_query}&audio&per_page={limit}"
            )

            # Make request
            response = await self._make_request(search_url)

            if not response or 'hits' not in response:
                return []

            tracks = []
            for item in response['hits']:
                track_info = self._parse_track_data(item)
                if track_info:
                    tracks.append(track_info)

            return tracks[:limit]

        except Exception as e:
            print(f"Pixabay search error: {e}")
            return []

    async def get_download_url(self, track_id: str) -> str:
        """Get download URL for Pixabay track."""
        # Pixabay provides download URL directly in search results
        # track_id here is actually the download URL
        return track_id

    def _parse_track_data(self, data: dict) -> Optional[TrackInfo]:
        """Parse Pixabay track data into TrackInfo."""
        try:
            # Extract basic info
            audio_id = data.get('id')
            if not audio_id:
                return None

            # Pixabay audio files often don't have traditional titles
            # Use a combination of tags or filename
            tags = data.get('tags', '').split(', ')
            title = tags[0] if tags else f"Audio {audio_id}"

            # Use "Pixabay" as artist since it's a platform
            artist = "Pixabay"

            # Extract duration (in seconds)
            duration = data.get('duration', 0)

            # Build source URL
            source_url = f"https://pixabay.com/sound-effects/{data.get('pageURL', '').split('/')[-1]}"

            # Extract audio URL (download URL)
            audio_url = data.get('audio')

            return TrackInfo(
                title=title,
                artist=artist,
                album='',  # Pixabay doesn't have albums
                duration=int(duration),
                genre='sound effect',  # Most Pixabay audio is sound effects
                year='',  # No year info
                license='cc0',  # Pixabay uses CC0 license
                cover_url=None,  # No covers for audio
                source_url=source_url,
                download_url=audio_url,
                source='pixabay'
            )

        except Exception as e:
            print(f"Error parsing Pixabay track data: {e}")
            return None