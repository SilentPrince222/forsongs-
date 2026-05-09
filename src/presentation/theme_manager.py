"""Theme manager for customizing application appearance."""

import customtkinter as ctk
from typing import Optional


class ThemeManager:
    """Manages application themes and colors."""

    THEMES = {
        'dark': {
            'primary': '#1f6aa5',
            'secondary': '#2b2b2b',
            'background': '#1a1a1a',
            'text': '#ffffff',
            'accent': '#3b8ed0'
        },
        'light': {
            'primary': '#1f6aa5',
            'secondary': '#f0f0f0',
            'background': '#ffffff',
            'text': '#000000',
            'accent': '#3b8ed0'
        },
        'system': {
            'primary': 'system',
            'secondary': 'system',
            'background': 'system',
            'text': 'system',
            'accent': 'system'
        }
    }

    def __init__(self):
        self.current_theme = 'dark'

    def set_theme(self, theme_name: str):
        """Set application theme."""
        if theme_name not in self.THEMES:
            theme_name = 'dark'

        ctk.set_appearance_mode(theme_name)
        self.current_theme = theme_name

        # Optionally set custom color theme
        if theme_name != 'system':
            ctk.set_default_color_theme("blue")

    def get_color(self, color_key: str) -> str:
        """Get color for current theme."""
        theme = self.THEMES.get(self.current_theme, self.THEMES['dark'])
        return theme.get(color_key, '#ffffff')

    def toggle_theme(self):
        """Toggle between dark and light."""
        new_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.set_theme(new_theme)
        return new_theme
