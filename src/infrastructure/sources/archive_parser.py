import asyncio
from typing import List, Optional, Dict, Any
from urllib.parse import quote, urljoin
from src.domain import TrackInfo, HttpClient
from .base_parser import BaseMusicParser


class InternetArchiveMusicParser(BaseMusicParser):
    """Parser for Internet Archive music collections."""

    def __init__(self, http_client: HttpClient):
        super().__init__(http_client)
        self._source_name = 'archive'
        self.base_url = 'https://archive.org'
        self.search_url = 'https://archive.org/advancedsearch.php'

    async def search(self, query: str, limit: int = 20) -> List[TrackInfo]:
        """Search Internet Archive for music."""
        try:
            # Build search query for audio files
            search_params = {
                'q': f'(title:({query}) OR creator:({query})) AND mediatype:(audio)',
                'fl[]': ['identifier', 'title', 'creator', 'description', 'format', 'date'],
                'sort[]': 'downloads desc',
                'rows': limit,
                'output': 'json'
            }

            # Make request
            response = await self._make_request(self.search_url, params=search_params)

            if not response or 'response' not in response or 'docs' not in response['response']:
                return []

            tracks = []
            for item in response['response']['docs']:
                track_info = await self._parse_archive_item(item)
                if track_info:
                    tracks.append(track_info)

            return tracks[:limit]

        except Exception as e:
            print(f"Internet Archive search error: {e}")
            return []

    async def _parse_archive_item(self, data: dict) -> Optional[TrackInfo]:
        """Parse Internet Archive item and extract track info."""
        try:
            identifier = data.get('identifier')
            if not identifier:
                return None

            # Get detailed metadata for the item
            metadata_url = f"{self.base_url}/metadata/{identifier}"
            metadata_response = await self._make_request(metadata_url)

            if not metadata_response or 'metadata' not in metadata_response:
                return None

            metadata = metadata_response['metadata']

            # Check if it's audio
            if metadata.get('mediatype') != 'audio':
                return None

            # Extract basic info
            title = metadata.get('title', ['Unknown'])[0] if isinstance(metadata.get('title'), list) else metadata.get('title', 'Unknown')
            creator = metadata.get('creator', ['Unknown'])[0] if isinstance(metadata.get('creator'), list) else metadata.get('creator', 'Unknown')

            # Internet Archive items are public domain
            license = 'cc0'

            # Build source URL
            source_url = f"{self.base_url}/details/{identifier}"

            # Try to find audio files
            files = metadata_response.get('files', {})
            audio_file = None
            duration = 0

            for filename, file_info in files.items():
                if file_info.get('format', '').lower() in ['vbr mp3', 'mp3', 'flac', 'wav']:
                    audio_file = filename
                    # Try to extract duration if available
                    length = file_info.get('length', '0')
                    try:
                        duration = float(length)
                    except (ValueError, TypeError):
                        duration = 0
                    break

            if not audio_file:
                return None

            # Build download URL
            download_url = f"{self.base_url}/download/{identifier}/{audio_file}"

            # Extract year
            year = ''
            date = metadata.get('date', '')
            if date and len(date) >= 4:
                year = date[:4]

            return TrackInfo(
                title=title,
                artist=creator,
                album='',  # Archive items often don't have albums
                duration=int(duration),
                genre='',  # Archive doesn't categorize by genre well
                year=year,
                license=license,
                cover_url=None,  # Archive doesn't have covers
                source_url=source_url,
                download_url=download_url,
                source='archive'
            )

        except Exception as e:
            print(f"Error parsing Internet Archive item {data.get('identifier', 'unknown')}: {e}")
            return None

    async def get_download_url(self, track_id: str) -> str:
        """Get download URL for Internet Archive track."""
        # track_id is the identifier, download URL is constructed above
        # This method is called when we already have the URL from search
        return f"{self.base_url}/download/{track_id}"

    async def _make_request(self, url: str, params: Optional[Dict[str, Any]] = None) -> dict:
        """Make HTTP request with optional query parameters."""
        if params:
            query_string = '&'.join([f"{k}={quote(str(v))}" for k, v in params.items()])
            url = f"{url}?{query_string}"

        return await super()._make_request(url)