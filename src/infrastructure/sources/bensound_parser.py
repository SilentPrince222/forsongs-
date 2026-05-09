import asyncio
from typing import List, Optional
from urllib.parse import quote
from bs4 import BeautifulSoup
from src.domain import TrackInfo, HttpClient
from .base_parser import BaseMusicParser


class BensoundMusicParser(BaseMusicParser):
    """Parser for Bensound (free music for projects)."""

    def __init__(self, http_client: HttpClient):
        super().__init__(http_client)
        self._source_name = 'bensound'
        self.base_url = 'https://www.bensound.com'

    async def search(self, query: str, limit: int = 20) -> List[TrackInfo]:
        """Search Bensound for tracks."""
        try:
            # Bensound doesn't have search API, so we'll get all tracks and filter
            all_tracks_url = f"{self.base_url}/royalty-free-music/track"

            # For now, return popular tracks since no search
            # In a real implementation, we'd scrape the search results
            tracks = await self._get_popular_tracks(limit)

            # Simple filtering by query (case-insensitive)
            query_lower = query.lower()
            filtered_tracks = [
                track for track in tracks
                if query_lower in track.title.lower() or query_lower in track.artist.lower()
            ]

            return filtered_tracks[:limit] if filtered_tracks else tracks[:limit]

        except Exception as e:
            print(f"Bensound search error: {e}")
            return []

    async def _get_popular_tracks(self, limit: int = 20) -> List[TrackInfo]:
        """Get popular tracks from Bensound."""
        try:
            # Get main music page
            response = await self._make_request(f"{self.base_url}/royalty-free-music")

            if not response or 'text' not in response:
                return []

            soup = BeautifulSoup(response['text'], 'html.parser')

            tracks = []
            # Find track elements (this selector may need updating based on site changes)
            track_elements = soup.select('.track-item, .music-track')[:limit]

            for element in track_elements:
                track_info = self._parse_track_element(element)
                if track_info:
                    tracks.append(track_info)

            return tracks

        except Exception as e:
            print(f"Error getting Bensound popular tracks: {e}")
            return []

    def _parse_track_element(self, element) -> Optional[TrackInfo]:
        """Parse Bensound track element."""
        try:
            # Extract title
            title_elem = element.select_one('.track-title, .title, h3')
            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)

            # Bensound music is by Bensound
            artist = "Bensound"

            # Build source URL
            link_elem = element.select_one('a')
            if link_elem and link_elem.get('href'):
                source_url = urljoin(self.base_url, link_elem['href'])
            else:
                source_url = f"{self.base_url}/royalty-free-music"

            # Duration (hardcoded since not easily available)
            duration = 180  # Default 3 minutes

            return TrackInfo(
                title=title,
                artist=artist,
                album='',  # Bensound doesn't have albums
                duration=duration,
                genre='royalty free',  # Bensound's genre
                year='',  # No year info
                license='cc-by',  # Bensound uses CC-BY license
                cover_url=None,  # No covers
                source_url=source_url,
                download_url=None,  # Download URL needs to be extracted from page
                source='bensound'
            )

        except Exception as e:
            print(f"Error parsing Bensound track element: {e}")
            return None

    async def get_download_url(self, track_id: str) -> str:
        """Get download URL for Bensound track."""
        try:
            # track_id is the source URL for Bensound
            # Need to scrape the individual track page for download link
            response = await self._make_request(track_id)

            if not response or 'text' not in response:
                raise ValueError(f"Could not load track page: {track_id}")

            soup = BeautifulSoup(response['text'], 'html.parser')

            # Look for download button/link
            download_elem = soup.select_one('.download-btn, .btn-download, [href*="download"]')
            if download_elem and download_elem.get('href'):
                download_url = urljoin(self.base_url, download_elem['href'])
                return download_url

            raise ValueError(f"No download URL found on page: {track_id}")

        except Exception as e:
            raise ValueError(f"Failed to get Bensound download URL for {track_id}: {e}")


# Helper function for urljoin
def urljoin(base: str, url: str) -> str:
    """Join URL parts."""
    from urllib.parse import urljoin as urllib_urljoin
    return urllib_urljoin(base, url)