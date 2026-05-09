"""Main application window using Clean Architecture."""

import asyncio
import threading
import customtkinter as ctk
import sys
from pathlib import Path
from typing import Optional

from src.presentation.di_container import container
from src.presentation.viewmodels.search_viewmodel import SearchViewModel
from src.presentation.viewmodels.downloads_viewmodel import DownloadsViewModel
from src.presentation.viewmodels.library_viewmodel import LibraryViewModel
from src.presentation.viewmodels.playlists_viewmodel import PlaylistsViewModel
from src.presentation.viewmodels.settings_viewmodel import SettingsViewModel
from src.presentation.tabs.search_tab import SearchTab
from src.presentation.tabs.downloads_tab import DownloadsTab
from src.presentation.tabs.library_tab import LibraryTab
from src.presentation.tabs.playlists_tab import PlaylistsTab
from src.presentation.tabs.settings_tab import SettingsTab
from src.presentation.theme_manager import ThemeManager


class ForsongApp(ctk.CTk):
    """Main application window (Clean Architecture version)."""

    def __init__(self):
        super().__init__()

        # Initialize DI container
        self.container = container
        self.event_bus = container.event_bus

        # Theme manager
        self.theme_manager = ThemeManager()

        # ViewModels
        self.search_viewmodel = SearchViewModel()
        self.downloads_viewmodel = DownloadsViewModel()
        self.library_viewmodel = LibraryViewModel()
        self.playlists_viewmodel = PlaylistsViewModel()
        self.settings_viewmodel = SettingsViewModel()

        # Window setup
        self.title("Forsong - Легальный музыкальный загрузчик")
        self.geometry("1200x800")
        self.minsize(900, 600)

        # Apply theme from settings
        theme = self.settings_viewmodel.get_theme()
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme("blue")

        # Setup UI
        self._setup_ui()

        # Subscribe to application events
        self._setup_event_subscriptions()

        # Start async components (download manager)
        self._start_async_components()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _setup_ui(self):
        """Setup main UI layout."""
        # Create tabview
        self.tabview = ctk.CTkTabview(self, width=1180, height=750)
        self.tabview.pack(pady=10, padx=10, fill="both", expand=True)

        # Add tabs
        self.tabview.add("🔍 Поиск")
        self.tabview.add("⬇️ Загрузки")
        self.tabview.add("📚 Библиотека")
        self.tabview.add("🎵 Плейлисты")
        self.tabview.add("⚙️ Настройки")

        # Initialize each tab
        self.search_tab = SearchTab(
            self.tabview.tab("🔍 Поиск"),
            viewmodel=self.search_viewmodel
        )
        self.search_tab.pack(fill="both", expand=True)

        self.downloads_tab = DownloadsTab(
            self.tabview.tab("⬇️ Загрузки"),
            viewmodel=self.downloads_viewmodel
        )
        self.downloads_tab.pack(fill="both", expand=True)

        self.library_tab = LibraryTab(
            self.tabview.tab("📚 Библиотека"),
            viewmodel=self.library_viewmodel
        )
        self.library_tab.pack(fill="both", expand=True)

        self.playlists_tab = PlaylistsTab(
            self.tabview.tab("🎵 Плейлисты"),
            viewmodel=self.playlists_viewmodel
        )
        self.playlists_tab.pack(fill="both", expand=True)

        self.settings_tab = SettingsTab(
            self.tabview.tab("⚙️ Настройки"),
            viewmodel=self.settings_viewmodel
        )
        self.settings_tab.pack(fill="both", expand=True)

    def _setup_event_subscriptions(self):
        """Subscribe to application-level events."""
        # We can subscribe to any events that need to affect the main window
        # Most UI updates are handled by ViewModels directly
        pass

    def _start_async_components(self):
        """Start async components in background thread."""
        def run_async():
            asyncio.run(self.container.startup())

        thread = threading.Thread(target=run_async, daemon=True)
        thread.start()

    def _on_closing(self):
        """Handle window close event."""
        # Shutdown async components
        try:
            asyncio.run(self.container.shutdown())
        except Exception as e:
            print(f"Shutdown error: {e}")
        self.destroy()

    def run(self):
        """Run the application."""
        self.mainloop()
