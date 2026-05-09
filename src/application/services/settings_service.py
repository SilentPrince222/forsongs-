"""Service for managing application settings."""

import json
from pathlib import Path
from typing import Any, Dict
from src.application.event_bus import event_bus
from src.domain.events import SettingsChangedEvent


class SettingsService:
    """Service for application settings management."""

    def __init__(self, config_file: Path | str = None):
        self.config_file = Path(config_file) if config_file else Path("config.json")
        self._settings: Dict[str, Any] = {}
        self._load_defaults()
        self._load_from_file()

    def _load_defaults(self):
        """Load default settings."""
        self._settings = {
            'download_folder': 'downloads',
            'max_concurrent_downloads': 3,
            'theme': 'dark',
            'auto_start': False,
            'notifications_enabled': True,
            'sources_enabled': {
                'fma': True,
                'jamendo': True,
                'archive': True,
                'pixabay': True,
                'bensound': True,
                'soundclick': True,
            }
        }

    def _load_from_file(self):
        """Load settings from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    saved = json.load(f)
                self._settings.update(saved)
            except Exception:
                pass

    def _save_to_file(self):
        """Save settings to file."""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self._settings, f, indent=2)
        except Exception:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self._settings.get(key, default)

    def set(self, key: str, value: Any):
        """Set a setting value and persist."""
        old_value = self._settings.get(key)
        self._settings[key] = value
        self._save_to_file()
        event_bus.publish(SettingsChangedEvent(setting_name=key, new_value=value))

    def get_all(self) -> Dict[str, Any]:
        """Get all settings."""
        return self._settings.copy()

    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self._load_defaults()
        self._save_to_file()
        # Publish events for all settings changed
        for key, value in self._settings.items():
            event_bus.publish(SettingsChangedEvent(setting_name=key, new_value=value))
