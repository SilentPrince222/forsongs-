"""Cover image downloader and generator."""

import os
from pathlib import Path
from typing import Optional
import requests
from PIL import Image, ImageDraw, ImageFont


class CoverDownloader:
    """Downloads and generates cover images for tracks."""

    @staticmethod
    def download_cover(url: str, output_path: Path | str) -> bool:
        """Download cover image from URL and save to file."""
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(response.content)
            Image.open(output_path).verify()
            return True
        except Exception:
            return False

    @staticmethod
    def generate_text_cover(
        text: str,
        output_path: Path | str,
        size: tuple[int, int] = (800, 800),
        background_color: tuple[int, int, int] = (30, 30, 50),
        text_color: tuple[int, int, int] = (255, 255, 255),
    ) -> bool:
        """Generate a simple text-based cover image."""
        try:
            img = Image.new("RGB", size, background_color)
            draw = ImageDraw.Draw(img)
            font = CoverDownloader._get_font()
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (size[0] - text_width) // 2
            y = (size[1] - text_height) // 2
            draw.text((x, y), text, font=font, fill=text_color)
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(output_path, "JPEG", quality=90)
            return True
        except ImportError:
            return False
        except Exception:
            return False

    @staticmethod
    def _get_font():
        """Get available font."""
        try:
            from PIL import ImageFont
            possible_fonts = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
            ]
            for fpath in possible_fonts:
                if Path(fpath).exists():
                    return ImageFont.truetype(fpath, 48)
            return ImageFont.load_default()
        except Exception:
            from PIL import ImageFont
            return ImageFont.load_default()
