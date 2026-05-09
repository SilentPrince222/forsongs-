#!/usr/bin/env python3
"""
Demo script showing Forsong parser functionality
This demonstrates how the implemented parsers work
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

async def demo_parsers():
    """Demonstrate parser functionality"""
    print("🎵 Forsong Parser Demo")
    print("=" * 50)

    try:
        from src.application.services.parser_manager import ParserManager

        # Create mock parsers for demo (since we don't have real API keys)
        class MockParser:
            def __init__(self, source_name, demo_tracks):
                self.source_name = source_name
                self.demo_tracks = demo_tracks

            async def search(self, query, limit=20):
                # Return mock results for demo
                return [
                    track for track in self.demo_tracks
                    if query.lower() in track.title.lower() or query.lower() in track.artist.lower()
                ][:limit]

            async def get_download_url(self, track_id):
                return f"https://{self.source_name}.com/download/{track_id}"

        # Create demo tracks for each source
        demo_tracks = {
            'fma': [
                type('TrackInfo', (), {
                    'title': 'Electronic Groove',
                    'artist': 'FMA Artist',
                    'source': 'fma',
                    'license': 'cc-by',
                    'duration': 245
                })()
            ],
            'jamendo': [
                type('TrackInfo', (), {
                    'title': 'Jazz Piano',
                    'artist': 'Jamendo Musician',
                    'source': 'jamendo',
                    'license': 'cc-by-sa',
                    'duration': 312
                })()
            ],
            'archive': [
                type('TrackInfo', (), {
                    'title': 'Classical Symphony',
                    'artist': 'Public Domain Composer',
                    'source': 'archive',
                    'license': 'cc0',
                    'duration': 1800
                })()
            ],
            'pixabay': [
                type('TrackInfo', (), {
                    'title': 'Nature Sounds',
                    'artist': 'Pixabay',
                    'source': 'pixabay',
                    'license': 'cc0',
                    'duration': 120
                })()
            ],
            'bensound': [
                type('TrackInfo', (), {
                    'title': 'Corporate Background',
                    'artist': 'Bensound',
                    'source': 'bensound',
                    'license': 'cc-by',
                    'duration': 180
                })()
            ],
            'soundclick': [
                type('TrackInfo', (), {
                    'title': 'Indie Rock Track',
                    'artist': 'SoundClick Artist',
                    'source': 'soundclick',
                    'license': 'cc-by',
                    'duration': 198
                })()
            ]
        }

        # Create mock parsers
        parsers = [MockParser(source, tracks) for source, tracks in demo_tracks.items()]

        # Create parser manager
        manager = ParserManager(parsers)

        print("📋 Available sources:")
        sources = manager.get_available_sources()
        for source in sources:
            print(f"  • {source}")

        print(f"\n🔍 Total sources: {len(sources)}")

        # Demo search
        print("\n🔍 Demo search for 'jazz':")
        results = await manager.search_all_sources('jazz', limit=5)

        for i, track in enumerate(results, 1):
            print(f"  {i}. {track.title} by {track.artist} ({track.source}) - {track.duration}s")

        # Demo specific source search
        print("\n🎯 Search 'electronic' on FMA only:")
        fma_results = await manager.search_specific_source('fma', 'electronic', limit=3)

        for track in fma_results:
            print(f"  • {track.title} by {track.artist} ({track.license})")

        # Demo source info
        print("\nℹ️  Source information:")
        for source in sources:
            info = manager.get_source_info(source)
            if info:
                print(f"  • {source}: {info['parser_class']} - {'Available' if info['available'] else 'Unavailable'}")

        print("\n✅ Parser demo completed successfully!")
        print("🎵 All music sources are ready for integration!")

        return True

    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main demo function"""
    print("Starting Forsong parser demonstration...\n")

    success = asyncio.run(demo_parsers())

    if success:
        print("\n🎉 Demo completed successfully!")
        print("\nNext steps:")
        print("  • Configure API keys for real music sources")
        print("  • Implement GUI for search and download")
        print("  • Add database integration")
        print("  • Test with real APIs")
    else:
        print("\n❌ Demo failed!")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())