"""Custom progress bar widget for downloads."""

import customtkinter as ctk
from typing import Optional


class CustomProgressBar(ctk.CTkFrame):
    """Widget displaying download progress with speed and ETA."""

    def __init__(
        self,
        master,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the progress bar UI."""
        self.grid_columnconfigure(0, weight=1)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self, height=15)
        self.progress_bar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.progress_bar.set(0)

        # Info frame (speed, eta, percent)
        self.info_label = ctk.CTkLabel(
            self,
            text="0% • 0 B/s • ETA: --",
            font=("Arial", 10)
        )
        self.info_label.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="w")

    def update_progress(
        self,
        progress: float,
        speed_bps: int = 0,
        eta_seconds: int = 0
    ):
        """Update progress display."""
        self.progress_bar.set(progress)

        # Format percentage
        percent = int(progress * 100)

        # Format speed
        speed_text = self._format_speed(speed_bps)

        # Format ETA
        eta_text = self._format_eta(eta_seconds)

        self.info_label.configure(text=f"{percent}% • {speed_text} • ETA: {eta_text}")

    def reset(self):
        """Reset progress to zero."""
        self.progress_bar.set(0)
        self.info_label.configure(text="0% • 0 B/s • ETA: --")

    @staticmethod
    def _format_speed(speed_bps: int) -> str:
        """Format bytes per second to human-readable."""
        if speed_bps >= 1024 * 1024:
            return f"{speed_bps / (1024*1024):.1f} MB/s"
        elif speed_bps >= 1024:
            return f"{speed_bps / 1024:.1f} KB/s"
        else:
            return f"{speed_bps} B/s"

    @staticmethod
    def _format_eta(seconds: int) -> str:
        """Format ETA to human-readable."""
        if seconds <= 0 or seconds == 999999:
            return "--"
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            mins, secs = divmod(seconds, 60)
            return f"{mins}m {secs}s"
        else:
            hours, rem = divmod(seconds, 3600)
            mins, _ = divmod(rem, 60)
            return f"{hours}h {mins}m"
