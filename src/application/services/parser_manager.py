from typing import List, Optional
from src.domain import TrackInfo, MusicParser
from src.application.services.search_service import SearchService


class ParserManager:
    """Manages all music source parsers."""

    def __init__(self, parsers: List[MusicParser]):
        self.parsers = {parser.source_name: parser for parser in parsers}
        self._search_service = SearchService(list(self.parsers.values()))

    def get_available_sources(self) -> List[str]:
        """Get list of available music sources."""
        return list(self.parsers.keys())

    def get_parser(self, source: str) -> Optional[MusicParser]:
        """Get parser for specific source."""
        return self.parsers.get(source)

    def get_search_service(self) -> SearchService:
        """Get the search service for performing searches."""
        return self._search_service

    async def search_all_sources(self, query: str, limit: int = 20) -> List[TrackInfo]:
        """Search across all available sources."""
        return await self._search_service.search_all_sources(query, limit)

    async def search_specific_source(self, source: str, query: str, limit: int = 20) -> List[TrackInfo]:
        """Search a specific source."""
        return await self._search_service.search_single_source(source, query, limit)

    def is_source_available(self, source: str) -> bool:
        """Check if a source is available."""
        return source in self.parsers

    def get_source_info(self, source: str) -> Optional[dict]:
        """Get information about a source."""
        parser = self.parsers.get(source)
        if parser:
            return {
                'name': source,
                'available': True,
                'parser_class': parser.__class__.__name__
            }
        return None