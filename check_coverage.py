#!/usr/bin/env python3
"""
Coverage test for Forsong project
Checks which parts of the codebase are tested
"""

import sys
import os
import inspect
from pathlib import Path

class CoverageChecker:
    """Simple coverage checker for Forsong"""

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent
        self.coverage_data = {}

    def analyze_coverage(self):
        """Analyze test coverage"""
        print("📊 Analyzing code coverage...")

        # Find all Python files
        python_files = []
        for root, dirs, files in os.walk('src'):
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    python_files.append(os.path.join(root, file))

        # Find all test files
        test_files = []
        for file in os.listdir('.'):
            if file.startswith('test_') and file.endswith('.py'):
                test_files.append(file)

        coverage = {}

        for py_file in python_files:
            relative_path = py_file.replace('src/', '')
            coverage[relative_path] = self.check_file_coverage(py_file, test_files)

        self.coverage_data = coverage
        return coverage

    def check_file_coverage(self, py_file, test_files):
        """Check if a file has corresponding tests"""
        # Extract module name
        module_name = py_file.replace('src/', '').replace('.py', '').replace('/', '.')

        # Look for test files that might test this module
        possible_tests = [
            f"test_{module_name.split('.')[-1]}.py",
            f"test_{module_name.replace('.', '_')}.py",
            "test_project.py",
            "test_integration.py"
        ]

        has_tests = any(test in test_files for test in possible_tests)

        # Check if module is imported in tests
        tested = False
        for test_file in test_files:
            try:
                with open(test_file, 'r') as f:
                    content = f.read()
                    if f"src.{module_name}" in content or module_name in content:
                        tested = True
                        break
            except:
                pass

        return {
            'has_test_file': has_tests,
            'is_tested': tested,
            'module': module_name
        }

    def generate_report(self):
        """Generate coverage report"""
        if not self.coverage_data:
            self.analyze_coverage()

        print("\n📈 Coverage Report")
        print("="*50)

        total_files = len(self.coverage_data)
        tested_files = sum(1 for data in self.coverage_data.values() if data['is_tested'])

        print(f"Total Python files: {total_files}")
        print(f"Files with tests: {tested_files}")
        print(".1f")

        print("\nDetailed coverage:")
        for file_path, data in sorted(self.coverage_data.items()):
            status = "✅" if data['is_tested'] else "❌"
            test_status = "has test file" if data['has_test_file'] else "no test file"
            print(f"{status} {file_path} ({test_status})")

        return tested_files / total_files if total_files > 0 else 0

def main():
    """Main entry point"""
    checker = CoverageChecker()
    coverage_ratio = checker.generate_report()

    if coverage_ratio >= 0.4:
        print("🎉 Basic test coverage achieved!")
        return 0
    else:
        print("⚠️ Add more tests to reach minimum coverage")
        return 1

if __name__ == "__main__":
    sys.exit(main())