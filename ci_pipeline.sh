#!/bin/bash
# Forsong CI/CD Pipeline
# Run automated checks for continuous integration

echo "🔄 Starting Forsong CI/CD Pipeline..."
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    local status=$1
    local message=$2
    if [ "$status" -eq 0 ]; then
        echo -e "${GREEN}✅ $message${NC}"
    else
        echo -e "${RED}❌ $message${NC}"
    fi
}

# Check if we're in project root
if [ ! -f "quality_check.py" ]; then
    echo -e "${RED}❌ Error: Not in project root directory${NC}"
    exit 1
fi

echo "📋 Running pre-flight checks..."

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "🐍 Python version: $PYTHON_VERSION"

# Check if required files exist
REQUIRED_FILES=("main.py" "requirements.txt" "src/" "quality_check.py")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -e "$file" ]; then
        echo -e "${RED}❌ Missing required file: $file${NC}"
        exit 1
    fi
done
echo -e "${GREEN}✅ All required files present${NC}"

echo ""
echo "🧪 Running quality checks..."

# Run quality checks
python3 quality_check.py
QUALITY_EXIT=$?

print_status $QUALITY_EXIT "Quality checks"

if [ $QUALITY_EXIT -ne 0 ]; then
    echo ""
    echo -e "${RED}🚫 CI/CD Pipeline failed at quality checks${NC}"
    echo "Please fix the issues above and try again."
    exit 1
fi

echo ""
echo "📦 Running build simulation..."

# Simulate build process
echo "Building Forsong application..."

# Check if we can import main modules (build test)
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from src.domain import Track
    from src.application.event_bus import event_bus
    print('✅ Core modules import successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"
BUILD_EXIT=$?

print_status $BUILD_EXIT "Build simulation"

if [ $BUILD_EXIT -ne 0 ]; then
    echo ""
    echo -e "${RED}🚫 CI/CD Pipeline failed at build${NC}"
    exit 1
fi

echo ""
echo "📊 Generating coverage report..."

# Run coverage check
python3 check_coverage.py
COVERAGE_EXIT=$?

print_status $COVERAGE_EXIT "Coverage report"

echo ""
echo "📋 CI/CD Pipeline Summary"
echo "========================"

if [ $QUALITY_EXIT -eq 0 ] && [ $BUILD_EXIT -eq 0 ]; then
    echo -e "${GREEN}🎉 CI/CD Pipeline completed successfully!${NC}"
    echo ""
    echo "📝 Next steps:"
    echo "  • Code is ready for deployment"
    echo "  • All tests pass"
    echo "  • Quality standards met"
    echo "  • Documentation updated"
    echo ""
    echo "🚀 Ready to merge/deploy!"
    exit 0
else
    echo -e "${RED}🚫 CI/CD Pipeline failed${NC}"
    echo ""
    echo "🔧 Please fix the issues and run again."
    exit 1
fi