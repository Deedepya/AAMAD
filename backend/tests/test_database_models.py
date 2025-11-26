# Tests for database models

import pytest
import uuid
from datetime import datetime, date
from database.models import User, Document, OnboardingTask, ComplianceRecord, AgentLog


@pytest.mark.database
class TestUserModel:
    """Tests for User model"""
    
    def test_create_user(self, db_session):
        """Test creating a user"""
        user = User(
            id=uuid.uuid4(),
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            role="new_hire"
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.role == "new_hire"
        assert user.created_at is not None
    
    def test_user_relationships(self, db_session):
        """Test user relationships with documents and tasks"""
        user = User(
            id=uuid.uuid4(),
            email="test@example.com",
            first_name="John",
            last_name="Doe"
        )
        db_session.add(user)
        db_session.commit()
        
        # Create related document
        document = Document(
            id=uuid.uuid4(),
            user_id=user.id,
            document_type="I9",
            file_path="/test/path",
            status="uploaded"
        )
        db_session.add(document)
        db_session.commit()
        
        # Verify relationship
        assert len(user.documents) == 1
        assert user.documents[0].document_type == "I9"


@pytest.mark.database
class TestDocumentModel:
    """Tests for Document model"""
    
    def test_create_document(self, db_session, sample_user_id):
        """Test creating a document"""
        user = User(
            id=uuid.UUID(sample_user_id),
            email="test@example.com"
        )
        db_session.add(user)
        db_session.commit()
        
        document = Document(
            id=uuid.uuid4(),
            user_id=uuid.UUID(sample_user_id),
            document_type="I9",
            file_path="/test/path/document.pdf",
            status="uploaded"
        )
        db_session.add(document)
        db_session.commit()
        
        assert document.id is not None
        assert document.document_type == "I9"
        assert document.status == "uploaded"
        assert document.user_id == uuid.UUID(sample_user_id)
        assert document.created_at is not None
    
    def test_document_status_transitions(self, db_session, sample_user_id):
        """Test document status transitions"""
        user = User(
            id=uuid.UUID(sample_user_id),
            email="test@example.com"
        )
        db_session.add(user)
        db_session.commit()
        
        document = Document(
            id=uuid.uuid4(),
            user_id=uuid.UUID(sample_user_id),
            document_type="W4",
            file_path="/test/path",
            status="uploaded"
        )
        db_session.add(document)
        db_session.commit()
        
        # Transition to processing
        document.status = "processing"
        db_session.commit()
        assert document.status == "processing"
        
        # Transition to verified
        document.status = "verified"
        db_session.commit()
        assert document.status == "verified"


@pytest.mark.database
class TestOnboardingTaskModel:
    """Tests for OnboardingTask model"""
    
    def test_create_task(self, db_session, sample_user_id):
        """Test creating an onboarding task"""
        user = User(
            id=uuid.UUID(sample_user_id),
            email="test@example.com"
        )
        db_session.add(user)
        db_session.commit()
        
        task = OnboardingTask(
            id=uuid.uuid4(),
            user_id=uuid.UUID(sample_user_id),
            task_name="Complete I-9 Form",
            description="Fill out and submit I-9 form",
            status="pending",
            due_date=date(2024, 12, 31)
        )
        db_session.add(task)
        db_session.commit()
        
        assert task.id is not None
        assert task.task_name == "Complete I-9 Form"
        assert task.status == "pending"
        assert task.due_date == date(2024, 12, 31)
    
    def test_complete_task(self, db_session, sample_user_id):
        """Test completing a task"""
        user = User(
            id=uuid.UUID(sample_user_id),
            email="test@example.com"
        )
        db_session.add(user)
        db_session.commit()
        
        task = OnboardingTask(
            id=uuid.uuid4(),
            user_id=uuid.UUID(sample_user_id),
            task_name="Test Task",
            status="pending"
        )
        db_session.add(task)
        db_session.commit()
        
        # Complete task
        task.status = "completed"
        task.completed_at = datetime.utcnow()
        db_session.commit()
        
        assert task.status == "completed"
        assert task.completed_at is not None


@pytest.mark.database
class TestComplianceRecordModel:
    """Tests for ComplianceRecord model"""
    
    def test_create_compliance_record(self, db_session, sample_user_id):
        """Test creating a compliance record"""
        user = User(
            id=uuid.UUID(sample_user_id),
            email="test@example.com"
        )
        db_session.add(user)
        db_session.commit()
        
        document = Document(
            id=uuid.uuid4(),
            user_id=uuid.UUID(sample_user_id),
            document_type="I9",
            file_path="/test/path",
            status="verified"
        )
        db_session.add(document)
        db_session.commit()
        
        compliance = ComplianceRecord(
            id=uuid.uuid4(),
            user_id=uuid.UUID(sample_user_id),
            document_id=document.id,
            compliance_type="I9",
            status="compliant",
            audit_log={"validated_at": datetime.utcnow().isoformat()}
        )
        db_session.add(compliance)
        db_session.commit()
        
        assert compliance.id is not None
        assert compliance.compliance_type == "I9"
        assert compliance.status == "compliant"
        assert compliance.audit_log is not None


@pytest.mark.database
class TestAgentLogModel:
    """Tests for AgentLog model"""
    
    def test_create_agent_log(self, db_session):
        """Test creating an agent log"""
        execution_id = uuid.uuid4()
        agent_log = AgentLog(
            id=uuid.uuid4(),
            execution_id=execution_id,
            agent_name="document_processing_agent",
            task_name="process_document_upload",
            status="success",
            input_data={"file_path": "/test/path"},
            output_data={"extracted_text": "test"},
            execution_time_ms=1500
        )
        db_session.add(agent_log)
        db_session.commit()
        
        assert agent_log.id is not None
        assert agent_log.agent_name == "document_processing_agent"
        assert agent_log.status == "success"
        assert agent_log.execution_time_ms == 1500

