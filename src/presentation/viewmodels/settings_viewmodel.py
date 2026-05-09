"""ViewModel for settings functionality following MVVM pattern."""

from typing import Callable, Optional
from src.presentation.di_container import container
from src.domain.events import SettingsChangedEvent


class SettingsViewModel:
    """ViewModel for settings tab."""

    def __init__(self):
        self.settings_service = container.settings_service
        self.event_bus = container.event_bus

        # State
        self.settings: dict = {}
        self.on_settings_updated: Optional[Callable] = None

        # Subscribe to events
        self.event_bus.subscribe('SettingsChangedEvent', self._on_setting_changed)

        # Load initial settings
        self._load_settings()

    def _load_settings(self):
        """Load settings from service."""
        self.settings = self.settings_service.get_all()

    def get_setting(self, key: str, default=None):
        """Get a setting value."""
        return self.settings.get(key, default)

    def set_setting(self, key: str, value):
        """Set a setting value."""
        self.settings_service.set(key, value)
        # Note: event bus will trigger _on_setting_changed which calls _notify_ui

    def get_download_folder(self) -> str:
        """Get download folder path."""
        return self.get_setting('download_folder', 'downloads')

    def set_download_folder(self, path: str):
        """Set download folder path."""
        self.set_setting('download_folder', path)

    def get_max_concurrent(self) -> int:
        """Get max concurrent downloads."""
        return self.get_setting('max_concurrent_downloads', 3)

    def set_max_concurrent(self, value: int):
        """Set max concurrent downloads."""
        self.set_setting('max_concurrent_downloads', value)

    def get_theme(self) -> str:
        """Get UI theme."""
        return self.get_setting('theme', 'dark')

    def set_theme(self, theme: str):
        """Set UI theme."""
        self.set_setting('theme', theme)

    def is_source_enabled(self, source: str) -> bool:
        """Check if a source is enabled."""
        sources = self.get_setting('sources_enabled', {})
        return sources.get(source, True)

    def set_source_enabled(self, source: str, enabled: bool):
        """Enable/disable a source."""
        sources = self.get_setting('sources_enabled', {})
        sources[source] = enabled
        self.set_setting('sources_enabled', sources)

    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.settings_service.reset_to_defaults()
        self._load_settings()
        self._notify_ui()

    def _on_setting_changed(self, event: SettingsChangedEvent):
        """Handle setting changed event."""
        self.settings[event.setting_name] = event.new_value
        self._notify_ui()

    def _notify_ui(self):
        """Notify UI about settings update."""
        if self.on_settings_updated:
            self.on_settings_updated(self.settings)
