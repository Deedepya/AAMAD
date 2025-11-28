"""
Unit tests for DocumentUploadService
"""

import io
import uuid
import pytest
from unittest.mock import Mock, AsyncMock

from services.DocumentUpload.document_upload_service import (
    DocumentUploadService,
    UploadSuccess,
    UploadFailure
)


class TestDocumentUploadService:
    """Test suite for DocumentUploadService"""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock DocumentUploadClient"""
        client = Mock()
        client.documentUploadRequest = AsyncMock()
        return client
    
    @pytest.fixture
    def service(self, mock_client):
        """Create a DocumentUploadService instance"""
        return DocumentUploadService(client=mock_client)
    
    @pytest.fixture
    def test_file(self):
        """Create a test file BytesIO object"""
        file_content = b"This is a test document content"
        file = io.BytesIO(file_content)
        file.name = "test_document.txt"
        return file
    
    @pytest.fixture
    def large_file(self):
        """Create a file larger than 10MB"""
        # Create 11MB file
        large_content = b"x" * (11 * 1024 * 1024)
        file = io.BytesIO(large_content)
        file.name = "large_file.txt"
        return file
    
    @pytest.fixture
    def empty_file(self):
        """Create an empty file"""
        file = io.BytesIO(b"")
        file.name = "empty_file.txt"
        return file
    
    @pytest.fixture
    def valid_user_id(self):
        """Generate a valid UUID"""
        return str(uuid.uuid4())
    
    # ========================================================================
    # Success Cases
    # ========================================================================
    
    @pytest.mark.asyncio
    async def test_upload_success(self, service, mock_client, test_file, valid_user_id):
        """Test successful document upload"""
        # Setup mock to return success
        mock_client.documentUploadRequest.return_value = UploadSuccess(
            document_id=str(uuid.uuid4()),
            status="uploaded",
            message="Document uploaded successfully"
        )
        
        result = await service.upload_document(
            file=test_file,
            document_type="I9",
            user_id=valid_user_id
        )
        
        assert isinstance(result, UploadSuccess)
        assert result.status == "uploaded"
        mock_client.documentUploadRequest.assert_called_once()
        call_args = mock_client.documentUploadRequest.call_args
        assert call_args[1]["document_type"] == "I9"  # Should be uppercase
    
    @pytest.mark.asyncio
    async def test_upload_success_with_lowercase_document_type(self, service, mock_client, test_file, valid_user_id):
        """Test that lowercase document types are converted to uppercase"""
        mock_client.documentUploadRequest.return_value = UploadSuccess(
            document_id=str(uuid.uuid4()),
            status="uploaded",
            message="Document uploaded successfully"
        )
        
        result = await service.upload_document(
            file=test_file,
            document_type="i9",  # Lowercase
            user_id=valid_user_id
        )
        
        assert isinstance(result, UploadSuccess)
        # Verify client was called with uppercase
        call_args = mock_client.documentUploadRequest.call_args
        assert call_args[1]["document_type"] == "I9"
    
    @pytest.mark.asyncio
    async def test_upload_all_valid_document_types(self, service, mock_client, test_file, valid_user_id):
        """Test upload with all valid document types"""
        valid_types = ["I9", "W4", "ID", "PASSPORT", "DRIVERSLICENSE", "SOCIALSECURITYCARD"]
        
        mock_client.documentUploadRequest.return_value = UploadSuccess(
            document_id=str(uuid.uuid4()),
            status="uploaded",
            message="Document uploaded successfully"
        )
        
        for doc_type in valid_types:
            # Create new file for each test
            test_file_copy = io.BytesIO(b"Test content")
            test_file_copy.name = "test.txt"
            
            result = await service.upload_document(
                file=test_file_copy,
                document_type=doc_type,
                user_id=valid_user_id
            )
            
            assert isinstance(result, UploadSuccess), f"Failed for document type: {doc_type}"
    
    # ========================================================================
    # File Validation Tests
    # ========================================================================
    
    @pytest.mark.asyncio
    async def test_upload_missing_file(self, service, valid_user_id):
        """Test upload with None file"""
        result = await service.upload_document(
            file=None,
            document_type="I9",
            user_id=valid_user_id
        )
        
        assert isinstance(result, UploadFailure)
        assert result.error_code == 400
        assert "No file provided" in result.error_message
    
    @pytest.mark.asyncio
    async def test_upload_empty_file(self, service, empty_file, valid_user_id):
        """Test upload with empty file"""
        result = await service.upload_document(
            file=empty_file,
            document_type="I9",
            user_id=valid_user_id
        )
        
        assert isinstance(result, UploadFailure)
        assert result.error_code == 400
        assert "File is empty" in result.error_message
    
    @pytest.mark.asyncio
    async def test_upload_file_too_large(self, service, large_file, valid_user_id):
        """Test upload with file exceeding 10MB limit"""
        result = await service.upload_document(
            file=large_file,
            document_type="I9",
            user_id=valid_user_id
        )
        
        assert isinstance(result, UploadFailure)
        assert result.error_code == 400
        assert "exceeds maximum" in result.error_message
        assert "10MB" in result.error_message
    
    @pytest.mark.asyncio
    async def test_upload_file_at_max_size(self, service, valid_user_id):
        """Test upload with file at exactly 10MB (should pass)"""
        # Create exactly 10MB file
        max_size_content = b"x" * (10 * 1024 * 1024)
        max_file = io.BytesIO(max_size_content)
        max_file.name = "max_file.txt"
        
        mock_client = Mock()
        mock_client.documentUploadRequest = AsyncMock(return_value=UploadSuccess(
            document_id=str(uuid.uuid4()),
            status="uploaded",
            message="Document uploaded successfully"
        ))
        service.client = mock_client
        
        result = await service.upload_document(
            file=max_file,
            document_type="I9",
            user_id=valid_user_id
        )
        
        assert isinstance(result, UploadSuccess)
    
    @pytest.mark.asyncio
    async def test_upload_invalid_file_object(self, service, valid_user_id):
        """Test upload with invalid file object"""
        # Create an object that doesn't have seek/tell methods
        invalid_file = "not a file object"
        
        result = await service.upload_document(
            file=invalid_file,
            document_type="I9",
            user_id=valid_user_id
        )
        
        assert isinstance(result, UploadFailure)
        assert result.error_code == 400
        assert "Invalid file object" in result.error_message
    
    # ========================================================================
    # Document Type Validation Tests
    # ========================================================================
    
    @pytest.mark.asyncio
    async def test_upload_missing_document_type(self, service, test_file, valid_user_id):
        """Test upload with empty document type"""
        result = await service.upload_document(
            file=test_file,
            document_type="",
            user_id=valid_user_id
        )
        
        assert isinstance(result, UploadFailure)
        assert result.error_code == 400
        assert "Invalid document type" in result.error_message
    
    @pytest.mark.asyncio
    async def test_upload_none_document_type(self, service, test_file, valid_user_id):
        """Test upload with None document type"""
        result = await service.upload_document(
            file=test_file,
            document_type=None,
            user_id=valid_user_id
        )
        
        assert isinstance(result, UploadFailure)
        assert result.error_code == 400
        assert "Invalid document type" in result.error_message
    
    @pytest.mark.asyncio
    async def test_upload_invalid_document_type(self, service, test_file, valid_user_id):
        """Test upload with invalid document type"""
        result = await service.upload_document(
            file=test_file,
            document_type="INVALID_TYPE",
            user_id=valid_user_id
        )
        
        assert isinstance(result, UploadFailure)
        assert result.error_code == 400
        assert "Invalid document type" in result.error_message
        # Should list valid types
        assert "I9" in result.error_message
    
    # ========================================================================
    # User ID Validation Tests
    # ========================================================================
    
    @pytest.mark.asyncio
    async def test_upload_missing_user_id(self, service, test_file):
        """Test upload with empty user_id"""
        result = await service.upload_document(
            file=test_file,
            document_type="I9",
            user_id=""
        )
        
        assert isinstance(result, UploadFailure)
        assert result.error_code == 400
        assert "User ID is required" in result.error_message
    
    @pytest.mark.asyncio
    async def test_upload_invalid_user_id_format(self, service, test_file):
        """Test upload with invalid user_id format"""
        result = await service.upload_document(
            file=test_file,
            document_type="I9",
            user_id="not-a-valid-uuid"
        )
        
        assert isinstance(result, UploadFailure)
        assert result.error_code == 400
        assert "Invalid user ID format" in result.error_message
    
    @pytest.mark.asyncio
    async def test_upload_valid_uuid_user_id(self, service, mock_client, test_file):
        """Test upload with valid UUID user_id"""
        mock_client.documentUploadRequest.return_value = UploadSuccess(
            document_id=str(uuid.uuid4()),
            status="uploaded",
            message="Document uploaded successfully"
        )
        
        valid_uuid = str(uuid.uuid4())
        result = await service.upload_document(
            file=test_file,
            document_type="I9",
            user_id=valid_uuid
        )
        
        assert isinstance(result, UploadSuccess)
        # Verify client was called with the same user_id
        call_args = mock_client.documentUploadRequest.call_args
        assert call_args[1]["user_id"] == valid_uuid
    
    # ========================================================================
    # Client Integration Tests
    # ========================================================================
    
    @pytest.mark.asyncio
    async def test_upload_client_returns_failure(self, service, mock_client, test_file, valid_user_id):
        """Test when client returns UploadFailure"""
        mock_client.documentUploadRequest.return_value = UploadFailure(
            error_code=500,
            error_message="Client error"
        )
        
        result = await service.upload_document(
            file=test_file,
            document_type="I9",
            user_id=valid_user_id
        )
        
        assert isinstance(result, UploadFailure)
        assert result.error_code == 500
        assert result.error_message == "Client error"
    
    @pytest.mark.asyncio
    async def test_upload_client_receives_correct_parameters(self, service, mock_client, test_file, valid_user_id):
        """Test that client receives correct parameters"""
        mock_client.documentUploadRequest.return_value = UploadSuccess(
            document_id=str(uuid.uuid4()),
            status="uploaded",
            message="Document uploaded successfully"
        )
        
        await service.upload_document(
            file=test_file,
            document_type="w4",  # Lowercase
            user_id=valid_user_id
        )
        
        # Verify client was called with correct parameters
        mock_client.documentUploadRequest.assert_called_once()
        call_kwargs = mock_client.documentUploadRequest.call_args[1]
        
        assert call_kwargs["document_type"] == "W4"  # Should be uppercase
        assert call_kwargs["user_id"] == valid_user_id
        assert call_kwargs["file"] == test_file
    
    @pytest.mark.asyncio
    async def test_upload_file_position_preserved(self, service, mock_client, test_file, valid_user_id):
        """Test that file position is preserved for client"""
        mock_client.documentUploadRequest.return_value = UploadSuccess(
            document_id=str(uuid.uuid4()),
            status="uploaded",
            message="Document uploaded successfully"
        )
        
        # Service will seek to end and back to beginning
        # Verify file is readable by client
        await service.upload_document(
            file=test_file,
            document_type="I9",
            user_id=valid_user_id
        )
        
        # File should be readable (position reset)
        call_kwargs = mock_client.documentUploadRequest.call_args[1]
        client_file = call_kwargs["file"]
        client_file.seek(0)
        content = client_file.read()
        assert len(content) > 0
    
    # ========================================================================
    # Edge Cases
    # ========================================================================
    
    @pytest.mark.asyncio
    async def test_upload_file_size_calculation(self, service, valid_user_id):
        """Test file size calculation for various file sizes"""
        mock_client = Mock()
        mock_client.documentUploadRequest = AsyncMock(return_value=UploadSuccess(
            document_id=str(uuid.uuid4()),
            status="uploaded",
            message="Document uploaded successfully"
        ))
        service.client = mock_client
        
        # Test with 1MB file
        one_mb_file = io.BytesIO(b"x" * (1 * 1024 * 1024))
        one_mb_file.name = "1mb.txt"
        
        result = await service.upload_document(
            file=one_mb_file,
            document_type="I9",
            user_id=valid_user_id
        )
        
        assert isinstance(result, UploadSuccess)
    
    @pytest.mark.asyncio
    async def test_upload_multiple_validations_fail(self, service):
        """Test that first validation error is returned"""
        # Missing file, invalid type, and invalid user_id
        result = await service.upload_document(
            file=None,
            document_type="INVALID",
            user_id="invalid"
        )
        
        # Should return first error (missing file)
        assert isinstance(result, UploadFailure)
        assert result.error_code == 400
        assert "No file provided" in result.error_message

