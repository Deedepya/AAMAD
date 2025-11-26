# Database Models
# This file defines SQLAlchemy models for the onboarding system
# Reference: SAD Section 7.3 (Database Architecture)

from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Date, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import uuid

Base = declarative_base()


class User(Base):
    """User model for employee accounts"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    role = Column(String(50), default="new_hire")  # new_hire, hr_admin, manager
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    onboarding_tasks = relationship("OnboardingTask", back_populates="user", cascade="all, delete-orphan")
    compliance_records = relationship("ComplianceRecord", back_populates="user", cascade="all, delete-orphan")


class Document(Base):
    """Document model for uploaded documents"""
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    document_type = Column(String(50), nullable=False)  # I9, W4, ID, PASSPORT, etc.
    file_path = Column(String(500), nullable=False)  # S3 path or local path
    status = Column(String(50), default="uploaded", nullable=False)  # uploaded, processing, verified, rejected
    extracted_data = Column(JSON)  # OCR results and extracted fields
    confidence_scores = Column(JSON)  # Confidence scores for extracted fields
    validation_status = Column(String(50))  # valid, invalid, needs-review
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="documents")
    compliance_records = relationship("ComplianceRecord", back_populates="document", cascade="all, delete-orphan")


class OnboardingTask(Base):
    """Onboarding task model for task tracking"""
    __tablename__ = "onboarding_tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    task_name = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="pending", nullable=False)  # pending, in_progress, completed, failed
    due_date = Column(Date)
    completed_at = Column(DateTime)
    priority = Column(String(20), default="medium")  # low, medium, high
    task_metadata = Column(JSON)  # Additional task-specific data (renamed from metadata - reserved in SQLAlchemy)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="onboarding_tasks")


class ComplianceRecord(Base):
    """Compliance record model for compliance verification results"""
    __tablename__ = "compliance_records"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    compliance_type = Column(String(50), nullable=False)  # I9, W4, etc.
    status = Column(String(50), nullable=False)  # compliant, non_compliant, needs_review
    audit_log = Column(JSON, nullable=False)  # Compliance check details
    missing_documents = Column(JSON)  # List of missing required documents
    verified_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="compliance_records")
    document = relationship("Document", back_populates="compliance_records")


class AgentLog(Base):
    """Agent execution log model for audit trail"""
    __tablename__ = "agent_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id = Column(UUID(as_uuid=True), nullable=False, index=True)  # Links related agent executions
    agent_name = Column(String(100), nullable=False, index=True)
    task_name = Column(String(200), nullable=False)
    status = Column(String(50), nullable=False)  # success, failed, in_progress
    input_data = Column(JSON)  # Input to agent/task
    output_data = Column(JSON)  # Output from agent/task
    error_message = Column(Text)
    execution_time_ms = Column(Integer)  # Execution time in milliseconds
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

