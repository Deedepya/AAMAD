# FastAPI Application
# Main entry point for the Automated Employee Onboarding Workflow backend

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
import os
import uuid
import logging
import tempfile
from pathlib import Path
from datetime import datetime

from database import get_db, init_db, User, Document, OnboardingTask, ComplianceRecord, AgentLog
from crew.crew_config import get_crew
from utils.storage import get_storage_manager
from pydantic import BaseModel, EmailStr
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Onboarding Workflow API",
    description="Automated Employee Onboarding Workflow - CrewAI Backend",
    version="1.0.0"
)

# CORS middleware for iOS app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify iOS app origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and crew on application startup"""
    try:
        init_db()
        logger.info("Database initialized")
        
        # Pre-load crew configuration
        get_crew()
        logger.info("CrewAI crew initialized")
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise


# Pydantic models for request/response
class DocumentUploadResponse(BaseModel):
    document_id: str
    status: str
    message: str


class OnboardingStatusResponse(BaseModel):
    user_id: str
    overall_progress: float
    tasks_completed: int
    tasks_total: int
    status: str


class TaskResponse(BaseModel):
    id: str
    task_name: str
    status: str
    due_date: Optional[str] = None
    completed_at: Optional[str] = None


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


# Document upload endpoint
@app.post("/api/v1/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    user_id: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Upload a document for processing.
    
    This endpoint:
    1. Receives document file from iOS app
    2. Saves document to temporary storage
    3. Creates database record
    4. Triggers CrewAI crew for processing
    5. Returns document ID and status
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Validate file size (10MB max per SAD)
        file_content = await file.read()
        file_size = len(file_content)
        max_size = 10 * 1024 * 1024  # 10MB
        if file_size > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File size ({file_size / 1024 / 1024:.2f}MB) exceeds maximum (10MB)"
            )
        
        # Validate document type
        valid_types = ["I9", "W4", "ID", "PASSPORT", "DRIVERSLICENSE", "SOCIALSECURITYCARD"]
        if document_type.upper() not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid document type. Valid types: {', '.join(valid_types)}"
            )
        
        # Check if user exists, create if not (for MVP)
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            # Create user for MVP (in production, user should exist)
            user = User(
                id=uuid.UUID(user_id),
                email=f"user_{user_id}@example.com",  # Placeholder
                first_name="",
                last_name=""
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Save file using storage manager
        storage = get_storage_manager()
        file_extension = Path(file.filename).suffix
        document_id = str(uuid.uuid4())
        file_name = f"{document_id}{file_extension}"
        
        file_path = storage.save_file(file_content, file_name, user_id)
        
        # Create document record in database
        document = Document(
            id=uuid.UUID(document_id),
            user_id=uuid.UUID(user_id),
            document_type=document_type.upper(),
            file_path=str(file_path),
            status="uploaded",
            created_at=datetime.utcnow()
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        
        logger.info(f"Document uploaded: {document_id} (type: {document_type}, user: {user_id})")
        
        # Trigger CrewAI crew processing asynchronously
        # For MVP, we'll process synchronously, but in production this should be async
        try:
            # Update status to processing
            document.status = "processing"
            db.commit()
            
            # Process document with CrewAI crew
            process_document_with_crew(document_id, str(file_path), document_type, user_id, db)
            
        except Exception as e:
            logger.error(f"Document processing failed: {str(e)}")
            document.status = "error"
            db.commit()
            # Don't fail the upload, just log the error
        
        return DocumentUploadResponse(
            document_id=document_id,
            status="uploaded",
            message="Document uploaded successfully and processing started"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Document upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


def process_document_with_crew(
    document_id: str,
    file_path: str,
    document_type: str,
    user_id: str,
    db: Session
):
    """
    Process document using CrewAI crew.
    
    This function:
    1. Prepares context for crew
    2. Executes crew with document processing tasks
    3. Saves results to database
    4. Updates document status
    """
    execution_id = str(uuid.uuid4())
    
    try:
        # Get crew
        crew = get_crew()
        
        # Prepare input context for crew
        input_context = {
            "document_id": document_id,
            "file_path": file_path,
            "document_type": document_type,
            "user_id": user_id,
            "execution_id": execution_id
        }
        
        # Execute crew
        logger.info(f"Starting CrewAI crew execution for document {document_id}")
        result = crew.kickoff(inputs=input_context)
        
        # Process results and update database
        # The crew output should contain extracted data and compliance status
        # For now, we'll update the document status based on crew execution
        
        document = db.query(Document).filter(Document.id == uuid.UUID(document_id)).first()
        if document:
            # Update document with processing results
            # In a full implementation, parse crew output and extract data
            document.status = "verified"  # Update based on crew results
            document.updated_at = datetime.utcnow()
            db.commit()
        
        logger.info(f"CrewAI crew execution completed for document {document_id}")
        
    except Exception as e:
        logger.error(f"CrewAI crew execution failed: {str(e)}")
        # Log error to agent_logs
        agent_log = AgentLog(
            execution_id=uuid.UUID(execution_id),
            agent_name="crew_execution",
            task_name="process_document_upload",
            status="failed",
            error_message=str(e),
            created_at=datetime.utcnow()
        )
        db.add(agent_log)
        db.commit()
        raise


# Get onboarding status endpoint
@app.get("/api/v1/onboarding/{user_id}/status", response_model=OnboardingStatusResponse)
async def get_onboarding_status(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get overall onboarding status for a user"""
    try:
        user_uuid = uuid.UUID(user_id)
        user = db.query(User).filter(User.id == user_uuid).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get all tasks for user
        tasks = db.query(OnboardingTask).filter(OnboardingTask.user_id == user_uuid).all()
        
        tasks_total = len(tasks)
        tasks_completed = len([t for t in tasks if t.status == "completed"])
        overall_progress = (tasks_completed / tasks_total * 100) if tasks_total > 0 else 0
        
        # Determine overall status
        if tasks_completed == tasks_total and tasks_total > 0:
            status = "completed"
        elif tasks_completed > 0:
            status = "in_progress"
        else:
            status = "not_started"
        
        return OnboardingStatusResponse(
            user_id=user_id,
            overall_progress=round(overall_progress, 2),
            tasks_completed=tasks_completed,
            tasks_total=tasks_total,
            status=status
        )
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    except Exception as e:
        logger.error(f"Error getting onboarding status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Get tasks endpoint
@app.get("/api/v1/tasks/{user_id}", response_model=list[TaskResponse])
async def get_tasks(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get all onboarding tasks for a user"""
    try:
        user_uuid = uuid.UUID(user_id)
        tasks = db.query(OnboardingTask).filter(OnboardingTask.user_id == user_uuid).all()
        
        return [
            TaskResponse(
                id=str(task.id),
                task_name=task.task_name,
                status=task.status,
                due_date=task.due_date.isoformat() if task.due_date else None,
                completed_at=task.completed_at.isoformat() if task.completed_at else None
            )
            for task in tasks
        ]
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    except Exception as e:
        logger.error(f"Error getting tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Complete task endpoint
@app.post("/api/v1/tasks/{task_id}/complete")
async def complete_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    """Mark a task as completed"""
    try:
        task_uuid = uuid.UUID(task_id)
        task = db.query(OnboardingTask).filter(OnboardingTask.id == task_uuid).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task.status = "completed"
        task.completed_at = datetime.utcnow()
        db.commit()
        
        return {"status": "success", "message": "Task marked as completed"}
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID format")
    except Exception as e:
        logger.error(f"Error completing task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", "8000")),
        reload=True
    )

