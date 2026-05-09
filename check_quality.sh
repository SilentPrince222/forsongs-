#!/bin/bash
# Forsong Quality Assurance Runner
# Run this script after any code changes to ensure quality

echo "🚀 Running Forsong Quality Assurance..."
echo "========================================"

# Check if we're in the right directory
if [ ! -f "quality_check.py" ]; then
    echo "❌ Error: quality_check.py not found. Run from project root."
    exit 1
fi

# Run quality checks
if [ -d "venv" ]; then
    source venv/bin/activate
fi
python3 quality_check.py
exit_code=$?

echo ""
echo "========================================"

if [ $exit_code -eq 0 ]; then
    echo "✅ Quality checks passed! Ready to commit."
    echo ""
    echo "Next steps:"
    echo "  git add ."
    echo "  git commit -m 'Your commit message'"
    echo "  git push"
else
    echo "❌ Quality checks failed! Fix issues before committing."
    echo ""
    echo "Common fixes:"
    echo "  - Run tests: python3 test_project.py"
    echo "  - Check syntax: python3 -m py_compile src/**/*.py"
    echo "  - Fix imports: Check error messages above"
fi

exit $exit_code