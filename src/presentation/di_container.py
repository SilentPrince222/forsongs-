from src.application import EventBus, DownloadService
from src.application.services.parser_manager import ParserManager
from src.application.services.metadata_service import MetadataService
from src.application.services.library_service import LibraryService
from src.application.services.playlist_service import PlaylistService
from src.application.services.settings_service import SettingsService
from src.infrastructure.database import PeeweeTrackRepository, PeeweePlaylistRepository, PeeweePlaylistTrackRepository, init_database
from src.infrastructure.sources import (
    FMAMusicParser, JamendoMusicParser, InternetArchiveMusicParser,
    PixabayAudioParser, BensoundMusicParser, SoundClickMusicParser
)
from src.infrastructure.http import AioHttpClient
from src.infrastructure.downloader import DownloadManager


class DependencyContainer:
    """Dependency injection container for the application."""

    def __init__(self):
        self._instances = {}
        self._setup_dependencies()

    def _setup_dependencies(self):
        """Initialize all dependencies."""

        # Initialize database
        init_database()

        # Infrastructure layer
        self._instances['http_client'] = AioHttpClient()
        self._instances['download_manager'] = DownloadManager()

        # Repositories
        self._instances['track_repository'] = PeeweeTrackRepository()
        self._instances['playlist_repository'] = PeeweePlaylistRepository()
        self._instances['playlist_track_repository'] = PeeweePlaylistTrackRepository()

        # Parsers
        self._instances['parsers'] = [
            FMAMusicParser(self._instances['http_client']),
            JamendoMusicParser(self._instances['http_client']),
            InternetArchiveMusicParser(self._instances['http_client']),
            PixabayAudioParser(self._instances['http_client']),
            BensoundMusicParser(self._instances['http_client']),
            SoundClickMusicParser(self._instances['http_client'])
        ]

        # Parser manager (includes SearchService)
        self._instances['parser_manager'] = ParserManager(self._instances['parsers'])

        # Application layer
        self._instances['event_bus'] = EventBus()
        self._instances['download_service'] = DownloadService(
            self._instances['track_repository'],
            self._instances['download_manager']
        )
        self._instances['metadata_service'] = MetadataService(
            self._instances['track_repository']
        )
        self._instances['library_service'] = LibraryService(
            self._instances['track_repository']
        )
        self._instances['playlist_service'] = PlaylistService(
            self._instances['playlist_repository'],
            self._instances['playlist_track_repository']
        )
        self._instances['settings_service'] = SettingsService()

    def get(self, name: str):
        """Get a dependency by name."""
        return self._instances.get(name)

    @property
    def event_bus(self):
        return self._instances['event_bus']

    @property
    def download_service(self):
        return self._instances['download_service']

    @property
    def search_service(self):
        return self._instances['search_service']

    @property
    def track_repository(self):
        return self._instances['track_repository']

    @property
    def download_manager(self):
        return self._instances['download_manager']

    @property
    def parser_manager(self):
        return self._instances['parser_manager']

    @property
    def metadata_service(self):
        return self._instances['metadata_service']

    @property
    def library_service(self):
        return self._instances['library_service']

    @property
    def playlist_service(self):
        return self._instances['playlist_service']

    @property
    def settings_service(self):
        return self._instances['settings_service']

    async def startup(self):
        """Startup all async components."""
        await self._instances['download_manager'].start()

    async def shutdown(self):
        """Shutdown all async components."""
        await self._instances['download_manager'].stop()
        await self._instances['http_client'].__aexit__(None, None, None)


# Global container instance
container = DependencyContainer()