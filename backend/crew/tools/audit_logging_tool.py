# Audit Logging Tool
# Logs compliance and processing activities for audit trail

try:
    from crewai_tools import tool
except ImportError:
    from crewai import tool
from typing import Dict, Any
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


@tool("Audit Logging Tool")
def audit_logging_tool(
    action: str,
    user_id: str,
    document_id: str = None,
    details: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Create audit log entry for compliance and processing activities.
    
    Args:
        action: Action being logged (e.g., "document_uploaded", "compliance_verified")
        user_id: User ID associated with the action
        document_id: Optional document ID
        details: Additional details to log
        
    Returns:
        Dictionary with audit log entry information
    """
    try:
        audit_entry = {
            "id": str(uuid.uuid4()),
            "action": action,
            "user_id": user_id,
            "document_id": document_id,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details or {},
            "status": "logged"
        }
        
        # Log to application logger
        logger.info(f"Audit log entry created: {action} for user {user_id}")
        
        # Return audit entry (will be saved to database by caller)
        return audit_entry
        
    except Exception as e:
        logger.error(f"Audit logging failed: {str(e)}")
        return {
            "status": "failed",
            "error": str(e)
        }

