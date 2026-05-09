"""Track card widget for displaying track information."""

import customtkinter as ctk
from typing import Callable, Optional
from tkinter import messagebox


class TrackCard(ctk.CTkFrame):
    """Widget displaying a single track with download button."""

    def __init__(
        self,
        master,
        track,
        download_callback: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        self.track = track
        self.download_callback = download_callback

        self._setup_ui()

    def _setup_ui(self):
        """Setup the track card UI."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # Track info frame
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Title
        self.title_label = ctk.CTkLabel(
            info_frame,
            text=self.track.title,
            font=("Arial", 14, "bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        # Artist and source
        artist_text = f"by {self.track.artist}"
        if hasattr(self.track, 'source') and self.track.source:
            artist_text += f" • {self.track.source.upper()}"
        self.artist_label = ctk.CTkLabel(
            info_frame,
            text=artist_text,
            font=("Arial", 11),
            text_color="gray"
        )
        self.artist_label.grid(row=1, column=0, sticky="w")

        # Duration
        duration_text = self._format_duration(getattr(self.track, 'duration', 0))
        self.duration_label = ctk.CTkLabel(
            info_frame,
            text=duration_text,
            font=("Arial", 11)
        )
        self.duration_label.grid(row=0, column=1, padx=10, sticky="e")

        # License if available
        if hasattr(self.track, 'license') and self.track.license:
            self.license_label = ctk.CTkLabel(
                info_frame,
                text=self.track.license,
                font=("Arial", 10),
                text_color="gray70"
            )
            self.license_label.grid(row=1, column=1, padx=10, sticky="e")

        # Download button
        self.download_btn = ctk.CTkButton(
            self,
            text="⬇️",
            width=40,
            height=30,
            command=self._on_download_clicked
        )
        self.download_btn.grid(row=0, column=1, padx=10, pady=5)

    def _on_download_clicked(self):
        """Handle download button click."""
        if self.download_callback:
            self.download_callback(self.track)

    @staticmethod
    def _format_duration(seconds: int) -> str:
        """Format seconds to MM:SS."""
        if seconds <= 0:
            return "0:00"
        minutes, secs = divmod(seconds, 60)
        return f"{minutes}:{secs:02d}"
