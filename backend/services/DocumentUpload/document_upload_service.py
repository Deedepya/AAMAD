"""
Document Upload Service
Implements DocumentUploadInterface for handling document uploads with validation
"""

import io
import uuid
from dataclasses import dataclass
from typing import Union, Protocol


# ============================================================================
# Response Models
# ============================================================================

@dataclass
class UploadSuccess:
    """Success response for document upload"""
    document_id: str
    status: str
    message: str


@dataclass
class UploadFailure:
    """Failure response for document upload"""
    error_code: int
    error_message: str


UploadResult = Union[UploadSuccess, UploadFailure]


# ============================================================================
# Client Protocol/Interface
# ============================================================================

class DocumentUploadClient(Protocol):
    """
    Protocol for document upload client.
    
    Defines the interface for clients that send document upload requests
    to external APIs or services.
    """
    
    async def documentUploadRequest(
        self,
        file: io.BytesIO,
        document_type: str,
        user_id: str
    ) -> UploadResult:
        """
        Send document upload request to external API/service.
        
        Args:
            file: File content as BytesIO
            document_type: Type of document (I9, W4, ID, etc.)
            user_id: Unique identifier for the user
            
        Returns:
            UploadSuccess: If upload succeeds, contains document_id, status, message
            UploadFailure: If upload fails, contains error_code and error_message
        """
        ...


# ============================================================================
# Service Implementation
# ============================================================================

class DocumentUploadService:
    """
    Service for handling document uploads.
    
    Implements DocumentUploadInterface and provides validation
    and processing for document uploads.
    
    Uses a DocumentUploadClient to send API requests after validation.
    """
    
    # Valid document types (case-insensitive)
    VALID_DOCUMENT_TYPES = [
        "I9", "W4", "ID", "PASSPORT", 
        "DRIVERSLICENSE", "SOCIALSECURITYCARD"
    ]
    
    # Maximum file size: 10MB
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes
    
    def __init__(self, client: DocumentUploadClient):
        """
        Initialize DocumentUploadService with a client.
        
        Args:
            client: DocumentUploadClient implementation for sending API requests
        """
        self.client = client
    
    async def upload_document(
        self,
        file: io.BytesIO,
        document_type: str,
        user_id: str
    ) -> UploadResult:
        """
        Upload a document for processing.
        
        Args:
            file: File content as BytesIO (can be None)
            document_type: Type of document (I9, W4, ID, etc.)
            user_id: Unique identifier for the user
            
        Returns:
            UploadSuccess: If upload succeeds, contains document_id, status, message
            UploadFailure: If upload fails, contains error_code and error_message
        """
        # Validate file exists
        if file is None:
            return UploadFailure(
                error_code=400,
                error_message="No file provided"
            )
        
        # Validate file has content
        try:
            file.seek(0, io.SEEK_END)
            file_size = file.tell()
            file.seek(0)  # Reset to beginning
        except (AttributeError, OSError):
            return UploadFailure(
                error_code=400,
                error_message="Invalid file object"
            )
        
        if file_size == 0:
            return UploadFailure(
                error_code=400,
                error_message="File is empty"
            )
        
        # Validate file size (10MB max)
        if file_size > self.MAX_FILE_SIZE:
            file_size_mb = file_size / (1024 * 1024)
            return UploadFailure(
                error_code=400,
                error_message=f"File size ({file_size_mb:.2f}MB) exceeds maximum (10MB)"
            )
        
        # Validate document type
        if not document_type:
            valid_types_str = ", ".join(self.VALID_DOCUMENT_TYPES)
            return UploadFailure(
                error_code=400,
                error_message=f"Invalid document type. Valid types: {valid_types_str}"
            )
        
        document_type_upper = document_type.upper()
        if document_type_upper not in self.VALID_DOCUMENT_TYPES:
            valid_types_str = ", ".join(self.VALID_DOCUMENT_TYPES)
            return UploadFailure(
                error_code=400,
                error_message=f"Invalid document type. Valid types: {valid_types_str}"
            )
        
        # Validate user_id format (basic UUID check)
        if not user_id:
            return UploadFailure(
                error_code=400,
                error_message="User ID is required"
            )
        
        try:
            uuid.UUID(user_id)
        except (ValueError, TypeError):
            return UploadFailure(
                error_code=400,
                error_message="Invalid user ID format"
            )
        
        # All validations passed - send request via client
        # Client handles the actual API request and returns the result
        result = await self.client.documentUploadRequest(
            file=file,
            document_type=document_type_upper,
            user_id=user_id
        )
        
        # Return the client's response (UploadSuccess or UploadFailure)
        return result

