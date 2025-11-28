from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi import Depends
import io
import logging
from fastapi import Request

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.post("/upload")
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    document_type: str = "I9",
    user_id: str = ""
):
    """
    Upload a document using the DocumentUploadService
    """
    # Extract form data fields (FastAPI doesn't auto-extract form fields without Form())
    # This handles multipart/form-data where user_id and document_type are sent as form fields
    try:
        form_data = await request.form()
        # Override with form data if present
        if "document_type" in form_data:
            document_type = form_data["document_type"]
        if "user_id" in form_data:
            user_id = form_data["user_id"]
    except Exception:
        # If form data can't be read, use defaults/parameters as-is
        pass
    
    # Read file content
    file_content = await file.read()
    file_bytes = io.BytesIO(file_content)
    file_bytes.name = file.filename

    # Access service from app.state
    upload_service = request.app.state.upload_service

    # Call service
    result = await upload_service.upload_document(
        file=file_bytes,
        document_type=document_type,
        user_id=user_id
    )

    # Handle response
    if hasattr(result, "error_code"):
        raise HTTPException(status_code=result.error_code, detail=result.error_message)
    return result
