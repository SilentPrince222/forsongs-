import asyncio
from typing import List, Optional, Dict, Any
from urllib.parse import quote
from src.domain import TrackInfo, HttpClient
from .base_parser import BaseMusicParser


class JamendoMusicParser(BaseMusicParser):
    """Parser for Jamendo music platform."""

    def __init__(self, http_client: HttpClient, client_id: Optional[str] = None):
        super().__init__(http_client)
        self._source_name = 'jamendo'
        self.client_id = client_id or 'your_jamendo_client_id'  # Replace with actual client ID
        self.base_url = 'https://api.jamendo.com/v3.0'

    async def search(self, query: str, limit: int = 20) -> List[TrackInfo]:
        """Search Jamendo for tracks."""
        try:
            # Encode query for URL
            encoded_query = quote(query)

            # Build search URL
            search_url = (
                f"{self.base_url}/tracks/?client_id={self.client_id}"
                f"&format=json&search={encoded_query}&limit={limit}"
                "&include=licenses+albums+artists&groupby=track"
            )

            # Make request
            response = await self._make_request(search_url)

            if not response or 'results' not in response:
                return []

            tracks = []
            for item in response['results']:
                track_info = self._parse_track_data(item)
                if track_info:
                    tracks.append(track_info)

            return tracks[:limit]

        except Exception as e:
            print(f"Jamendo search error: {e}")
            return []

    async def get_download_url(self, track_id: str) -> str:
        """Get download URL for Jamendo track."""
        try:
            # Get track details
            track_url = (
                f"{self.base_url}/tracks/?client_id={self.client_id}"
                f"&format=json&id={track_id}&include=audiodownload"
            )

            response = await self._make_request(track_url)

            if response and 'results' in response and len(response['results']) > 0:
                track_data = response['results'][0]
                # Jamendo provides audiodownload field
                if 'audiodownload' in track_data and track_data['audiodownload']:
                    return track_data['audiodownload']

            raise ValueError(f"No download URL found for track {track_id}")

        except Exception as e:
            raise ValueError(f"Failed to get Jamendo download URL for {track_id}: {e}")

    def _parse_track_data(self, data: dict) -> Optional[TrackInfo]:
        """Parse Jamendo track data into TrackInfo."""
        try:
            # Extract basic info
            title = data.get('name', '').strip()
            artist = ''

            # Extract artist info
            if 'artist_name' in data:
                artist = data['artist_name']
            elif 'artist' in data and isinstance(data['artist'], dict):
                artist = data['artist'].get('name', 'Unknown')

            if not title or not artist:
                return None

            # Build source URL
            track_id = data.get('id')
            source_url = f"https://www.jamendo.com/track/{track_id}"

            # Extract duration (in seconds)
            duration = data.get('duration', 0)

            # Extract album info
            album = ''
            if 'album_name' in data:
                album = data['album_name']
            elif 'album' in data and isinstance(data['album'], dict):
                album = data['album'].get('name', '')

            # Extract license info
            license_type = data.get('license_ccurl', '')
            license = 'cc-by'  # Default
            if 'by-nc' in license_type.lower():
                license = 'cc-by-nc'
            elif 'by-sa' in license_type.lower():
                license = 'cc-by-sa'
            elif 'by-nc-sa' in license_type.lower():
                license = 'cc-by-nc-sa'

            # Extract cover URL
            cover_url = None
            if 'album' in data and isinstance(data['album'], dict):
                cover_url = data['album'].get('image')

            return TrackInfo(
                title=title,
                artist=artist,
                album=album,
                duration=duration,
                genre=data.get('genre', ''),
                year=data.get('releasedate', '').split('-')[0] if data.get('releasedate') else '',
                license=license,
                cover_url=cover_url,
                source_url=source_url,
                download_url=data.get('audiodownload'),
                source='jamendo'
            )

        except Exception as e:
            print(f"Error parsing Jamendo track data: {e}")
            return None