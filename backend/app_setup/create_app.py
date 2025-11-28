# app_setup/create_app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Import your real service + client
from services.DocumentUpload.document_upload_service import DocumentUploadService
from services.DocumentUpload.direct_upload_client import DirectDocumentUploadClient


# ============================================================
# Logging Setup
# ============================================================

def _configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


# ============================================================
# FastAPI App Creation
# ============================================================

def _create_fastapi_app() -> FastAPI:
    """Initialize FastAPI application with metadata."""
    return FastAPI(
        title="Onboarding Workflow API",
        description="Automated Employee Onboarding Workflow Backend",
        version="1.0.0"
    )


# ============================================================
# CORS Setup
# ============================================================

def _configure_cors(app: FastAPI):
    """Add global CORS configuration."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],   # Restrict in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )


# ============================================================
# Service Initialization
# ============================================================

def _configure_services(app: FastAPI):
    """
    Attach services to app.state so endpoints can use them.

    Since you currently have NO storage manager and NO DB,
    we initialize the DirectDocumentUploadClient WITHOUT storage.
    """
    # Create Direct client (NO storage manager)
    upload_client = DirectDocumentUploadClient(storage_manager=None)

    # Create the service layer
    upload_service = DocumentUploadService(client=upload_client)

    # Attach to FastAPI app
    app.state.upload_service = upload_service


# ============================================================
# Public create_app() function
# ============================================================

# def create_app() -> FastAPI:
#     """
#     Build and return a fully configured FastAPI app.
#     No business logic here — only configuration.
#     Endpoints are defined in main.py.
#     """
#     _configure_logging()

#     app = _create_fastapi_app()
#     _configure_cors(app)
#     _configure_services(app)

#     return app

from app_routes.document_routes import router as document_router

def create_app() -> FastAPI:
    _configure_logging()
    app = _create_fastapi_app()
    _configure_cors(app)
    _configure_services(app)
    app.include_router(document_router, prefix="/documents")
    return app