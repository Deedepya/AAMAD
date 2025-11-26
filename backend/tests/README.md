# Backend Test Suite

## Overview

Comprehensive test suite for the Automated Employee Onboarding Workflow backend, covering database models, API endpoints, tools, and integration flows.

## Test Files

### 1. `test_database_models.py`
Tests for all database models:
- ✅ User model creation and relationships
- ✅ Document model with status transitions
- ✅ OnboardingTask model and completion
- ✅ ComplianceRecord model
- ✅ AgentLog model

**Run:** `pytest tests/test_database_models.py -v -m database`

### 2. `test_api_endpoints.py`
Tests for all API endpoints:
- ✅ Health check endpoint
- ✅ Document upload (success, validation, errors)
- ✅ Onboarding status retrieval
- ✅ Task listing and completion
- ✅ Error handling (404, 400, 422)

**Run:** `pytest tests/test_api_endpoints.py -v -m api`

### 3. `test_tools.py`
Tests for CrewAI tools:
- ✅ OCR tool functionality
- ✅ Document validation tool
- ✅ Image processing tool
- ✅ Compliance validation (I-9, W-4, ID)
- ✅ Audit logging tool

**Run:** `pytest tests/test_tools.py -v -m tools`

### 4. `test_integration.py`
End-to-end integration tests:
- ✅ Complete document upload workflow
- ✅ Task management workflow
- ✅ User auto-creation
- ✅ Status tracking

**Run:** `pytest tests/test_integration.py -v -m integration`

## Quick Start

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt

# Or install minimal test dependencies
pip install pytest pytest-asyncio httpx fastapi sqlalchemy
```

### Run All Tests
```bash
cd backend
pytest tests/ -v
```

### Run by Category
```bash
# Database tests only
pytest tests/ -v -m database

# API tests only
pytest tests/ -v -m api

# Tool tests only
pytest tests/ -v -m tools

# Integration tests only
pytest tests/ -v -m integration
```

### Run Specific Test File
```bash
pytest tests/test_database_models.py -v
```

### Run Specific Test
```bash
pytest tests/test_database_models.py::TestUserModel::test_create_user -v
```

## Test Configuration

### Pytest Configuration (`pytest.ini`)
- Test discovery: `test_*.py` files
- Markers: `unit`, `integration`, `api`, `database`, `tools`
- Verbose output by default

### Fixtures (`conftest.py`)
- `db_session`: In-memory SQLite database session
- `test_client`: FastAPI test client with database override
- `sample_user_id`: Test user ID
- `sample_document_id`: Test document ID
- `temp_upload_dir`: Temporary upload directory

## Test Coverage

### Database Models
- ✅ User creation, relationships
- ✅ Document CRUD operations
- ✅ Task lifecycle management
- ✅ Compliance record creation
- ✅ Agent log tracking

### API Endpoints
- ✅ All endpoints tested
- ✅ Success cases
- ✅ Validation errors
- ✅ Not found errors
- ✅ File size limits
- ✅ Invalid input handling

### Tools
- ✅ OCR text extraction
- ✅ Document validation
- ✅ Image processing
- ✅ Compliance checks
- ✅ Audit logging

### Integration
- ✅ Complete workflows
- ✅ Error recovery
- ✅ Data persistence

## Known Limitations

1. **CrewAI Dependencies**: Some tests require CrewAI to be fully installed. Tests handle missing dependencies gracefully.

2. **OCR Tool**: Requires Tesseract OCR installed on system for full functionality. Tests work without it but OCR results will be empty.

3. **External Services**: Tests use mocks/stubs for:
   - Email notifications (SendGrid)
   - Push notifications (APNs)
   - HRIS integration (Workday/BambooHR)
   - Cloud storage (S3)

## Test Results

When running tests, you'll see:
- ✅ Passed tests
- ❌ Failed tests with error details
- ⚠️ Skipped tests (if dependencies missing)
- Test execution time
- Coverage report (if pytest-cov installed)

## Continuous Integration

To integrate with CI/CD:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    cd backend
    pip install -r requirements.txt
    pytest tests/ -v --cov=. --cov-report=xml
```

## Troubleshooting

### Import Errors
If you see import errors:
```bash
# Make sure you're in the backend directory
cd backend

# Install all dependencies
pip install -r requirements.txt
```

### Database Errors
Tests use in-memory SQLite by default. If you see database errors:
- Check that SQLAlchemy is installed
- Verify database URL in test environment

### Missing Dependencies
Some tests may skip if optional dependencies are missing:
- CrewAI (for crew execution tests)
- Tesseract OCR (for OCR tool tests)
- boto3 (for S3 storage tests)

These are handled gracefully - tests will skip or use mocks.

## Next Steps

1. **Add Coverage Reporting**:
   ```bash
   pip install pytest-cov
   pytest tests/ --cov=. --cov-report=html
   ```

2. **Add Performance Tests**: Test API response times

3. **Add Security Tests**: Test authentication and authorization

4. **Add Load Tests**: Test under concurrent load

