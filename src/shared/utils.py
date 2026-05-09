import os
import hashlib
import re
from typing import Optional
from pathlib import Path

from src.domain.constants import DEFAULT_DOWNLOAD_DIR


def sanitize_filename(name: str) -> str:
    """Remove invalid characters for Windows filenames."""
    # Replace invalid characters with underscores
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', name)

    # Remove leading/trailing dots, spaces, and underscores
    sanitized = sanitized.strip('. _')

    # Replace multiple consecutive underscores with single
    sanitized = re.sub(r'_+', '_', sanitized)

    # Remove leading/trailing underscores again
    sanitized = sanitized.strip('_')

    # Ensure not empty and not too long
    if not sanitized:
        sanitized = 'untitled'

    # Windows has 255 char limit for filenames
    if len(sanitized) > 255:
        name_part, ext = os.path.splitext(sanitized)
        max_name_len = 255 - len(ext)
        sanitized = name_part[:max_name_len] + ext

    return sanitized


def format_duration(seconds: int) -> str:
    """Format seconds into MM:SS or HH:MM:SS."""
    if seconds < 3600:  # Less than 1 hour
        minutes, secs = divmod(seconds, 60)
        return f"{minutes:02d}:{secs:02d}"
    else:
        hours, remainder = divmod(seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_filesize(bytes_size: int) -> str:
    """Format bytes into human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return ".1f"
        bytes_size /= 1024.0
    return ".1f"


def calculate_file_hash(filepath: str, algorithm: str = 'sha256') -> str:
    """Calculate file hash."""
    hash_func = hashlib.new(algorithm)

    with open(filepath, 'rb') as f:
        # Read in chunks to handle large files
        for chunk in iter(lambda: f.read(8192), b''):
            hash_func.update(chunk)

    return hash_func.hexdigest()


def ensure_dir(path: str) -> None:
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def get_file_info(filepath: str) -> dict:
    """Get file information."""
    stat = os.stat(filepath)
    return {
        'size': stat.st_size,
        'modified': stat.st_mtime,
        'created': stat.st_ctime,
        'exists': True
    }


def clean_string(text: str) -> str:
    """Clean and normalize string."""
    if not text:
        return ''

    # Remove extra whitespace
    cleaned = ' '.join(text.split())

    # Remove null bytes and other control characters
    cleaned = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', cleaned)

    return cleaned.strip()


def is_valid_audio_file(filepath: str) -> bool:
    """Check if file is a valid audio file."""
    if not os.path.exists(filepath):
        return False

    # Check extension
    _, ext = os.path.splitext(filepath.lower())
    valid_extensions = {'.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac'}

    return ext in valid_extensions


def generate_safe_path(base_dir: str, filename: str, extension: str = '') -> str:
    """Generate a safe file path that doesn't conflict with existing files."""
    safe_name = sanitize_filename(filename)

    if extension and not safe_name.endswith(extension):
        safe_name += extension

    full_path = os.path.join(base_dir, safe_name)

    # If file exists, add number suffix
    if os.path.exists(full_path):
        name_part, ext_part = os.path.splitext(safe_name)
        counter = 1
        while True:
            new_name = f"{name_part}_{counter}{ext_part}"
            new_path = os.path.join(base_dir, new_name)
            if not os.path.exists(new_path):
                return new_path
            counter += 1

    return full_path