import asyncio
from typing import List, Optional
from src.domain import (
    TrackInfo, MusicParser,
    SearchStartedEvent, SearchCompletedEvent, SearchFailedEvent,
    SearchCommand, ParserError
)
from src.application.event_bus import event_bus


class SearchService:
    """Service for searching music across multiple sources."""

    def __init__(self, parsers: List[MusicParser]):
        self.parsers = {parser.source_name: parser for parser in parsers}

        # Subscribe to search commands
        event_bus.subscribe('SearchCommand', self._handle_search_command)

    def _handle_search_command(self, command: SearchCommand):
        """Handle search command."""
        asyncio.create_task(self._perform_search(command.query, command.source, command.limit))

    async def _perform_search(self, query: str, source: Optional[str], limit: int):
        """Perform search across sources."""
        event_bus.publish(SearchStartedEvent(query=query, source=source))

        try:
            all_results = []

            if source and source in self.parsers:
                # Search specific source
                results = await self.parsers[source].search(query, limit)
                all_results.extend(results)
                event_bus.publish(SearchCompletedEvent(
                    query=query,
                    results=results,
                    source=source
                ))
            else:
                # Search all sources in parallel
                tasks = []
                for parser in self.parsers.values():
                    task = parser.search(query, limit // len(self.parsers) or 1)
                    tasks.append(task)

                results_list = await asyncio.gather(*tasks, return_exceptions=True)

                for i, results in enumerate(results_list):
                    if isinstance(results, Exception):
                        source_name = list(self.parsers.keys())[i]
                        event_bus.publish(SearchFailedEvent(
                            query=query,
                            error=f"Search failed for {source_name}: {str(results)}",
                            source=source_name
                        ))
                    else:
                        all_results.extend(results)

                event_bus.publish(SearchCompletedEvent(
                    query=query,
                    results=all_results,
                    source=None
                ))

        except Exception as e:
            event_bus.publish(SearchFailedEvent(
                query=query,
                error=str(e),
                source=source
            ))

    async def search_single_source(self, source: Optional[str], query: str, limit: int = 20) -> List[TrackInfo]:
        """Search a single source or all sources if source is None."""
        if source is None:
            # Search all sources
            return await self.search_all_sources(query, limit)

        if source not in self.parsers:
            raise ParserError(f"Unknown source: {source}")

        try:
            return await self.parsers[source].search(query, limit)
        except Exception as e:
            raise ParserError(f"Search failed for {source}: {str(e)}")

    async def search_all_sources(self, query: str, limit: int = 20) -> List[TrackInfo]:
        """Search across all available sources."""
        # Distribute limit among sources
        per_source_limit = max(1, limit // len(self.parsers))
        all_results = []

        # Search all sources in parallel
        tasks = [parser.search(query, per_source_limit) for parser in self.parsers.values()]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for i, result in enumerate(results):
            source_name = list(self.parsers.keys())[i]
            if isinstance(result, Exception):
                print(f"Search failed for {source_name}: {result}")
            else:
                all_results.extend(result)

        # Return limited results
        return all_results[:limit]

    def get_available_sources(self) -> List[str]:
        """Get list of available music sources."""
        return list(self.parsers.keys())