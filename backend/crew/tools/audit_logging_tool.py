"""
Audit Logging Tool for CrewAI
Creates audit trail entries for document processing
"""

from crewai.tools import tool
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@tool("Audit Logging Tool - Create audit trail entries")
def audit_logging_tool(
    document_id: str,
    user_id: str,
    action: str,
    details: str = ""
) -> str:
    """
    Create an audit log entry for document processing actions.
    
    Args:
        document_id: Document identifier
        user_id: User identifier
        action: Action performed (e.g., "upload", "process", "validate")
        details: Additional details about the action
        
    Returns:
        Audit log entry in JSON format
    """
    try:
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "document_id": document_id,
            "user_id": user_id,
            "action": action,
            "details": details,
            "status": "logged"
        }
        
        # Log to application logger
        logger.info(f"Audit log: {action} for document {document_id} by user {user_id}")
        
        # In production, this would write to database or audit log service
        # For MVP, we just return the audit entry
        result = json.dumps(audit_entry, indent=2)
        return result
        
    except Exception as e:
        logger.error(f"Audit logging error: {str(e)}")
        return f'{{"status": "error", "message": "{str(e)}"}}'

