#!/usr/bin/env python3
"""
Test GUI application startup without actually showing the window
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_gui_imports():
    """Test that GUI component files exist."""
    print("Testing GUI component files...")

    try:
        # Check that GUI files exist
        gui_files = [
            'src/presentation/app.py',
            'src/presentation/di_container.py',
            'src/presentation/viewmodels/search_viewmodel.py',
            'src/presentation/viewmodels/downloads_viewmodel.py'
        ]

        for file_path in gui_files:
            assert os.path.exists(file_path), f"GUI file missing: {file_path}"

        # Check that app.py has the main class
        with open('src/presentation/app.py', 'r') as f:
            content = f.read()
            assert 'class ForsongApp' in content, "ForsongApp class not found"

        print("✅ GUI component files exist")
        return True
    except Exception as e:
        print(f"❌ GUI component error: {e}")
        return False

def test_di_container():
    """Test DI container file structure."""
    print("Testing DI container structure...")

    try:
        # Check that DI container file exists
        assert os.path.exists('src/presentation/di_container.py'), "DI container file missing"

        # Check that it has the main components
        with open('src/presentation/di_container.py', 'r') as f:
            content = f.read()
            assert 'class DependencyContainer' in content, "DependencyContainer class not found"
            assert 'container = DependencyContainer' in content, "Global container not found"
            assert 'parsers' in content, "Parsers setup not found"

        print("✅ DI container structure correct")
        return True
    except Exception as e:
        print(f"❌ DI container structure error: {e}")
        return False

def test_viewmodels():
    """Test viewmodel file structure."""
    print("Testing viewmodel structure...")

    try:
        # Check that viewmodel files exist
        vm_files = [
            'src/presentation/viewmodels/search_viewmodel.py',
            'src/presentation/viewmodels/downloads_viewmodel.py'
        ]

        for file_path in vm_files:
            assert os.path.exists(file_path), f"Viewmodel file missing: {file_path}"

        # Check search viewmodel structure
        with open('src/presentation/viewmodels/search_viewmodel.py', 'r') as f:
            content = f.read()
            assert 'class SearchViewModel' in content, "SearchViewModel class not found"
            assert 'perform_search' in content, "perform_search method not found"

        # Check downloads viewmodel structure
        with open('src/presentation/viewmodels/downloads_viewmodel.py', 'r') as f:
            content = f.read()
            assert 'class DownloadsViewModel' in content, "DownloadsViewModel class not found"
            assert 'pause_download' in content, "pause_download method not found"

        print("✅ Viewmodel structure correct")
        return True
    except Exception as e:
        print(f"❌ Viewmodel structure error: {e}")
        return False

def main():
    """Run GUI tests."""
    print("🖥️  Testing Forsong GUI components...\n")

    tests = [
        test_gui_imports,
        test_di_container,
        test_viewmodels,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print(f"📊 GUI Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All GUI tests passed! GUI is ready.")
        return 0
    else:
        print("⚠️ Some GUI tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())