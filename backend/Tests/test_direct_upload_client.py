import io
import uuid
import pytest
from unittest.mock import Mock, patch

from services.DocumentUpload.direct_upload_client import DirectDocumentUploadClient
from services.DocumentUpload.document_upload_service import UploadSuccess, UploadFailure


@pytest.mark.asyncio
class TestDirectDocumentUploadClient:
    """Unit tests for DirectDocumentUploadClient"""

    @pytest.fixture
    def client(self):
        """Client without storage"""
        return DirectDocumentUploadClient(storage_manager=None)

    @pytest.fixture
    def client_with_storage(self):
        """Client with mocked storage manager"""
        storage_manager = Mock()
        storage_manager.save_file = Mock(return_value="/mock/path/file.jpg")
        return DirectDocumentUploadClient(storage_manager=storage_manager)

    @pytest.fixture
    def test_file(self):
        """Sample file with a name"""
        file = io.BytesIO(b"Test content")
        file.name = "test.txt"
        return file

    @pytest.fixture
    def test_file_no_name(self):
        """Sample file without a name attribute"""
        return io.BytesIO(b"Test content")

    # -------------------------------
    # Basic upload tests
    # -------------------------------
    async def test_upload_success_without_storage(self, client, test_file):
        """Test successful upload without storage manager"""
        user_id = str(uuid.uuid4())
        result = await client.documentUploadRequest(
            file=test_file,
            document_type="I9",
            user_id=user_id
        )

        assert isinstance(result, UploadSuccess)
        assert result.status == "uploaded"
        assert result.message == "Document uploaded successfully"
        assert result.document_id is not None
        uuid.UUID(result.document_id)  # Ensure valid UUID

    async def test_upload_success_with_storage(self, client_with_storage, test_file):
        """Test successful upload with storage manager"""
        user_id = str(uuid.uuid4())
        result = await client_with_storage.documentUploadRequest(
            file=test_file,
            document_type="W4",
            user_id=user_id
        )

        assert isinstance(result, UploadSuccess)
        assert result.status == "uploaded"
        assert result.message == "Document uploaded successfully"
        client_with_storage.storage_manager.save_file.assert_called_once()

    # -------------------------------
    # File name / extension tests
    # -------------------------------
    async def test_upload_with_filename_extension(self, client_with_storage, test_file):
        """Test that file extension is extracted from filename"""
        test_file.name = "document.pdf"
        user_id = str(uuid.uuid4())
        result = await client_with_storage.documentUploadRequest(
            file=test_file,
            document_type="I9",
            user_id=user_id
        )

        assert isinstance(result, UploadSuccess)
        saved_filename = client_with_storage.storage_manager.save_file.call_args[0][1]
        assert saved_filename.endswith(".pdf")
        assert saved_filename.startswith(result.document_id)
        # Verify the filename format: {document_id}.pdf
        assert saved_filename == f"{result.document_id}.pdf"

    async def test_upload_without_filename_uses_default_extension(self, client_with_storage, test_file_no_name):
        """Test that default .jpg extension is used when filename is missing"""
        user_id = str(uuid.uuid4())
        result = await client_with_storage.documentUploadRequest(
            file=test_file_no_name,
            document_type="I9",
            user_id=user_id
        )

        assert isinstance(result, UploadSuccess)
        saved_filename = client_with_storage.storage_manager.save_file.call_args[0][1]
        assert saved_filename.endswith(".jpg")
        assert saved_filename.startswith(result.document_id)

    # -------------------------------
    # Edge case tests
    # -------------------------------
    async def test_upload_handles_storage_error_gracefully(self, test_file):
        """Test that storage errors don't cause upload to fail"""
        storage_manager = Mock()
        storage_manager.save_file.side_effect = Exception("Storage error")
        client = DirectDocumentUploadClient(storage_manager=storage_manager)

        result = await client.documentUploadRequest(
            file=test_file,
            document_type="I9",
            user_id=str(uuid.uuid4())
        )

        assert isinstance(result, UploadSuccess)
        assert result.status == "uploaded"
        assert result.message == "Document uploaded successfully"

    async def test_upload_handles_general_exception(self):
        """Test that general exceptions are caught and returned as UploadFailure"""
        # Generate user_id before patching uuid4
        user_id = str(uuid.uuid4())
        test_file = io.BytesIO(b"Test content")
        test_file.name = "test.txt"
        
        # Patch uuid4 to raise an exception when called inside the method
        with patch('services.DocumentUpload.direct_upload_client.uuid.uuid4', side_effect=Exception("Unexpected error")):
            client = DirectDocumentUploadClient()
            
            result = await client.documentUploadRequest(
                file=test_file,
                document_type="I9",
                user_id=user_id
            )

            assert isinstance(result, UploadFailure)
            assert result.error_code == 500
            assert "Internal error" in result.error_message

    async def test_upload_generates_unique_document_ids(self, client, test_file):
        """Test that each upload generates a unique document ID"""
        user_id = str(uuid.uuid4())
        result1 = await client.documentUploadRequest(
            file=test_file,
            document_type="I9",
            user_id=user_id
        )

        test_file2 = io.BytesIO(b"Another content")
        test_file2.name = "test2.txt"
        result2 = await client.documentUploadRequest(
            file=test_file2,
            document_type="W4",
            user_id=user_id
        )

        assert isinstance(result1, UploadSuccess)
        assert isinstance(result2, UploadSuccess)
        assert result1.document_id != result2.document_id
        # Verify both are valid UUIDs
        uuid.UUID(result1.document_id)
        uuid.UUID(result2.document_id)

    async def test_upload_file_with_no_suffix(self, client_with_storage):
        """Test file with name but no extension uses default .jpg"""
        test_file = io.BytesIO(b"Test content")
        test_file.name = "document"  # No extension
        
        result = await client_with_storage.documentUploadRequest(
            file=test_file,
            document_type="I9",
            user_id=str(uuid.uuid4())
        )
        
        assert isinstance(result, UploadSuccess)
        saved_filename = client_with_storage.storage_manager.save_file.call_args[0][1]
        assert saved_filename.endswith(".jpg")
        assert saved_filename.startswith(result.document_id)

    async def test_upload_resets_file_position(self, client_with_storage, test_file):
        """Test that file position is reset before reading"""
        # Move file pointer to end
        test_file.seek(0, io.SEEK_END)
        initial_position = test_file.tell()
        assert initial_position > 0
        
        user_id = str(uuid.uuid4())
        result = await client_with_storage.documentUploadRequest(
            file=test_file,
            document_type="I9",
            user_id=user_id
        )
        
        assert isinstance(result, UploadSuccess)
        # Verify storage manager received the full file content
        call_args = client_with_storage.storage_manager.save_file.call_args
        file_content = call_args[0][0]  # First positional argument
        assert len(file_content) == initial_position

    async def test_upload_with_different_document_types(self, client, test_file):
        """Test upload with different document types"""
        document_types = ["I9", "W4", "ID", "PASSPORT", "DRIVERSLICENSE", "SOCIALSECURITYCARD"]
        user_id = str(uuid.uuid4())
        
        for doc_type in document_types:
            # Create new file for each test
            test_file_copy = io.BytesIO(b"Test content")
            test_file_copy.name = "test.txt"
            
            result = await client.documentUploadRequest(
                file=test_file_copy,
                document_type=doc_type,
                user_id=user_id
            )
            
            assert isinstance(result, UploadSuccess), f"Failed for document type: {doc_type}"
            assert result.status == "uploaded"
