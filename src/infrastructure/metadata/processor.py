"""Metadata processor for reading and writing audio metadata (ID3 tags)."""

import io
from pathlib import Path
from typing import Optional, Dict, Any

try:
    from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TCON, TYER, TRCK
    from mutagen.mp3 import MP3
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False


class MetadataProcessor:
    """Handler for reading and writing audio metadata."""

    def __init__(self) -> None:
        if not MUTAGEN_AVAILABLE:
            raise ImportError("mutagen library is required")

    def add_metadata(
        self,
        filepath: Path | str,
        track_info: Dict[str, Any],
    ) -> bool:
        """Add or update ID3 tags in an MP3 file."""
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                return False
            audio = MP3(filepath, ID3=ID3)
            if audio.tags is None:
                audio.add_tags()
            tags = audio.tags
            if "title" in track_info:
                tags.add(TIT2(encoding=3, text=track_info["title"]))
            if "artist" in track_info:
                tags.add(TPE1(encoding=3, text=track_info["artist"]))
            if "album" in track_info:
                tags.add(TALB(encoding=3, text=track_info["album"]))
            if "genre" in track_info:
                tags.add(TCON(encoding=3, text=track_info["genre"]))
            if "year" in track_info:
                tags.add(TYER(encoding=3, text=str(track_info["year"])))
            if "track_number" in track_info:
                tags.add(TRCK(encoding=3, text=str(track_info["track_number"])))
            audio.save(v2_version=3)
            return True
        except Exception:
            return False

    def embed_cover(self, filepath: Path | str, cover_image: Path | bytes) -> bool:
        """Embed cover art into audio file."""
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                return False
            audio = MP3(filepath, ID3=ID3)
            if audio.tags is None:
                audio.add_tags()
            tags = audio.tags
            self._add_cover_art(tags, cover_image)
            audio.save(v2_version=3)
            return True
        except Exception:
            return False

    def _add_cover_art(self, tags: Any, cover_image: Path | bytes) -> None:
        """Add APIC (cover art) frame to tags."""
        if isinstance(cover_image, Path):
            with open(cover_image, "rb") as img_file:
                img_data = img_file.read()
        else:
            img_data = cover_image
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(img_data))
            mime_type = "image/jpeg" if img.format == "JPEG" else "image/png"
        except Exception:
            mime_type = "image/jpeg"
        tags.add(
            APIC(
                encoding=3,
                mime=mime_type,
                type=3,
                desc="Cover",
                data=img_data,
            )
        )

    def extract_metadata(self, filepath: Path | str) -> Dict[str, Any]:
        """Extract metadata from audio file."""
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                return {}
            audio = MP3(filepath, ID3=ID3)
            if audio.tags is None:
                return {}
            return {
                "title": self._get_text_tag(audio.tags, "TIT2"),
                "artist": self._get_text_tag(audio.tags, "TPE1"),
                "album": self._get_text_tag(audio.tags, "TALB"),
                "genre": self._get_text_tag(audio.tags, "TCON"),
                "year": self._get_int_tag(audio.tags, "TYER"),
                "duration": int(audio.info.length) if audio.info else 0,
                "bitrate": audio.info.bitrate // 1000 if audio.info else 0,
            }
        except Exception:
            return {}

    def _get_text_tag(self, tags: Any, frame_id: str) -> Optional[str]:
        frame = tags.get(frame_id)
        if frame and hasattr(frame, "text"):
            return str(frame.text[0]) if frame.text else None
        return None

    def _get_int_tag(self, tags: Any, frame_id: str) -> Optional[int]:
        frame = tags.get(frame_id)
        if frame and hasattr(frame, "text"):
            try:
                return int(frame.text[0])
            except (ValueError, IndexError):
                pass
        return None
