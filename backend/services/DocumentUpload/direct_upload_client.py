"""
Direct Document Upload Client Implementation
Handles document uploads directly (no HTTP calls) - for use in main.py
"""

import io
import uuid
import logging
from pathlib import Path

from .document_upload_service import (
    DocumentUploadClient,
    UploadSuccess,
    UploadFailure,
    UploadResult
)

logger = logging.getLogger(__name__)


class DirectDocumentUploadClient:
    """
    Direct implementation of DocumentUploadClient protocol.
    
    Handles document uploads directly without HTTP calls.
    For use in main.py to avoid circular dependencies.
    """
    
    def __init__(self, storage_manager=None):
        """
        Initialize direct upload client.
        
        Args:
            storage_manager: Storage manager instance (optional)
        """
        self.storage_manager = storage_manager
    
    async def documentUploadRequest(
        self,
        file: io.BytesIO,
        document_type: str,
        user_id: str
    ) -> UploadResult:
        """
        Process document upload directly (no HTTP calls).
        
        Args:
            file: File content as BytesIO
            document_type: Type of document (I9, W4, ID, etc.)
            user_id: Unique identifier for the user
            
        Returns:
            UploadSuccess: If upload succeeds, contains document_id, status, message
            UploadFailure: If upload fails, contains error_code and error_message
        """
        try:
            # Generate document ID
            document_id = str(uuid.uuid4())
            
            # Save file to storage if storage manager is available
            if self.storage_manager:
                try:
                    # Get file extension from filename if available
                    file_extension = ".jpg"  # Default
                    if hasattr(file, 'name') and file.name:
                        file_extension = Path(file.name).suffix or ".jpg"
                    
                    file_name = f"{document_id}{file_extension}"
                    
                    # Read file content
                    file.seek(0)
                    file_content = file.read()
                    
                    # Save to storage
                    file_path = self.storage_manager.save_file(
                        file_content,
                        file_name,
                        user_id
                    )
                    logger.info(f"File saved to storage: {file_path}")
                except Exception as e:
                    logger.error(f"Failed to save file to storage: {str(e)}")
                    # Continue without storage (for MVP without storage)
            
            # Return success response
            logger.info(f"Document upload successful: {document_id} (type: {document_type}, user: {user_id})")
            return UploadSuccess(
                document_id=document_id,
                status="uploaded",
                message="Document uploaded successfully"
            )
            
        except Exception as e:
            logger.error(f"Document upload failed: {str(e)}")
            return UploadFailure(
                error_code=500,
                error_message=f"Internal error: {str(e)}"
            )

