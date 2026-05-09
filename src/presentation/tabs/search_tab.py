"""Search tab for finding tracks."""

import customtkinter as ctk
from typing import List, Optional
from tkinter import messagebox

from src.presentation.viewmodels.search_viewmodel import SearchViewModel
from src.presentation.widgets.track_card import TrackCard
from src.domain import TrackInfo


class SearchTab(ctk.CTkFrame):
    """Search tab UI."""

    def __init__(self, master, viewmodel: Optional[SearchViewModel] = None):
        super().__init__(master)
        self.viewmodel = viewmodel
        self.search_results: List[TrackInfo] = []

        self._setup_ui()
        self._bind_viewmodel()

    def _setup_ui(self):
        """Setup search tab UI."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Search frame
        search_frame = ctk.CTkFrame(self)
        search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Введите название песни или исполнителя...",
            height=40,
            font=("Arial", 14)
        )
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.search_entry.bind("<Return>", lambda e: self._perform_search())

        self.search_button = ctk.CTkButton(
            search_frame,
            text="🔍 Найти",
            command=self._perform_search,
            height=40,
            font=("Arial", 14, "bold")
        )
        self.search_button.grid(row=0, column=1, padx=10, pady=10)

        # Source filter
        self.source_var = ctk.StringVar(value="Все источники")
        self.source_menu = ctk.CTkOptionMenu(
            search_frame,
            values=["Все источники"],
            variable=self.source_var,
            height=40,
            width=150
        )
        self.source_menu.grid(row=0, column=2, padx=10, pady=10)

        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 12)
        )
        self.status_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")

        # Results scrollable frame
        self.results_frame = ctk.CTkScrollableFrame(self, height=600)
        self.results_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    def _bind_viewmodel(self):
        """Bind to viewmodel callbacks."""
        if self.viewmodel:
            self.viewmodel.on_search_started = self._on_search_started
            self.viewmodel.on_search_completed = self._on_search_completed
            self.viewmodel.on_search_failed = self._on_search_failed

            # Populate source dropdown
            sources = self.viewmodel.get_available_sources()
            self.source_menu.configure(values=["Все источники"] + sources)

    def _perform_search(self):
        """Perform search."""
        if not self.viewmodel:
            return

        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Предупреждение", "Введите поисковый запрос")
            return

        source = self.source_var.get()
        self.viewmodel.set_search_query(query)
        self.viewmodel.set_selected_source(source)
        self.viewmodel.perform_search()

    def _on_search_started(self):
        """Handle search started."""
        self.search_button.configure(state="disabled", text="🔄")
        self.status_label.configure(text="Поиск...")

        # Clear results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        self.search_results.clear()

    def _on_search_completed(self, results: List[TrackInfo]):
        """Handle search completed."""
        self.search_button.configure(state="normal", text="🔍 Найти")
        self.search_results = results
        self.status_label.configure(text=f"Найдено: {len(results)} треков")

        # Display results
        for track in results:
            card = TrackCard(
                self.results_frame,
                track=track,
                download_callback=self._on_download_clicked
            )
            card.pack(fill="x", padx=5, pady=2)

    def _on_search_failed(self, error: str):
        """Handle search failed."""
        self.search_button.configure(state="normal", text="🔍 Найти")
        self.status_label.configure(text=f"Ошибка: {error}")
        messagebox.showerror("Ошибка поиска", error)

    def _on_download_clicked(self, track: TrackInfo):
        """Handle download from track card."""
        if self.viewmodel:
            self.viewmodel.download_track(track)
