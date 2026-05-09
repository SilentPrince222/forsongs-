#!/usr/bin/env python3
"""
Simple test to check for bugs in Forsong project architecture
Tests imports and basic functionality without external dependencies
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_domain_imports():
    """Test domain layer imports"""
    print("Testing domain layer...")

    try:
        from src.domain.entities import Track, Playlist, TrackInfo
        from src.domain.interfaces import TrackRepository, MusicParser
        from src.domain.events import SearchCommand, DownloadStartedEvent
        from src.domain.exceptions import DomainError
        from src.domain.constants import SOURCES, LICENSES

        # Test entity creation
        track = Track(title="Test Track", artist="Test Artist", source="fma")
        assert track.title == "Test Track"
        assert track.artist == "Test Artist"

        track_info = TrackInfo.from_raw_data({"title": "Test", "artist": "Artist"})
        assert track_info.title == "Test"

        print("✅ Domain layer OK")
        return True

    except Exception as e:
        print(f"❌ Domain layer error: {e}")
        return False

def test_application_imports():
    """Test application layer imports"""
    print("Testing application layer...")

    try:
        from src.application.event_bus import EventBus
        from src.application.services.search_service import SearchService
        from src.application.services.download_service import DownloadService

        # Test event bus
        bus = EventBus()
        called = False
        def test_handler(event):
            nonlocal called
            called = True

        bus.subscribe("TestEvent", test_handler)
        bus.publish(type('TestEvent', (), {})())

        assert called, "Event handler not called"

        print("✅ Application layer OK")
        return True

    except Exception as e:
        print(f"❌ Application layer error: {e}")
        return False

def test_shared_imports():
    """Test shared utilities"""
    print("Testing shared utilities...")

    try:
        from src.shared.utils import sanitize_filename, format_duration
        from src.shared.validators import validate_track_title

        # Test utilities
        safe = sanitize_filename("test<file>")
        assert safe == "test_file", f"Expected 'test_file', got '{safe}'"

        # Test with trailing invalid chars
        safe2 = sanitize_filename("test<>")
        assert safe2 == "test", f"Expected 'test', got '{safe2}'"

        duration = format_duration(125)
        assert duration == "02:05", f"Expected '02:05', got '{duration}'"

        # Test validators
        error = validate_track_title("")
        assert error is not None, "Should return error for empty title"

        error = validate_track_title("Valid Title")
        assert error is None, "Should not return error for valid title"

        print("✅ Shared utilities OK")
        return True

    except Exception as e:
        print(f"❌ Shared utilities error: {e}")
        return False

def test_architecture_separation():
    """Test that layers don't have forbidden imports"""
    print("Testing architecture separation...")

    try:
        # Domain should not import infrastructure
        with open('src/domain/entities.py', 'r') as f:
            domain_source = f.read()

        forbidden_imports = ['infrastructure', 'peewee', 'aiohttp', 'requests']
        for forbidden in forbidden_imports:
            if forbidden in domain_source:
                raise AssertionError(f"Domain layer imports forbidden '{forbidden}'")

        # Check that domain only imports from typing, dataclasses, datetime
        lines = domain_source.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('from ') or line.startswith('import '):
                if not any(allowed in line for allowed in ['typing', 'dataclasses', 'datetime']):
                    print(f"⚠️ Domain imports: {line}")

        print("✅ Architecture separation OK")
        return True

    except Exception as e:
        print(f"❌ Architecture separation error: {e}")
        return False

def test_infrastructure_structure():
    """Test infrastructure layer structure"""
    print("Testing infrastructure structure...")

    try:
        # Check that infrastructure files exist (don't import due to missing deps)
        assert os.path.exists('src/infrastructure/sources/base_parser.py'), "base_parser.py missing"
        assert os.path.exists('src/infrastructure/database/models.py'), "models.py missing"

        # Check file contents without importing
        with open('src/infrastructure/sources/base_parser.py', 'r') as f:
            content = f.read()
            assert 'class BaseMusicParser' in content, "BaseMusicParser class missing"
            assert 'async def search' in content, "search method missing"

        print("✅ Infrastructure structure OK")
        return True

    except Exception as e:
        print(f"❌ Infrastructure structure error: {e}")
        return False

def find_code_issues():
    """Find common code issues"""
    print("Checking for code issues...")

    issues = []

    # Check for TODO comments
    for root, dirs, files in os.walk('src'):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'TODO' in content:
                            issues.append(f"TODO found in {path}")
                        if 'FIXME' in content:
                            issues.append(f"FIXME found in {path}")
                        if 'XXX' in content:
                            issues.append(f"XXX found in {path}")
                except:
                    pass

    if issues:
        print("⚠️ Code issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ No obvious code issues found")

    return issues

def main():
    """Run all tests"""
    print("🧪 Running Forsong project tests...\n")

    tests = [
        test_domain_imports,
        test_application_imports,
        test_shared_imports,
        test_architecture_separation,
        test_infrastructure_structure,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print(f"📊 Test Results: {passed}/{total} tests passed")

    issues = find_code_issues()

    if passed == total and not issues:
        print("🎉 All tests passed! Project looks good.")
        return 0
    else:
        print("⚠️ Some issues found. Check output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())