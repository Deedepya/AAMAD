from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi import Depends
import io
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
