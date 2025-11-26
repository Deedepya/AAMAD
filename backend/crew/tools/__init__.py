# Tools package
from .ocr_tool import ocr_tool
from .document_validation_tool import document_validation_tool
from .image_processing_tool import image_processing_tool
from .compliance_validation_tool import compliance_validation_tool
from .audit_logging_tool import audit_logging_tool
from .notification_tools import email_tool, push_notification_tool, status_tracking_tool
from .hris_integration_tool import hris_integration_tool

# Tool registry for CrewAI
TOOLS_REGISTRY = {
    "ocr_tool": ocr_tool,
    "document_validation_tool": document_validation_tool,
    "image_processing_tool": image_processing_tool,
    "compliance_validation_tool": compliance_validation_tool,
    "audit_logging_tool": audit_logging_tool,
    "email_tool": email_tool,
    "push_notification_tool": push_notification_tool,
    "status_tracking_tool": status_tracking_tool,
    "hris_integration_tool": hris_integration_tool,
}

__all__ = [
    "ocr_tool",
    "document_validation_tool",
    "image_processing_tool",
    "compliance_validation_tool",
    "audit_logging_tool",
    "email_tool",
    "push_notification_tool",
    "status_tracking_tool",
    "hris_integration_tool",
    "TOOLS_REGISTRY",
]
