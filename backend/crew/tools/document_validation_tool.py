"""
Document Validation Tool for CrewAI
Validates document format, completeness, and content
"""

from crewai.tools import tool
import logging
import os

logger = logging.getLogger(__name__)


@tool("Document Validation Tool - Validate document format and content")
def document_validation_tool(file_path: str, document_type: str) -> str:
    """
    Validate document format, size, and basic content requirements.
    
    Args:
        file_path: Path to the document file
        document_type: Expected document type (I9, W4, ID, etc.)
        
    Returns:
        Validation result in JSON format
    """
    try:
        if not os.path.exists(file_path):
            return '{"status": "error", "message": "File not found"}'
        
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        
        # Basic validation checks
        validation_results = {
            "status": "valid",
            "file_size_mb": round(file_size_mb, 2),
            "document_type": document_type,
            "checks": []
        }
        
        # Check file size (max 10MB)
        if file_size_mb > 10:
            validation_results["status"] = "invalid"
            validation_results["checks"].append({
                "check": "file_size",
                "result": "failed",
                "message": f"File size {file_size_mb:.2f}MB exceeds 10MB limit"
            })
        else:
            validation_results["checks"].append({
                "check": "file_size",
                "result": "passed",
                "message": f"File size {file_size_mb:.2f}MB is within limits"
            })
        
        # Check file is not empty
        if file_size == 0:
            validation_results["status"] = "invalid"
            validation_results["checks"].append({
                "check": "file_empty",
                "result": "failed",
                "message": "File is empty"
            })
        else:
            validation_results["checks"].append({
                "check": "file_empty",
                "result": "passed",
                "message": "File has content"
            })
        
        # Check file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext in valid_extensions:
            validation_results["checks"].append({
                "check": "file_format",
                "result": "passed",
                "message": f"File format {file_ext} is supported"
            })
        else:
            validation_results["status"] = "needs-review"
            validation_results["checks"].append({
                "check": "file_format",
                "result": "warning",
                "message": f"File format {file_ext} may not be optimal"
            })
        
        import json
        result = json.dumps(validation_results, indent=2)
        logger.info(f"Document validation completed for {file_path}: {validation_results['status']}")
        return result
        
    except Exception as e:
        logger.error(f"Document validation error: {str(e)}")
        return f'{{"status": "error", "message": "{str(e)}"}}'

