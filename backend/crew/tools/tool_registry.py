"""
Tool Registry
Central registry for document upload processing tools
"""

from typing import Dict

# Import document processing tools only
from .ocr_tool import ocr_tool
from .document_validation_tool import document_validation_tool
from .image_processing_tool import image_processing_tool
from .compliance_validation_tool import compliance_validation_tool
from .audit_logging_tool import audit_logging_tool
from .hris_integration_tool import hris_integration_tool


def get_tools_registry() -> Dict[str, any]:
    """
    Get registry of all available tools for document upload processing
    
    Returns:
        Dictionary mapping tool names to tool instances
    """
    return {
        "ocr_tool": ocr_tool,
        "document_validation_tool": document_validation_tool,
        "image_processing_tool": image_processing_tool,
        "compliance_validation_tool": compliance_validation_tool,
        "audit_logging_tool": audit_logging_tool,
        "hris_integration_tool": hris_integration_tool,
    }

