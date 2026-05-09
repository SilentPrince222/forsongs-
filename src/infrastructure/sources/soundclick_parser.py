import asyncio
from typing import List, Optional
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup
from src.domain import TrackInfo, HttpClient
from .base_parser import BaseMusicParser


class SoundClickMusicParser(BaseMusicParser):
    """Parser for SoundClick (independent artists music)."""

    def __init__(self, http_client: HttpClient):
        super().__init__(http_client)
        self._source_name = 'soundclick'
        self.base_url = 'https://www.soundclick.com'

    async def search(self, query: str, limit: int = 20) -> List[TrackInfo]:
        """Search SoundClick for tracks."""
        try:
            # SoundClick has a search URL
            encoded_query = quote(query)
            search_url = f"{self.base_url}/search.cfm?q={encoded_query}&type=music"

            response = await self._make_request(search_url)

            if not response or 'text' not in response:
                return []

            soup = BeautifulSoup(response['text'], 'html.parser')

            tracks = []
            # Find track rows in search results
            track_elements = soup.select('.trackRow, .searchResult')[:limit]

            for element in track_elements:
                track_info = self._parse_search_result(element)
                if track_info:
                    tracks.append(track_info)

            return tracks[:limit]

        except Exception as e:
            print(f"SoundClick search error: {e}")
            return []

    def _parse_search_result(self, element) -> Optional[TrackInfo]:
        """Parse SoundClick search result."""
        try:
            # Extract title
            title_elem = element.select_one('.trackTitle, .title, a')
            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)

            # Extract artist
            artist_elem = element.select_one('.artistName, .artist')
            artist = artist_elem.get_text(strip=True) if artist_elem else "Unknown Artist"

            # Build source URL
            link_elem = element.select_one('a')
            if link_elem and link_elem.get('href'):
                source_url = urljoin(self.base_url, link_elem['href'])
            else:
                return None

            # Duration (try to extract if available)
            duration_elem = element.select_one('.duration, .time')
            duration = 0
            if duration_elem:
                duration_text = duration_elem.get_text(strip=True)
                duration = self._parse_duration(duration_text)

            return TrackInfo(
                title=title,
                artist=artist,
                album='',  # SoundClick doesn't have albums
                duration=duration,
                genre='',  # No genre in search results
                year='',  # No year info
                license='cc-by',  # Assume CC-BY (artists choose their own licenses)
                cover_url=None,  # No covers in search
                source_url=source_url,
                download_url=None,  # Download URL needs page scraping
                source='soundclick'
            )

        except Exception as e:
            print(f"Error parsing SoundClick search result: {e}")
            return None

    def _parse_duration(self, duration_text: str) -> int:
        """Parse duration string into seconds."""
        try:
            # Handle formats like "3:25" or "1:23:45"
            parts = duration_text.split(':')
            if len(parts) == 2:
                minutes, seconds = map(int, parts)
                return minutes * 60 + seconds
            elif len(parts) == 3:
                hours, minutes, seconds = map(int, parts)
                return hours * 3600 + minutes * 60 + seconds
            else:
                return 0
        except (ValueError, IndexError):
            return 0

    async def get_download_url(self, track_id: str) -> str:
        """Get download URL for SoundClick track."""
        try:
            # track_id is the source URL
            response = await self._make_request(track_id)

            if not response or 'text' not in response:
                raise ValueError(f"Could not load track page: {track_id}")

            soup = BeautifulSoup(response['text'], 'html.parser')

            # Look for download button/link
            # SoundClick may require login or have different download options
            download_elem = soup.select_one('.downloadBtn, .btn-download, [href*="download"]')

            if download_elem and download_elem.get('href'):
                download_url = urljoin(self.base_url, download_elem['href'])
                return download_url

            # Alternative: look for audio player source
            audio_elem = soup.select_one('audio source, audio')
            if audio_elem:
                if audio_elem.get('src'):
                    return urljoin(self.base_url, audio_elem['src'])

            raise ValueError(f"No download URL found on page: {track_id}")

        except Exception as e:
            raise ValueError(f"Failed to get SoundClick download URL for {track_id}: {e}")

    async def _get_popular_tracks(self, limit: int = 20) -> List[TrackInfo]:
        """Get popular tracks from SoundClick."""
        try:
            # Get main page or popular section
            response = await self._make_request(self.base_url)

            if not response or 'text' not in response:
                return []

            soup = BeautifulSoup(response['text'], 'html.parser')

            tracks = []
            # Find popular tracks (selector may need updating)
            track_elements = soup.select('.popularTrack, .featuredTrack')[:limit]

            for element in track_elements:
                track_info = self._parse_search_result(element)
                if track_info:
                    tracks.append(track_info)

            return tracks

        except Exception as e:
            print(f"Error getting SoundClick popular tracks: {e}")
            return []