#!/usr/bin/env python3
"""
Automatic testing and documentation system for Forsong project
Runs after each update to check for bugs and document changes
"""

import sys
import os
import subprocess
import json
from pathlib import Path
from datetime import datetime
import hashlib

class ForsongQualityChecker:
    """Automated quality checker for Forsong project"""

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent
        self.changelog_path = self.project_root / "CHANGELOG.md"
        self.test_results = {}
        self.changes_detected = []

    def run_all_checks(self):
        """Run all quality checks"""
        print("🔍 Running Forsong Quality Checks...\n")

        checks = [
            self.check_code_syntax,
            self.check_imports,
            self.run_unit_tests,
            self.run_integration_tests,
            self.check_coverage,
            self.check_architecture_compliance,
            self.detect_code_changes,
            self.update_documentation
        ]

        results = []
        for check in checks:
            try:
                result = check()
                results.append(result)
                status = "✅" if result["passed"] else "❌"
                print(f"{status} {result['name']}: {result['message']}")
            except Exception as e:
                results.append({
                    "name": check.__name__,
                    "passed": False,
                    "message": f"Check failed: {e}"
                })
                print(f"❌ {check.__name__}: Check failed: {e}")

        return results

    def check_code_syntax(self):
        """Check Python syntax in all .py files"""
        print("Checking Python syntax...")

        # Only check files in the new architecture layers
        layers_to_check = ['domain', 'application', 'infrastructure', 'presentation', 'shared']

        python_files = []
        for layer in layers_to_check:
            layer_path = os.path.join('src', layer)
            if os.path.exists(layer_path):
                for root, dirs, files in os.walk(layer_path):
                    for file in files:
                        if file.endswith('.py') and not file.startswith('__'):
                            python_files.append(os.path.join(root, file))

        # Also check root level files
        root_files = ['main.py', 'quality_check.py', 'test_project.py', 'test_integration.py']
        for file in root_files:
            if os.path.exists(file):
                python_files.append(file)

        errors = []
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    compile(f.read(), py_file, 'exec')
            except SyntaxError as e:
                errors.append(f"{py_file}: {e}")
                print(f"  ❌ Syntax error in {py_file}: {e}")
            except Exception as e:
                errors.append(f"{py_file}: {e}")
                print(f"  ❌ Error in {py_file}: {e}")

        return {
            "name": "Syntax Check",
            "passed": len(errors) == 0,
            "message": f"Found {len(errors)} syntax errors" if errors else "All files syntax OK",
            "details": errors
        }

    def check_imports(self):
        """Check that all imports work"""
        print("Checking imports...")

        # Change to project root for imports
        original_cwd = os.getcwd()
        os.chdir(self.project_root)

        try:
            # Test domain imports
            from src.domain import Track, TrackRepository, SearchCommand
            from src.application.event_bus import event_bus
            from src.shared.utils import sanitize_filename, format_duration

            # Test infrastructure (without dependencies)
            # Just check files exist
            infra_files = [
                'src/infrastructure/database/db.py',
                'src/infrastructure/sources/base_parser.py',
                'src/infrastructure/http/http_client.py'
            ]

            missing = [f for f in infra_files if not os.path.exists(f)]
            if missing:
                return {
                    "name": "Import Check",
                    "passed": False,
                    "message": f"Missing infrastructure files: {missing}"
                }

            return {
                "name": "Import Check",
                "passed": True,
                "message": "All core imports working"
            }

        except ImportError as e:
            return {
                "name": "Import Check",
                "passed": False,
                "message": f"Import error: {e}"
            }
        finally:
            os.chdir(original_cwd)

    def run_unit_tests(self):
        """Run unit tests"""
        print("Running unit tests...")

        try:
            result = subprocess.run([
                sys.executable, 'test_project.py'
            ], cwd=self.project_root, capture_output=True, text=True, timeout=30)

            return {
                "name": "Unit Tests",
                "passed": result.returncode == 0,
                "message": "Unit tests passed" if result.returncode == 0 else "Unit tests failed",
                "details": result.stdout + result.stderr
            }

        except subprocess.TimeoutExpired:
            return {
                "name": "Unit Tests",
                "passed": False,
                "message": "Unit tests timed out"
            }

    def run_integration_tests(self):
        """Run integration tests"""
        print("Running integration tests...")

        try:
            result = subprocess.run([
                sys.executable, 'test_integration.py'
            ], cwd=self.project_root, capture_output=True, text=True, timeout=60)

            return {
                "name": "Integration Tests",
                "passed": result.returncode == 0,
                "message": "Integration tests passed" if result.returncode == 0 else "Integration tests failed",
                "details": result.stdout + result.stderr
            }

        except subprocess.TimeoutExpired:
            return {
                "name": "Integration Tests",
                "passed": False,
                "message": "Integration tests timed out"
            }

    def check_coverage(self):
        """Check test coverage"""
        print("Checking test coverage...")

        try:
            result = subprocess.run([
                sys.executable, 'check_coverage.py'
            ], cwd=self.project_root, capture_output=True, text=True, timeout=30)

            coverage_good = result.returncode == 0

            return {
                "name": "Coverage Check",
                "passed": coverage_good,
                "message": "Coverage acceptable" if coverage_good else "Coverage needs improvement",
                "details": result.stdout + result.stderr
            }

        except subprocess.TimeoutExpired:
            return {
                "name": "Coverage Check",
                "passed": False,
                "message": "Coverage check timed out"
            }

    def check_architecture_compliance(self):
        """Check that architecture rules are followed"""
        print("Checking architecture compliance...")

        violations = []

        # Check domain doesn't import infrastructure
        try:
            with open('src/domain/entities.py', 'r') as f:
                content = f.read()
                if 'infrastructure' in content or 'peewee' in content:
                    violations.append("Domain layer imports infrastructure")
        except FileNotFoundError:
            violations.append("Domain entities.py not found")

        # Check application doesn't import presentation
        try:
            with open('src/application/event_bus.py', 'r') as f:
                content = f.read()
                if 'presentation' in content or 'gui' in content:
                    violations.append("Application layer imports presentation")
        except FileNotFoundError:
            violations.append("Application event_bus.py not found")

        return {
            "name": "Architecture Check",
            "passed": len(violations) == 0,
            "message": f"Architecture violations: {len(violations)}",
            "details": violations
        }

    def detect_code_changes(self):
        """Detect what files have changed since last check"""
        print("Detecting code changes...")

        changes = []
        hash_file = self.project_root / ".code_hashes.json"

        # Load previous hashes
        previous_hashes = {}
        if hash_file.exists():
            try:
                with open(hash_file, 'r') as f:
                    previous_hashes = json.load(f)
            except:
                pass

        # Calculate current hashes
        current_hashes = {}
        for root, dirs, files in os.walk('src'):
            for file in files:
                if file.endswith(('.py', '.md', '.txt')):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'rb') as f:
                            content = f.read()
                            current_hashes[path] = hashlib.md5(content).hexdigest()
                    except:
                        pass

        # Find changes
        for path, new_hash in current_hashes.items():
            if path not in previous_hashes:
                changes.append(f"NEW: {path}")
            elif previous_hashes[path] != new_hash:
                changes.append(f"MODIFIED: {path}")

        for path in previous_hashes:
            if path not in current_hashes:
                changes.append(f"DELETED: {path}")

        # Save current hashes
        with open(hash_file, 'w') as f:
            json.dump(current_hashes, f, indent=2)

        self.changes_detected = changes

        return {
            "name": "Change Detection",
            "passed": True,
            "message": f"Detected {len(changes)} file changes",
            "details": changes
        }

    def update_documentation(self):
        """Update CHANGELOG.md with detected changes"""
        print("Updating documentation...")

        if not self.changes_detected:
            return {
                "name": "Documentation Update",
                "passed": True,
                "message": "No changes to document"
            }

        # Read existing changelog
        changelog_content = ""
        if self.changelog_path.exists():
            with open(self.changelog_path, 'r', encoding='utf-8') as f:
                changelog_content = f.read()

        # Create new entry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = f"\n## {timestamp} - Automated Update\n\n"

        if self.changes_detected:
            new_entry += "### File Changes:\n"
            for change in self.changes_detected:
                new_entry += f"- {change}\n"
            new_entry += "\n"

        # Add test results
        if self.test_results:
            new_entry += "### Quality Check Results:\n"
            for result in self.test_results:
                status = "✅" if result.get("passed", False) else "❌"
                new_entry += f"- {status} {result['name']}: {result['message']}\n"
            new_entry += "\n"

        # Update changelog
        updated_content = new_entry + changelog_content

        with open(self.changelog_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        return {
            "name": "Documentation Update",
            "passed": True,
            "message": f"Updated CHANGELOG.md with {len(self.changes_detected)} changes"
        }

def main():
    """Main entry point"""
    checker = ForsongQualityChecker()
    results = checker.run_all_checks()

    # Store results for documentation
    checker.test_results = results

    # Final summary
    print("\n" + "="*50)
    print("QUALITY CHECK SUMMARY")
    print("="*50)

    passed = sum(1 for r in results if r["passed"])
    total = len(results)

    print(f"Tests passed: {passed}/{total}")

    if all(r["passed"] for r in results):
        print("🎉 All quality checks passed!")
        return 0
    else:
        print("⚠️ Some quality checks failed!")
        print("\nFailed checks:")
        for result in results:
            if not result["passed"]:
                print(f"  - {result['name']}: {result['message']}")
        return 1

if __name__ == "__main__":
    sys.exit(main())