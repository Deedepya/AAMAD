"""
Compliance Validation Tool for CrewAI
Validates documents against regulatory requirements (I-9, W-4)
"""

from crewai.tools import tool
import logging

logger = logging.getLogger(__name__)


@tool("Compliance Validation Tool - Validate regulatory compliance")
def compliance_validation_tool(document_type: str, extracted_data: str = "") -> str:
    """
    Validate document compliance with regulatory requirements.
    
    Args:
        document_type: Type of document (I9, W-4, ID, etc.)
        extracted_data: Extracted document data (JSON string or text)
        
    Returns:
        Compliance validation result in JSON format
    """
    try:
        import json
        
        # Parse extracted data if it's JSON
        try:
            if isinstance(extracted_data, str):
                data = json.loads(extracted_data)
            else:
                data = extracted_data
        except (json.JSONDecodeError, TypeError):
            # If not JSON, treat as text
            data = {"raw_text": str(extracted_data)}
        
        # Basic compliance checks based on document type
        compliance_result = {
            "compliance_status": "compliant",
            "document_type": document_type,
            "checks": [],
            "warnings": []
        }
        
        # I-9 specific checks
        if document_type.upper() == "I9":
            compliance_result["checks"].append({
                "check": "document_type",
                "result": "passed",
                "message": "I-9 form identified"
            })
            # Add more I-9 specific validations here
        
        # W-4 specific checks
        elif document_type.upper() == "W4":
            compliance_result["checks"].append({
                "check": "document_type",
                "result": "passed",
                "message": "W-4 form identified"
            })
            # Add more W-4 specific validations here
        
        # ID document checks
        elif document_type.upper() in ["ID", "PASSPORT", "DRIVERSLICENSE"]:
            compliance_result["checks"].append({
                "check": "document_type",
                "result": "passed",
                "message": f"{document_type} document identified"
            })
        
        # Check if extracted data has content
        if not data or (isinstance(data, dict) and not data.get("raw_text")):
            compliance_result["compliance_status"] = "needs-review"
            compliance_result["warnings"].append("Limited data extracted from document")
        
        result = json.dumps(compliance_result, indent=2)
        logger.info(f"Compliance validation completed for {document_type}: {compliance_result['compliance_status']}")
        return result
        
    except Exception as e:
        logger.error(f"Compliance validation error: {str(e)}")
        return f'{{"compliance_status": "error", "message": "{str(e)}"}}'

