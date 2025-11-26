# Tests for CrewAI tools

import pytest
import tempfile
import os
from pathlib import Path
from PIL import Image
import io

# Import tools
from crew.tools.ocr_tool import ocr_tool
from crew.tools.document_validation_tool import document_validation_tool
from crew.tools.image_processing_tool import image_processing_tool
from crew.tools.compliance_validation_tool import compliance_validation_tool
from crew.tools.audit_logging_tool import audit_logging_tool


@pytest.mark.tools
class TestOCRTool:
    """Tests for OCR tool"""
    
    def test_ocr_tool_with_image(self, temp_upload_dir):
        """Test OCR tool with a test image"""
        # Create a simple test image with text
        img = Image.new('RGB', (200, 50), color='white')
        # Note: In a real test, you'd add text to the image
        # For now, we'll test the tool structure
        
        test_file = temp_upload_dir / "test_ocr.jpg"
        img.save(test_file)
        
        result = ocr_tool(str(test_file))
        
        assert "status" in result
        assert "extracted_text" in result
        assert "confidence_score" in result
    
    def test_ocr_tool_file_not_found(self):
        """Test OCR tool with non-existent file"""
        result = ocr_tool("/nonexistent/file.jpg")
        assert result["status"] == "failed"
        assert "error" in result


@pytest.mark.tools
class TestDocumentValidationTool:
    """Tests for document validation tool"""
    
    def test_validate_valid_document(self, temp_upload_dir):
        """Test validation of valid document"""
        # Create test image file
        img = Image.new('RGB', (800, 600), color='white')
        test_file = temp_upload_dir / "test_doc.jpg"
        img.save(test_file)
        
        result = document_validation_tool(
            str(test_file),
            "I9",
            extracted_text="Form I-9 Employment Eligibility Verification Section 1"
        )
        
        assert "validation_status" in result
        assert "is_valid" in result
        assert "errors" in result
        assert "warnings" in result
    
    def test_validate_invalid_file_type(self, temp_upload_dir):
        """Test validation with invalid file type"""
        test_file = temp_upload_dir / "test_doc.txt"
        test_file.write_text("not an image")
        
        result = document_validation_tool(
            str(test_file),
            "I9"
        )
        
        assert result["validation_status"] in ["invalid", "needs-review"]
        assert len(result["errors"]) > 0
    
    def test_validate_file_too_large(self, temp_upload_dir):
        """Test validation with file exceeding size limit"""
        # Create large file (11MB)
        test_file = temp_upload_dir / "large_file.jpg"
        with open(test_file, "wb") as f:
            f.write(b"x" * (11 * 1024 * 1024))
        
        result = document_validation_tool(
            str(test_file),
            "I9"
        )
        
        assert result["validation_status"] == "invalid"
        assert any("exceeds maximum" in str(error) for error in result["errors"])


@pytest.mark.tools
class TestImageProcessingTool:
    """Tests for image processing tool"""
    
    def test_process_image(self, temp_upload_dir):
        """Test image processing"""
        # Create test image
        img = Image.new('RGB', (800, 600), color='white')
        test_file = temp_upload_dir / "test_image.jpg"
        img.save(test_file)
        
        result = image_processing_tool(str(test_file))
        
        assert result["status"] == "success"
        assert "processed_path" in result
        assert "original_path" in result
    
    def test_process_image_file_not_found(self):
        """Test image processing with non-existent file"""
        result = image_processing_tool("/nonexistent/file.jpg")
        assert result["status"] == "failed"


@pytest.mark.tools
class TestComplianceValidationTool:
    """Tests for compliance validation tool"""
    
    def test_validate_i9_compliance(self):
        """Test I-9 compliance validation"""
        extracted_data = {
            "extracted_text": "Form I-9 Employment Eligibility Verification Section 1 Employee Information Last Name First Name Signature Date"
        }
        
        result = compliance_validation_tool(
            "I9",
            extracted_data,
            user_id="test-user-id"
        )
        
        assert "compliance_status" in result
        assert "compliance_type" in result
        assert result["compliance_type"] == "I9"
        assert "audit_log" in result
    
    def test_validate_w4_compliance(self):
        """Test W-4 compliance validation"""
        extracted_data = {
            "extracted_text": "Form W-4 Employee's Withholding Certificate Employee's Name Social Security Number Address Signature"
        }
        
        result = compliance_validation_tool(
            "W4",
            extracted_data,
            user_id="test-user-id"
        )
        
        assert "compliance_status" in result
        assert result["compliance_type"] == "W4"
    
    def test_validate_id_compliance(self):
        """Test ID document compliance validation"""
        extracted_data = {
            "extracted_text": "John Doe 01/01/1990 DL123456789"
        }
        
        result = compliance_validation_tool(
            "ID",
            extracted_data,
            user_id="test-user-id"
        )
        
        assert "compliance_status" in result
        assert result["compliance_type"] == "ID"


@pytest.mark.tools
class TestAuditLoggingTool:
    """Tests for audit logging tool"""
    
    def test_create_audit_log(self, sample_user_id):
        """Test creating audit log entry"""
        result = audit_logging_tool(
            action="document_uploaded",
            user_id=sample_user_id,
            document_id="test-doc-id",
            details={"file_size": 1024}
        )
        
        assert "id" in result
        assert result["action"] == "document_uploaded"
        assert result["user_id"] == sample_user_id
        assert result["status"] == "logged"
        assert "timestamp" in result

