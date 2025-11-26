# Pytest configuration and fixtures

import pytest
import os
import tempfile
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Set test environment variables before imports
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["STORAGE_TYPE"] = "local"
os.environ["UPLOAD_DIR"] = str(Path(tempfile.gettempdir()) / "test_uploads")
os.environ["OPENAI_API_KEY"] = "test-key"  # Mock key for tests
os.environ["CREWAI_VERBOSE"] = "false"

from database import Base, get_db

# Import main app with error handling for missing dependencies
try:
    from main import app
except ImportError as e:
    # If dependencies are missing, create a minimal app for testing
    from fastapi import FastAPI
    app = FastAPI()
    import logging
    logging.warning(f"Could not import full app: {e}. Using minimal app for testing.")


@pytest.fixture(scope="function")
def db_session():
    """Create a test database session"""
    # Create in-memory SQLite database
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_client(db_session):
    """Create a test client with database override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    
    yield client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_id():
    """Sample user ID for testing"""
    return "550e8400-e29b-41d4-a716-446655440000"


@pytest.fixture
def sample_document_id():
    """Sample document ID for testing"""
    return "660e8400-e29b-41d4-a716-446655440001"


@pytest.fixture
def temp_upload_dir():
    """Create temporary upload directory"""
    upload_dir = Path(os.getenv("UPLOAD_DIR"))
    upload_dir.mkdir(parents=True, exist_ok=True)
    yield upload_dir
    # Cleanup (optional - can leave for inspection)
    # import shutil
    # if upload_dir.exists():
    #     shutil.rmtree(upload_dir)

