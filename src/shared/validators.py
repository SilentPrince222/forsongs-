import re
from typing import Optional


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_url(url: str) -> bool:
    """Validate URL format."""
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))


def validate_track_title(title: str) -> Optional[str]:
    """Validate track title. Returns error message or None."""
    if not title or not title.strip():
        return "Title cannot be empty"

    if len(title.strip()) > 200:
        return "Title too long (max 200 characters)"

    return None


def validate_artist_name(artist: str) -> Optional[str]:
    """Validate artist name. Returns error message or None."""
    if not artist or not artist.strip():
        return "Artist cannot be empty"

    if len(artist.strip()) > 100:
        return "Artist name too long (max 100 characters)"

    return None


def validate_playlist_name(name: str) -> Optional[str]:
    """Validate playlist name. Returns error message or None."""
    if not name or not name.strip():
        return "Playlist name cannot be empty"

    if len(name.strip()) > 50:
        return "Playlist name too long (max 50 characters)"

    # Check for invalid characters
    if re.search(r'[<>:"/\\|?*]', name):
        return "Playlist name contains invalid characters"

    return None


def validate_file_path(filepath: str) -> Optional[str]:
    """Validate file path. Returns error message or None."""
    if not filepath:
        return "File path cannot be empty"

    if len(filepath) > 260:  # Windows MAX_PATH
        return "File path too long"

    # Check for invalid characters in path
    invalid_chars = r'[<>|?*]'
    if re.search(invalid_chars, filepath):
        return "File path contains invalid characters"

    return None


def validate_year(year: Optional[int]) -> Optional[str]:
    """Validate year. Returns error message or None."""
    if year is None:
        return None

    current_year = 2026  # Update as needed
    if year < 1900 or year > current_year + 1:
        return f"Year must be between 1900 and {current_year + 1}"

    return None