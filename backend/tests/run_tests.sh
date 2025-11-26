#!/bin/bash
# Test runner script for backend tests

echo "=========================================="
echo "Running Backend Tests"
echo "=========================================="

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Install test dependencies if needed
echo "Checking dependencies..."
python3 -m pip install -q pytest pytest-asyncio httpx fastapi sqlalchemy 2>&1 | grep -v "already satisfied" || true

# Run tests
echo ""
echo "Running database model tests..."
python3 -m pytest tests/test_database_models.py -v --tb=short -m database 2>&1 | head -50

echo ""
echo "Running API endpoint tests..."
python3 -m pytest tests/test_api_endpoints.py -v --tb=short -m api 2>&1 | head -50

echo ""
echo "Running tool tests..."
python3 -m pytest tests/test_tools.py -v --tb=short -m tools 2>&1 | head -50

echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo "Note: Some tests may require additional dependencies (CrewAI, Tesseract OCR)"
echo "For full test suite, install all requirements: pip install -r requirements.txt"
echo "=========================================="

