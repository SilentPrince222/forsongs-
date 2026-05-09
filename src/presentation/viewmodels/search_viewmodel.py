from typing import List, Optional
from src.domain import TrackInfo, SearchStartedEvent, SearchCompletedEvent, SearchFailedEvent
from src.presentation.di_container import container


class SearchViewModel:
    """ViewModel for search functionality following MVVM pattern."""

    def __init__(self):
        self.event_bus = container.event_bus
        self.parser_manager = container.parser_manager

        # State
        self.search_query = ""
        self.selected_source = None
        self.is_searching = False
        self.search_results: List[TrackInfo] = []
        self.search_error: Optional[str] = None

        # Callbacks for UI updates
        self.on_search_started = None
        self.on_search_completed = None
        self.on_search_failed = None

        # Subscribe to search events
        self.event_bus.subscribe('SearchStartedEvent', self._on_search_started)
        self.event_bus.subscribe('SearchCompletedEvent', self._on_search_completed)
        self.event_bus.subscribe('SearchFailedEvent', self._on_search_failed)

    def set_search_query(self, query: str):
        """Set search query."""
        self.search_query = query.strip()

    def set_selected_source(self, source: str):
        """Set selected source filter."""
        self.selected_source = source if source != "Все источники" else None

    def perform_search(self):
        """Perform search operation."""
        if not self.search_query:
            return

        from src.domain import SearchCommand
        search_cmd = SearchCommand(
            query=self.search_query,
            source=self.selected_source,
            limit=20
        )
        self.event_bus.publish(search_cmd)

    def get_available_sources(self) -> List[str]:
        """Get list of available sources for UI."""
        return ["Все источники"] + self.parser_manager.get_available_sources()

    def download_track(self, track: TrackInfo):
        """Start downloading a track."""
        from src.domain import DownloadCommand
        download_cmd = DownloadCommand(track_info=track, output_path="downloads")
        self.event_bus.publish(download_cmd)

    def _on_search_started(self, event: SearchStartedEvent):
        """Handle search started event."""
        self.is_searching = True
        self.search_error = None
        self.search_results.clear()

        if self.on_search_started:
            self.on_search_started()

    def _on_search_completed(self, event: SearchCompletedEvent):
        """Handle search completed event."""
        self.is_searching = False
        self.search_results = event.results

        if self.on_search_completed:
            self.on_search_completed(self.search_results)

    def _on_search_failed(self, event: SearchFailedEvent):
        """Handle search failed event."""
        self.is_searching = False
        self.search_error = event.error

        if self.on_search_failed:
            self.on_search_failed(self.search_error)

    def get_search_status_text(self) -> str:
        """Get current search status text for UI."""
        if self.is_searching:
            return f"Поиск '{self.search_query}'..."
        elif self.search_error:
            return f"Ошибка: {self.search_error}"
        elif self.search_results:
            return f"Найдено {len(self.search_results)} результатов"
        else:
            return ""