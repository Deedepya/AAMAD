"""
FastAPI Document Upload Endpoint
Implements responsibilities:
1. HTTP request handling - Receives POST requests, Parses URL and routes to function
7. Error handling - Converts service responses to HTTP responses, handles network issues

This endpoint delegates business logic to DocumentUploadService and handles HTTP/network errors.
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import logging
import io
import os
import httpx

from .document_upload_service import (
    DocumentUploadService, 
    DocumentUploadClient,
    UploadSuccess, 
    UploadFailure,
    UploadResult
)

logger = logging.getLogger(__name__)


# ============================================================================
# Document Upload Client Implementation
# ============================================================================

class HTTPDocumentUploadClient:
    """
    HTTP client implementation of DocumentUploadClient protocol.
    
    Makes real API requests to the backend document upload endpoint.
    """
    
    def __init__(self, base_url: str = None, timeout: float = 30.0):
        """
        Initialize HTTP client.
        
        Args:
            base_url: Base URL for the API (defaults to http://localhost:8000)
            timeout: Request timeout in seconds (default: 30)
        """
        self.base_url = base_url or os.getenv("API_BASE_URL", "http://localhost:8000")
        self.timeout = timeout
        self.upload_endpoint = f"{self.base_url}/api/v1/documents/upload"
    
    async def documentUploadRequest(
        self,
        file: io.BytesIO,
        document_type: str,
        user_id: str
    ) -> UploadResult:
        """
        Send document upload request to backend API.
        
        Args:
            file: File content as BytesIO
            document_type: Type of document (I9, W4, ID, etc.)
            user_id: Unique identifier for the user
            
        Returns:
            UploadSuccess: If upload succeeds, contains document_id, status, message
            UploadFailure: If upload fails, contains error_code and error_message
        """
        try:
            # Reset file pointer to beginning
            file.seek(0)
            
            # Get filename if available
            filename = getattr(file, 'name', 'document.jpg')
            if not filename or filename == '<no name>':
                filename = f"document_{document_type.lower()}.jpg"
            
            # Prepare multipart form data
            files = {
                'file': (filename, file, 'application/octet-stream')
            }
            data = {
                'document_type': document_type,
                'user_id': user_id
            }
            
            # Make HTTP request
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"Sending document upload request to {self.upload_endpoint}")
                response = await client.post(
                    self.upload_endpoint,
                    files=files,
                    data=data
                )
                
                # Handle response
                if response.status_code == 200:
                    # Success response - validate required fields from API
                    result = response.json()
                    
                    # Validate required fields are present (no hardcoded defaults)
                    if 'document_id' not in result:
                        logger.error("API response missing required field: document_id")
                        return UploadFailure(
                            error_code=500,
                            error_message="Invalid API response: missing document_id field"
                        )
                    if 'status' not in result:
                        logger.error("API response missing required field: status")
                        return UploadFailure(
                            error_code=500,
                            error_message="Invalid API response: missing status field"
                        )
                    if 'message' not in result:
                        logger.error("API response missing required field: message")
                        return UploadFailure(
                            error_code=500,
                            error_message="Invalid API response: missing message field"
                        )
                    
                    logger.info(f"Document upload successful: {result['document_id']}")
                    return UploadSuccess(
                        document_id=result['document_id'],
                        status=result['status'],
                        message=result['message']
                    )
                else:
                    # Error response
                    error_detail = response.text
                    try:
                        error_json = response.json()
                        error_detail = error_json.get('detail', error_detail)
                    except:
                        pass
                    
                    logger.warning(f"Document upload failed: HTTP {response.status_code} - {error_detail}")
                    return UploadFailure(
                        error_code=response.status_code,
                        error_message=error_detail or f"Upload failed with status {response.status_code}"
                    )
                    
        except httpx.TimeoutException as e:
            logger.error(f"Request timeout: {str(e)}")
            return UploadFailure(
                error_code=504,
                error_message=f"Request timeout: API did not respond within {self.timeout} seconds"
            )
        except httpx.ConnectError as e:
            logger.error(f"Connection error: {str(e)}")
            return UploadFailure(
                error_code=503,
                error_message=f"Service unavailable: Could not connect to API at {self.upload_endpoint}"
            )
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            return UploadFailure(
                error_code=500,
                error_message=f"Network error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error during API request: {str(e)}")
            return UploadFailure(
                error_code=500,
                error_message=f"Internal error: {str(e)}"
            )


# ============================================================================
# FastAPI Application
# ============================================================================

# Create FastAPI app for document upload
app = FastAPI(
    title="Document Upload API",
    description="Document upload endpoint with HTTP handling and error responses",
    version="1.0.0"
)

# Initialize client and service
upload_client = HTTPDocumentUploadClient()
upload_service = DocumentUploadService(client=upload_client)


@app.post("/api/v1/documents/upload")
async def upload_document(
    file: Optional[UploadFile] = File(None),
    document_type: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None)
):
    """
    Document upload endpoint.
    
    Responsibility 1: HTTP Request Handling
    - Receives POST requests at /api/v1/documents/upload
    - FastAPI parses URL and routes to this function
    - FastAPI extracts file, document_type, user_id from multipart/form-data
    
    Responsibility 7: Error Handling
    - Handles network/HTTP errors
    - Converts service responses (UploadSuccess/UploadFailure) to HTTP responses
    - Returns HTTPException for network issues
    
    Business logic is delegated to DocumentUploadService.
    """
    
    try:
        # Convert FastAPI UploadFile to BytesIO for service
        file_bytesio = None
        if file is not None:
            try:
                file_content = await file.read()
                file_bytesio = io.BytesIO(file_content)
                # Set filename if available (for service logging/debugging)
                if hasattr(file, 'filename') and file.filename:
                    file_bytesio.name = file.filename
            except Exception as e:
                logger.error(f"Network error: Failed to read file from request - {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Network error: Failed to read file from request. {str(e)}"
                )
        
        # Call service with business logic
        result = await upload_service.upload_document(
            file=file_bytesio,
            document_type=document_type or "",
            user_id=user_id or ""
        )
        
        # Convert service response to HTTP response
        if isinstance(result, UploadSuccess):
            return {
                "document_id": result.document_id,
                "status": result.status,
                "message": result.message
            }
        elif isinstance(result, UploadFailure):
            raise HTTPException(
                status_code=result.error_code,
                detail=result.error_message
            )
        else:
            # Unexpected response type
            logger.error(f"Unexpected service response type: {type(result)}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error: Unexpected response from service"
            )
            
    except HTTPException:
        # Re-raise HTTP exceptions (already proper HTTP responses)
        raise
    except Exception as e:
        # Handle network/HTTP errors
        logger.error(f"Network/HTTP error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Network error: {str(e)}"
        )


# Health check endpoint for testing
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "document_upload"}

