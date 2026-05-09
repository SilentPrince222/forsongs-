"""Playlists tab for managing playlists."""

import customtkinter as ctk
from typing import List, Optional
from src.presentation.viewmodels.playlists_viewmodel import PlaylistsViewModel
from src.presentation.widgets.track_card import TrackCard
from src.domain import Playlist, PlaylistTrack
from tkinter import messagebox


class PlaylistsTab(ctk.CTkFrame):
    """Playlists tab UI."""

    def __init__(self, master, viewmodel: Optional[PlaylistsViewModel] = None):
        super().__init__(master)
        self.viewmodel = viewmodel

        self._setup_ui()
        self._bind_viewmodel()

    def _setup_ui(self):
        """Setup playlists tab UI."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Main container using grid
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.columnconfigure(0, weight=1, minsize=250)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)

        # Playlists list frame (left)
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)

        # Header
        header_label = ctk.CTkLabel(
            left_frame,
            text="🎵 Плейлисты",
            font=("Arial", 16, "bold")
        )
        header_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        create_btn = ctk.CTkButton(
            left_frame,
            text="+ Создать",
            command=self._show_create_playlist_dialog,
            height=30
        )
        create_btn.grid(row=0, column=1, padx=10, pady=10)

        # Playlists list
        self.playlists_list = ctk.CTkScrollableFrame(left_frame)
        self.playlists_list.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Tracks frame (right)
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        right_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)

        # Tracks header
        tracks_header = ctk.CTkLabel(
            right_frame,
            text="Треки",
            font=("Arial", 16, "bold")
        )
        tracks_header.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Tracks list
        self.tracks_list = ctk.CTkScrollableFrame(right_frame)
        self.tracks_list.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def _bind_viewmodel(self):
        """Bind to viewmodel callbacks."""
        if self.viewmodel:
            self.viewmodel.on_playlists_updated = self._on_playlists_updated
            self.viewmodel.on_tracks_updated = self._on_tracks_updated
            # Load initial data
            self.viewmodel.load_playlists()

    def _show_create_playlist_dialog(self):
        """Show create playlist dialog."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Создать плейлист")
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.wait_visibility()
        dialog.grab_set()

        name_label = ctk.CTkLabel(dialog, text="Название плейлиста:")
        name_label.pack(pady=10)
        name_entry = ctk.CTkEntry(dialog, width=300)
        name_entry.pack(pady=5)

        desc_label = ctk.CTkLabel(dialog, text="Описание (опционально):")
        desc_label.pack(pady=5)
        desc_entry = ctk.CTkEntry(dialog, width=300)
        desc_entry.pack(pady=5)

        def create():
            name = name_entry.get().strip()
            if name and self.viewmodel:
                self.viewmodel.create_playlist(name, desc_entry.get().strip() or None)
            dialog.destroy()

        create_btn = ctk.CTkButton(dialog, text="Создать", command=create)
        create_btn.pack(pady=10)

        cancel_btn = ctk.CTkButton(
            dialog,
            text="Отмена",
            command=dialog.destroy,
            fg_color="gray"
        )
        cancel_btn.pack(pady=5)

    def _on_playlists_updated(self, playlists: List[Playlist]):
        """Handle playlists update."""
        # Clear list
        for widget in self.playlists_list.winfo_children():
            widget.destroy()

        if not playlists:
            label = ctk.CTkLabel(self.playlists_list, text="Нет плейлистов", text_color="gray")
            label.pack(pady=20)
            return

        for playlist in playlists:
            btn = ctk.CTkButton(
                self.playlists_list,
                text=f"📁 {playlist.name}",
                anchor="w",
                command=lambda p=playlist: self._select_playlist(p.id)
            )
            btn.pack(fill="x", padx=5, pady=2)

    def _select_playlist(self, playlist_id: int):
        """Select a playlist."""
        if self.viewmodel:
            self.viewmodel.select_playlist(playlist_id)

    def _on_tracks_updated(self, tracks: List[PlaylistTrack]):
        """Handle tracks update for selected playlist."""
        # Clear tracks
        for widget in self.tracks_list.winfo_children():
            widget.destroy()

        if not tracks:
            label = ctk.CTkLabel(self.tracks_list, text="Плейлист пуст", text_color="gray")
            label.pack(pady=20)
            return

        # Display tracks (need to resolve full track info from ID)
        # For now just show track IDs - will be resolved via service
        for pt in tracks:
            label = ctk.CTkLabel(
                self.tracks_list,
                text=f"Track ID: {pt.track_id} (pos: {pt.position})",
                anchor="w"
            )
            label.pack(fill="x", padx=5, pady=2)
