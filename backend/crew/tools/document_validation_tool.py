# Document Validation Tool
# Validates document format, completeness, and quality

try:
    from crewai_tools import tool
except ImportError:
    from crewai import tool
from PIL import Image
import os
from typing import Dict, Any, List
import logging
import re

logger = logging.getLogger(__name__)


@tool("Document Validation Tool")
def document_validation_tool(file_path: str, document_type: str, extracted_text: str = "") -> Dict[str, Any]:
    """
    Validate document format, completeness, and quality.
    
    Args:
        file_path: Path to the document file
        document_type: Type of document (I9, W4, ID, PASSPORT, etc.)
        extracted_text: Optional extracted text from OCR
        
    Returns:
        Dictionary with validation results
    """
    try:
        validation_errors = []
        validation_warnings = []
        
        # Check file exists
        if not os.path.exists(file_path):
            return {
                "validation_status": "invalid",
                "errors": ["File not found"],
                "warnings": [],
                "is_valid": False
            }
        
        # Check file size (max 10MB per SAD)
        file_size = os.path.getsize(file_path)
        max_size = 10 * 1024 * 1024  # 10MB
        if file_size > max_size:
            validation_errors.append(f"File size ({file_size / 1024 / 1024:.2f}MB) exceeds maximum (10MB)")
        
        # Check file format
        valid_extensions = [".jpg", ".jpeg", ".png", ".pdf"]
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in valid_extensions:
            validation_errors.append(f"Invalid file format: {file_ext}. Supported: {', '.join(valid_extensions)}")
        
        # Image-specific validations
        if file_ext in [".jpg", ".jpeg", ".png"]:
            try:
                image = Image.open(file_path)
                width, height = image.size
                
                # Check minimum resolution
                min_resolution = 300 * 300  # Minimum pixels
                if width * height < min_resolution:
                    validation_warnings.append(f"Image resolution ({width}x{height}) may be too low for accurate OCR")
                
                # Check aspect ratio (documents are typically rectangular)
                aspect_ratio = width / height if height > 0 else 0
                if aspect_ratio < 0.5 or aspect_ratio > 2.0:
                    validation_warnings.append(f"Unusual aspect ratio ({aspect_ratio:.2f}) - document may be skewed")
                    
            except Exception as e:
                validation_errors.append(f"Unable to process image: {str(e)}")
        
        # Document type-specific validations
        if extracted_text:
            validation_result = validate_document_content(document_type, extracted_text)
            validation_errors.extend(validation_result.get("errors", []))
            validation_warnings.extend(validation_result.get("warnings", []))
        
        # Determine validation status
        is_valid = len(validation_errors) == 0
        validation_status = "valid" if is_valid else ("needs-review" if len(validation_warnings) > 0 else "invalid")
        
        result = {
            "validation_status": validation_status,
            "errors": validation_errors,
            "warnings": validation_warnings,
            "is_valid": is_valid,
            "file_size": file_size,
            "file_format": file_ext
        }
        
        logger.info(f"Document validation completed for {file_path}: {validation_status}")
        return result
        
    except Exception as e:
        logger.error(f"Document validation failed for {file_path}: {str(e)}")
        return {
            "validation_status": "invalid",
            "errors": [str(e)],
            "warnings": [],
            "is_valid": False
        }


def validate_document_content(document_type: str, extracted_text: str) -> Dict[str, List[str]]:
    """
    Validate document content based on document type.
    
    Args:
        document_type: Type of document
        extracted_text: Extracted text from OCR
        
    Returns:
        Dictionary with errors and warnings
    """
    errors = []
    warnings = []
    text_lower = extracted_text.lower()
    
    # I-9 specific validations
    if document_type.upper() == "I9":
        required_keywords = ["form i-9", "employment eligibility", "section 1", "section 2"]
        found_keywords = [kw for kw in required_keywords if kw in text_lower]
        if len(found_keywords) < 2:
            warnings.append("I-9 form may be incomplete - missing expected sections")
    
    # W-4 specific validations
    elif document_type.upper() == "W4":
        required_keywords = ["form w-4", "employee's withholding", "allowances"]
        found_keywords = [kw for kw in required_keywords if kw in text_lower]
        if len(found_keywords) < 2:
            warnings.append("W-4 form may be incomplete - missing expected fields")
    
    # ID/Driver's License validations
    elif document_type.upper() in ["ID", "DRIVERSLICENSE"]:
        # Check for common ID fields
        has_name = bool(re.search(r'\b[a-z]+\s+[a-z]+\b', text_lower))
        has_date = bool(re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text_lower))
        if not has_name or not has_date:
            warnings.append("ID document may be missing key information (name or date)")
    
    # Passport validations
    elif document_type.upper() == "PASSPORT":
        if "passport" not in text_lower and "passport number" not in text_lower:
            warnings.append("Passport document may not be a valid passport")
    
    return {"errors": errors, "warnings": warnings}

