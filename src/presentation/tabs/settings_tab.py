"""Settings tab for application configuration."""

import customtkinter as ctk
from pathlib import Path
from tkinter import filedialog
from src.presentation.viewmodels.settings_viewmodel import SettingsViewModel


class SettingsTab(ctk.CTkFrame):
    """Settings tab UI."""

    def __init__(self, master, viewmodel: Optional[SettingsViewModel] = None):
        super().__init__(master)
        self.viewmodel = viewmodel

        self._setup_ui()
        self._bind_viewmodel()

    def _setup_ui(self):
        """Setup settings tab UI."""
        self.grid_columnconfigure(0, weight=1)

        # Scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(self, height=600)
        self.scroll_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Settings sections will be added dynamically
        self._widgets = {}

    def _bind_viewmodel(self):
        """Bind to viewmodel callbacks."""
        if self.viewmodel:
            self.viewmodel.on_settings_updated = self._on_settings_updated
            self._populate_settings()

    def _populate_settings(self):
        """Populate settings controls."""
        if not self.viewmodel:
            return

        row = 0

        # Download folder
        folder_label = ctk.CTkLabel(self.scroll_frame, text="Папка загрузок:")
        folder_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        self._widgets['download_folder'] = ctk.CTkEntry(self.scroll_frame, width=300)
        self._widgets['download_folder'].insert(0, self.viewmodel.get_download_folder())
        self._widgets['download_folder'].grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        browse_btn = ctk.CTkButton(
            self.scroll_frame,
            text="...",
            width=30,
            command=self._browse_download_folder
        )
        browse_btn.grid(row=row, column=2, padx=5, pady=5)
        row += 1

        # Max concurrent downloads
        max_label = ctk.CTkLabel(self.scroll_frame, text="Макс. одновременных загрузок:")
        max_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        self._widgets['max_concurrent'] = ctk.CTkOptionMenu(
            self.scroll_frame,
            values=["1", "2", "3", "4", "5"],
            width=100
        )
        self._widgets['max_concurrent'].set(str(self.viewmodel.get_max_concurrent()))
        self._widgets['max_concurrent'].grid(row=row, column=1, padx=10, pady=5, sticky="w")
        row += 1

        # Theme
        theme_label = ctk.CTkLabel(self.scroll_frame, text="Тема:")
        theme_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        self._widgets['theme'] = ctk.CTkOptionMenu(
            self.scroll_frame,
            values=["dark", "light"],
            width=150,
            command=self._on_theme_changed
        )
        self._widgets['theme'].set(self.viewmodel.get_theme())
        self._widgets['theme'].grid(row=row, column=1, padx=10, pady=5, sticky="w")
        row += 1

        # Enable/disable sources section
        sources_label = ctk.CTkLabel(self.scroll_frame, text="Источники:", font=("Arial", 14, "bold"))
        sources_label.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        row += 1

        self._widgets['sources'] = {}
        for source in ['fma', 'jamendo', 'archive', 'pixabay', 'bensound', 'soundclick']:
            source_label = ctk.CTkLabel(self.scroll_frame, text=source.upper())
            source_label.grid(row=row, column=0, padx=30, pady=2, sticky="w")
            var = ctk.BooleanVar(value=self.viewmodel.is_source_enabled(source))
            checkbox = ctk.CTkCheckBox(
                self.scroll_frame,
                text="",
                variable=var,
                command=lambda s=source, v=var: self._on_source_toggled(s, v)
            )
            checkbox.grid(row=row, column=1, padx=10, pady=2, sticky="w")
            self._widgets['sources'][source] = var
            row += 1

        # Reset button
        reset_btn = ctk.CTkButton(
            self.scroll_frame,
            text="Сбросить настройки",
            command=self._reset_settings,
            fg_color="gray"
        )
        reset_btn.grid(row=row, column=0, padx=10, pady=20, sticky="w")

    def _browse_download_folder(self):
        """Open folder browser."""
        folder = filedialog.askdirectory(title="Выберите папку загрузок")
        if folder:
            self._widgets['download_folder'].delete(0, "end")
            self._widgets['download_folder'].insert(0, folder)
            self.viewmodel.set_download_folder(folder)

    def _on_theme_changed(self, theme: str):
        """Handle theme change."""
        self.viewmodel.set_theme(theme)

    def _on_source_toggled(self, source: str, var):
        """Handle source toggle."""
        self.viewmodel.set_source_enabled(source, var.get())

    def _reset_settings(self):
        """Reset settings to defaults."""
        if messagebox.askyesno("Сброс", "Сбросить все настройки?"):
            self.viewmodel.reset_to_defaults()

    def _on_settings_updated(self, settings: dict):
        """Handle settings update."""
        # Update UI to reflect new settings
        if 'download_folder' in settings and 'download_folder' in self._widgets:
            self._widgets['download_folder'].delete(0, "end")
            self._widgets['download_folder'].insert(0, settings['download_folder'])

        if 'max_concurrent_downloads' in settings and 'max_concurrent' in self._widgets:
            self._widgets['max_concurrent'].set(str(settings['max_concurrent_downloads']))

        if 'theme' in settings and 'theme' in self._widgets:
            self._widgets['theme'].set(settings['theme'])
