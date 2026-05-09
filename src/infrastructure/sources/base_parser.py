import asyncio
from abc import ABC, abstractmethod
from typing import List
from src.domain import TrackInfo, MusicParser, HttpClient


class BaseMusicParser(MusicParser):
    """Base implementation for music parsers."""

    def __init__(self, http_client: HttpClient):
        self.http_client = http_client
        self._source_name = ""

    @property
    def source_name(self) -> str:
        return self._source_name

    @abstractmethod
    async def search(self, query: str, limit: int = 20) -> List[TrackInfo]:
        """Search for tracks by query."""
        pass

    @abstractmethod
    async def get_download_url(self, track_id: str) -> str:
        """Get direct download URL for a track."""
        pass

    async def _make_request(self, url: str, **kwargs) -> dict:
        """Helper method to make HTTP requests."""
        return await self.http_client.get(url, **kwargs)

    def _normalize_track_info(self, raw_data: dict) -> TrackInfo:
        """Normalize raw data from different sources."""
        return TrackInfo.from_raw_data(raw_data)