#!/usr/bin/env python3
"""Forsong - Legal Music Downloader main entry point (Clean Architecture)"""

import sys
from pathlib import Path

# Add project root to sys.path so 'src' package is importable
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from src.presentation.app import ForsongApp

    def main():
        print("Starting Forsong GUI application...")
        app = ForsongApp()
        app.run()

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"Import error: {e}")
    print("Install dependencies: pip install -r requirements.txt")
    print("Required: customtkinter, peewee, aiohttp, mutagen, pillow")
    input("Press Enter to exit...")
except Exception as e:
    print(f"Startup error: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")
except Exception as e:
    print(f"Startup error: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")