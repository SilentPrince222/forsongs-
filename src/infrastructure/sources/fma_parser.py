import asyncio
from typing import List, Optional
from urllib.parse import quote
from src.domain import TrackInfo, HttpClient
from .base_parser import BaseMusicParser


class FMAMusicParser(BaseMusicParser):
    """Parser for Free Music Archive (FMA)."""

    def __init__(self, http_client: HttpClient, api_key: Optional[str] = None):
        super().__init__(http_client)
        self._source_name = 'fma'
        self.api_key = api_key or ''
        self.base_url = 'https://freemusicarchive.org/api/v0'

    async def search(self, query: str, limit: int = 20) -> List[TrackInfo]:
        """Search FMA for tracks."""
        try:
            # Encode query for URL
            encoded_query = quote(query)

            # Build search URL
            search_url = f"{self.base_url}/search?type=track&q={encoded_query}&limit={limit}"
            if self.api_key:
                search_url += f"&api_key={self.api_key}"

            # Make request
            response = await self._make_request(search_url)

            if not response or 'data' not in response:
                return []

            tracks = []
            for item in response['data']:
                track_info = self._parse_track_data(item)
                if track_info:
                    tracks.append(track_info)

            return tracks[:limit]

        except Exception as e:
            print(f"FMA search error: {e}")
            return []

    async def get_download_url(self, track_id: str) -> str:
        """Get download URL for FMA track."""
        try:
            # Get track details
            track_url = f"{self.base_url}/tracks/{track_id}"
            if self.api_key:
                track_url += f"?api_key={self.api_key}"

            response = await self._make_request(track_url)

            if response and 'data' in response and len(response['data']) > 0:
                track_data = response['data'][0]
                # FMA provides track_mp3 field with direct download URL
                if 'track_mp3' in track_data and track_data['track_mp3']:
                    return track_data['track_mp3']

            raise ValueError(f"No download URL found for track {track_id}")

        except Exception as e:
            raise ValueError(f"Failed to get FMA download URL for {track_id}: {e}")

    def _parse_track_data(self, data: dict) -> Optional[TrackInfo]:
        """Parse FMA track data into TrackInfo."""
        try:
            # Extract basic info
            title = data.get('track_title', '').strip()
            artist = data.get('artist_name', '').strip()

            if not title or not artist:
                return None

            # Build source URL
            track_id = data.get('track_id')
            source_url = f"https://freemusicarchive.org/music/{data.get('artist_url', '')}/{data.get('album_url', '')}/{data.get('track_url', '')}"

            # Extract duration (in seconds)
            duration = 0
            if 'track_duration' in data:
                duration_str = str(data['track_duration'])
                if ':' in duration_str:
                    # Format like "3:25"
                    parts = duration_str.split(':')
                    if len(parts) == 2:
                        duration = int(parts[0]) * 60 + int(parts[1])
                else:
                    # Assume seconds
                    duration = int(float(duration_str))

            # License info
            license_type = data.get('track_license', '')
            if 'creative commons' in license_type.lower():
                if 'cc0' in license_type.lower():
                    license = 'cc0'
                elif 'by-nc-sa' in license_type.lower():
                    license = 'cc-by-nc-sa'
                elif 'by-nc' in license_type.lower():
                    license = 'cc-by-nc'
                elif 'by-sa' in license_type.lower():
                    license = 'cc-by-sa'
                else:
                    license = 'cc-by'

            return TrackInfo(
                title=title,
                artist=artist,
                album=data.get('album_title', ''),
                duration=duration,
                genre=data.get('track_genres', [{}])[0].get('genre_title', '') if data.get('track_genres') else '',
                year=data.get('track_year', ''),
                license=license,
                cover_url=data.get('track_image_file'),
                source_url=source_url,
                download_url=data.get('track_mp3'),
                source='fma'
            )

        except Exception as e:
            print(f"Error parsing FMA track data: {e}")
            return None