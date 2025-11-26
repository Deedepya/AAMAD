# Tests for API endpoints

import pytest
import uuid
import io
from pathlib import Path
from database.models import User, Document, OnboardingTask


@pytest.mark.api
class TestHealthEndpoint:
    """Tests for health check endpoint"""
    
    def test_health_check(self, test_client):
        """Test health check endpoint"""
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


@pytest.mark.api
class TestDocumentUploadEndpoint:
    """Tests for document upload endpoint"""
    
    def test_upload_document_success(self, test_client, db_session, sample_user_id, temp_upload_dir):
        """Test successful document upload"""
        # Create user first
        user = User(
            id=uuid.UUID(sample_user_id),
            email="test@example.com",
            first_name="Test",
            last_name="User"
        )
        db_session.add(user)
        db_session.commit()
        
        # Create test image file
        test_file = io.BytesIO(b"fake image content")
        test_file.name = "test_document.jpg"
        
        response = test_client.post(
            "/api/v1/documents/upload",
            files={"file": ("test_document.jpg", test_file, "image/jpeg")},
            data={
                "document_type": "I9",
                "user_id": sample_user_id
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "document_id" in data
        assert data["status"] == "uploaded"
        assert "message" in data
        
        # Verify document in database
        document = db_session.query(Document).filter(
            Document.id == uuid.UUID(data["document_id"])
        ).first()
        assert document is not None
        assert document.document_type == "I9"
        assert document.user_id == uuid.UUID(sample_user_id)
    
    def test_upload_document_missing_file(self, test_client):
        """Test upload without file"""
        response = test_client.post(
            "/api/v1/documents/upload",
            data={
                "document_type": "I9",
                "user_id": str(uuid.uuid4())
            }
        )
        assert response.status_code == 422  # Validation error
    
    def test_upload_document_invalid_type(self, test_client, sample_user_id):
        """Test upload with invalid document type"""
        test_file = io.BytesIO(b"fake content")
        test_file.name = "test.jpg"
        
        response = test_client.post(
            "/api/v1/documents/upload",
            files={"file": ("test.jpg", test_file, "image/jpeg")},
            data={
                "document_type": "INVALID",
                "user_id": sample_user_id
            }
        )
        assert response.status_code == 400
        assert "Invalid document type" in response.json()["detail"]
    
    def test_upload_document_file_too_large(self, test_client, sample_user_id):
        """Test upload with file exceeding size limit"""
        # Create file larger than 10MB
        large_content = b"x" * (11 * 1024 * 1024)  # 11MB
        test_file = io.BytesIO(large_content)
        test_file.name = "large_file.jpg"
        
        response = test_client.post(
            "/api/v1/documents/upload",
            files={"file": ("large_file.jpg", test_file, "image/jpeg")},
            data={
                "document_type": "I9",
                "user_id": sample_user_id
            }
        )
        assert response.status_code == 400
        assert "exceeds maximum" in response.json()["detail"]


@pytest.mark.api
class TestOnboardingStatusEndpoint:
    """Tests for onboarding status endpoint"""
    
    def test_get_onboarding_status(self, test_client, db_session, sample_user_id):
        """Test getting onboarding status"""
        # Create user
        user = User(
            id=uuid.UUID(sample_user_id),
            email="test@example.com"
        )
        db_session.add(user)
        db_session.commit()
        
        # Create tasks
        task1 = OnboardingTask(
            id=uuid.uuid4(),
            user_id=uuid.UUID(sample_user_id),
            task_name="Task 1",
            status="completed"
        )
        task2 = OnboardingTask(
            id=uuid.uuid4(),
            user_id=uuid.UUID(sample_user_id),
            task_name="Task 2",
            status="pending"
        )
        db_session.add_all([task1, task2])
        db_session.commit()
        
        response = test_client.get(f"/api/v1/onboarding/{sample_user_id}/status")
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == sample_user_id
        assert data["tasks_total"] == 2
        assert data["tasks_completed"] == 1
        assert data["overall_progress"] == 50.0
        assert data["status"] == "in_progress"
    
    def test_get_onboarding_status_user_not_found(self, test_client):
        """Test getting status for non-existent user"""
        fake_user_id = str(uuid.uuid4())
        response = test_client.get(f"/api/v1/onboarding/{fake_user_id}/status")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


@pytest.mark.api
class TestTasksEndpoint:
    """Tests for tasks endpoint"""
    
    def test_get_tasks(self, test_client, db_session, sample_user_id):
        """Test getting user tasks"""
        # Create user
        user = User(
            id=uuid.UUID(sample_user_id),
            email="test@example.com"
        )
        db_session.add(user)
        db_session.commit()
        
        # Create tasks
        task = OnboardingTask(
            id=uuid.uuid4(),
            user_id=uuid.UUID(sample_user_id),
            task_name="Complete I-9",
            status="pending"
        )
        db_session.add(task)
        db_session.commit()
        
        response = test_client.get(f"/api/v1/tasks/{sample_user_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["task_name"] == "Complete I-9"
        assert data[0]["status"] == "pending"
    
    def test_complete_task(self, test_client, db_session, sample_user_id):
        """Test completing a task"""
        # Create user
        user = User(
            id=uuid.UUID(sample_user_id),
            email="test@example.com"
        )
        db_session.add(user)
        db_session.commit()
        
        # Create task
        task = OnboardingTask(
            id=uuid.uuid4(),
            user_id=uuid.UUID(sample_user_id),
            task_name="Test Task",
            status="pending"
        )
        db_session.add(task)
        db_session.commit()
        task_id = str(task.id)
        
        response = test_client.post(f"/api/v1/tasks/{task_id}/complete")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
        # Verify task is completed
        db_session.refresh(task)
        assert task.status == "completed"
        assert task.completed_at is not None
    
    def test_complete_task_not_found(self, test_client):
        """Test completing non-existent task"""
        fake_task_id = str(uuid.uuid4())
        response = test_client.post(f"/api/v1/tasks/{fake_task_id}/complete")
        assert response.status_code == 404

