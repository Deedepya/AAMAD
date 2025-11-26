# Integration tests for document upload flow

import pytest
import uuid
import io
from database.models import User, Document, OnboardingTask, ComplianceRecord


@pytest.mark.integration
class TestDocumentUploadFlow:
    """Integration tests for complete document upload and processing flow"""
    
    def test_complete_document_upload_flow(self, test_client, db_session, sample_user_id, temp_upload_dir):
        """Test complete flow: upload -> database -> status check"""
        # Step 1: Create user
        user = User(
            id=uuid.UUID(sample_user_id),
            email="integration@example.com",
            first_name="Integration",
            last_name="Test"
        )
        db_session.add(user)
        db_session.commit()
        
        # Step 2: Upload document
        test_file = io.BytesIO(b"fake image content for integration test")
        test_file.name = "integration_test.jpg"
        
        upload_response = test_client.post(
            "/api/v1/documents/upload",
            files={"file": ("integration_test.jpg", test_file, "image/jpeg")},
            data={
                "document_type": "I9",
                "user_id": sample_user_id
            }
        )
        
        assert upload_response.status_code == 200
        upload_data = upload_response.json()
        document_id = upload_data["document_id"]
        
        # Step 3: Verify document in database
        document = db_session.query(Document).filter(
            Document.id == uuid.UUID(document_id)
        ).first()
        assert document is not None
        assert document.document_type == "I9"
        assert document.user_id == uuid.UUID(sample_user_id)
        assert document.status in ["uploaded", "processing", "verified"]
        
        # Step 4: Check onboarding status
        status_response = test_client.get(f"/api/v1/onboarding/{sample_user_id}/status")
        assert status_response.status_code == 200
        status_data = status_response.json()
        assert status_data["user_id"] == sample_user_id
    
    def test_document_upload_creates_user_if_missing(self, test_client, db_session, temp_upload_dir):
        """Test that upload creates user if it doesn't exist"""
        new_user_id = str(uuid.uuid4())
        
        test_file = io.BytesIO(b"test content")
        test_file.name = "test.jpg"
        
        response = test_client.post(
            "/api/v1/documents/upload",
            files={"file": ("test.jpg", test_file, "image/jpeg")},
            data={
                "document_type": "W4",
                "user_id": new_user_id
            }
        )
        
        assert response.status_code == 200
        
        # Verify user was created
        user = db_session.query(User).filter(
            User.id == uuid.UUID(new_user_id)
        ).first()
        assert user is not None
        assert user.email is not None


@pytest.mark.integration
class TestTaskManagementFlow:
    """Integration tests for task management flow"""
    
    def test_create_and_complete_task_flow(self, test_client, db_session, sample_user_id):
        """Test creating tasks and completing them"""
        # Create user
        user = User(
            id=uuid.UUID(sample_user_id),
            email="tasktest@example.com"
        )
        db_session.add(user)
        db_session.commit()
        
        # Manually create task (API doesn't have create endpoint yet)
        task = OnboardingTask(
            id=uuid.uuid4(),
            user_id=uuid.UUID(sample_user_id),
            task_name="Integration Test Task",
            status="pending"
        )
        db_session.add(task)
        db_session.commit()
        task_id = str(task.id)
        
        # Get tasks
        get_response = test_client.get(f"/api/v1/tasks/{sample_user_id}")
        assert get_response.status_code == 200
        tasks = get_response.json()
        assert len(tasks) == 1
        
        # Complete task
        complete_response = test_client.post(f"/api/v1/tasks/{task_id}/complete")
        assert complete_response.status_code == 200
        
        # Verify task is completed
        db_session.refresh(task)
        assert task.status == "completed"
        assert task.completed_at is not None
        
        # Check status reflects completion
        status_response = test_client.get(f"/api/v1/onboarding/{sample_user_id}/status")
        assert status_response.status_code == 200
        status_data = status_response.json()
        assert status_data["tasks_completed"] == 1
        assert status_data["overall_progress"] == 100.0

