"""Downloads tab for managing active downloads."""

import customtkinter as ctk
from typing import List
from src.presentation.viewmodels.downloads_viewmodel import DownloadsViewModel
from src.presentation.widgets.custom_progress import CustomProgressBar
from src.domain import DownloadTask


class DownloadsTab(ctk.CTkFrame):
    """Downloads tab UI."""

    def __init__(self, master, viewmodel: Optional[DownloadsViewModel] = None):
        super().__init__(master)
        self.viewmodel = viewmodel

        self._setup_ui()
        self._bind_viewmodel()

    def _setup_ui(self):
        """Setup downloads tab UI."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        header_label = ctk.CTkLabel(
            self,
            text="Активные загрузки",
            font=("Arial", 18, "bold")
        )
        header_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Scrollable downloads list
        self.downloads_list = ctk.CTkScrollableFrame(self, height=600)
        self.downloads_list.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def _bind_viewmodel(self):
        """Bind to viewmodel callbacks."""
        if self.viewmodel:
            self.viewmodel.on_downloads_changed = self._update_downloads_ui
            # Initial load
            self._update_downloads_ui()

    def _update_downloads_ui(self):
        """Update downloads list UI."""
        # Clear existing widgets
        for widget in self.downloads_list.winfo_children():
            widget.destroy()

        if not self.viewmodel:
            return

        active_downloads = self.viewmodel.get_active_downloads()

        if not active_downloads:
            empty_label = ctk.CTkLabel(
                self.downloads_list,
                text="Нет активных загрузок",
                font=("Arial", 14),
                text_color="gray"
            )
            empty_label.pack(pady=50)
            return

        for task in active_downloads:
            self._create_download_item(task)

    def _create_download_item(self, task: DownloadTask):
        """Create a download item widget."""
        frame = ctk.CTkFrame(self.downloads_list)
        frame.pack(fill="x", padx=5, pady=5)

        # Track info
        title_label = ctk.CTkLabel(
            frame,
            text=task.track_info.title,
            font=("Arial", 13, "bold")
        )
        title_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        artist_label = ctk.CTkLabel(
            frame,
            text=f"by {task.track_info.artist}",
            font=("Arial", 11),
            text_color="gray"
        )
        artist_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Progress bar
        progress_bar = CustomProgressBar(frame)
        progress_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # Update progress if downloading
        if task.status == 'downloading':
            progress_bar.update_progress(
                task.progress,
                task.speed_bps,
                task.eta_seconds
            )
        elif task.status == 'completed':
            progress_bar.progress_bar.set(1.0)
            progress_bar.info_label.configure(text="Завершено")
        elif task.status == 'failed':
            progress_bar.info_label.configure(text=f"Ошибка: {task.error_message}")
        elif task.status == 'paused':
            progress_bar.info_label.configure(text="Приостановлено")
        else:
            progress_bar.info_label.configure(text="Ожидание")

        # Control buttons frame
        controls = ctk.CTkFrame(frame, fg_color="transparent")
        controls.grid(row=0, column=2, rowspan=2, padx=10, pady=5)

        # Pause/Resume button
        if task.status == 'downloading':
            pause_btn = ctk.CTkButton(
                controls,
                text="⏸️",
                width=30,
                height=25,
                command=lambda: self._pause_download(task.id)
            )
            pause_btn.pack(pady=2)
        elif task.status == 'paused':
            resume_btn = ctk.CTkButton(
                controls,
                text="▶️",
                width=30,
                height=25,
                command=lambda: self._resume_download(task.id)
            )
            resume_btn.pack(pady=2)

        # Cancel button
        cancel_btn = ctk.CTkButton(
            controls,
            text="❌",
            width=30,
            height=25,
            fg_color="red",
            command=lambda: self._cancel_download(task.id)
        )
        cancel_btn.pack(pady=2)

        # Make frame expandable
        frame.grid_columnconfigure(0, weight=1)

    def _pause_download(self, task_id: str):
        """Pause a download."""
        if self.viewmodel:
            self.viewmodel.pause_download(task_id)

    def _resume_download(self, task_id: str):
        """Resume a download."""
        if self.viewmodel:
            self.viewmodel.resume_download(task_id)

    def _cancel_download(self, task_id: str):
        """Cancel a download."""
        if self.viewmodel:
            if messagebox.askyesno("Подтверждение", "Отменить загрузку?"):
                self.viewmodel.cancel_download(task_id)
