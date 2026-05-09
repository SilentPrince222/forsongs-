"""Library tab for managing collected tracks."""

import customtkinter as ctk
from typing import List, Optional
from src.presentation.viewmodels.library_viewmodel import LibraryViewModel
from src.presentation.widgets.track_card import TrackCard
from src.domain import Track
from tkinter import messagebox


class LibraryTab(ctk.CTkFrame):
    """Library tab UI."""

    def __init__(self, master, viewmodel: Optional[LibraryViewModel] = None):
        super().__init__(master)
        self.viewmodel = viewmodel

        self._setup_ui()
        self._bind_viewmodel()

    def _setup_ui(self):
        """Setup library tab UI."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header with search
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1)

        title_label = ctk.CTkLabel(
            header_frame,
            text="📚 Библиотека",
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.search_entry = ctk.CTkEntry(
            header_frame,
            placeholder_text="Поиск в библиотеке...",
            height=35
        )
        self.search_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.search_entry.bind("<Return>", lambda e: self._perform_search())

        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄",
            width=35,
            height=35,
            command=self._refresh_library
        )
        refresh_btn.grid(row=0, column=2, padx=10, pady=5)

        # Library content
        self.library_frame = ctk.CTkScrollableFrame(self, height=600)
        self.library_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def _bind_viewmodel(self):
        """Bind to viewmodel callbacks."""
        if self.viewmodel:
            self.viewmodel.on_library_updated = self._on_library_updated
            # Load initial data
            self.viewmodel.load_library()

    def _perform_search(self):
        """Perform search."""
        if self.viewmodel:
            query = self.search_entry.get().strip()
            self.viewmodel.search_tracks(query)

    def _refresh_library(self):
        """Refresh library."""
        if self.viewmodel:
            self.viewmodel.load_library()

    def _on_library_updated(self, tracks: List[Track]):
        """Handle library update."""
        # Clear current display
        for widget in self.library_frame.winfo_children():
            widget.destroy()

        if not tracks:
            empty_label = ctk.CTkLabel(
                self.library_frame,
                text="Библиотека пуста",
                font=("Arial", 14),
                text_color="gray"
            )
            empty_label.pack(pady=50)
            return

        # Display tracks
        for track in tracks:
            card = TrackCard(
                self.library_frame,
                track=track,
                download_callback=None  # Library tracks already downloaded
            )
            card.download_btn.configure(state="disabled", text="✓")
            card.pack(fill="x", padx=5, pady=2)
