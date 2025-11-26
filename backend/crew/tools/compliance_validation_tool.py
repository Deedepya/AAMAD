# Compliance Validation Tool
# Validates document compliance with regulatory requirements

try:
    from crewai_tools import tool
except ImportError:
    from crewai import tool
from typing import Dict, Any
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)


@tool("Compliance Validation Tool")
def compliance_validation_tool(
    document_type: str,
    extracted_data: Dict[str, Any],
    user_id: str = None
) -> Dict[str, Any]:
    """
    Validate document compliance with regulatory requirements (I-9, W-4, etc.).
    
    Args:
        document_type: Type of document (I9, W4, etc.)
        extracted_data: Extracted document data from OCR
        user_id: Optional user ID for context
        
    Returns:
        Dictionary with compliance validation results
    """
    try:
        compliance_status = "compliant"
        compliance_errors = []
        compliance_warnings = []
        audit_log = {
            "validated_at": datetime.utcnow().isoformat(),
            "document_type": document_type,
            "validation_rules_applied": []
        }
        
        # I-9 Compliance Validation
        if document_type.upper() == "I9":
            i9_result = validate_i9_compliance(extracted_data)
            compliance_status = i9_result["status"]
            compliance_errors.extend(i9_result.get("errors", []))
            compliance_warnings.extend(i9_result.get("warnings", []))
            audit_log["validation_rules_applied"].append("I-9 Section 1 and Section 2 requirements")
            audit_log["i9_validation"] = i9_result
        
        # W-4 Compliance Validation
        elif document_type.upper() == "W4":
            w4_result = validate_w4_compliance(extracted_data)
            compliance_status = w4_result["status"]
            compliance_errors.extend(w4_result.get("errors", []))
            compliance_warnings.extend(w4_result.get("warnings", []))
            audit_log["validation_rules_applied"].append("W-4 withholding requirements")
            audit_log["w4_validation"] = w4_result
        
        # ID/Passport Compliance (basic checks)
        elif document_type.upper() in ["ID", "PASSPORT", "DRIVERSLICENSE"]:
            id_result = validate_id_compliance(extracted_data)
            compliance_status = id_result["status"]
            compliance_errors.extend(id_result.get("errors", []))
            compliance_warnings.extend(id_result.get("warnings", []))
            audit_log["validation_rules_applied"].append("Identity document verification")
            audit_log["id_validation"] = id_result
        
        # Determine final status
        if compliance_errors:
            compliance_status = "non_compliant"
        elif compliance_warnings:
            compliance_status = "needs_review"
        
        result = {
            "compliance_status": compliance_status,
            "compliance_type": document_type.upper(),
            "errors": compliance_errors,
            "warnings": compliance_warnings,
            "audit_log": audit_log,
            "validated_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Compliance validation completed for {document_type}: {compliance_status}")
        return result
        
    except Exception as e:
        logger.error(f"Compliance validation failed for {document_type}: {str(e)}")
        return {
            "compliance_status": "needs_review",
            "compliance_type": document_type.upper(),
            "errors": [str(e)],
            "warnings": [],
            "audit_log": {"error": str(e)},
            "validated_at": datetime.utcnow().isoformat()
        }


def validate_i9_compliance(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate I-9 form compliance"""
    errors = []
    warnings = []
    text = extracted_data.get("extracted_text", "").lower()
    
    # Check for required I-9 sections
    has_section1 = "section 1" in text or "employee information" in text
    has_section2 = "section 2" in text or "employer review" in text
    
    if not has_section1:
        errors.append("I-9 Section 1 (Employee Information) not found")
    if not has_section2:
        warnings.append("I-9 Section 2 (Employer Review) not found - may need employer completion")
    
    # Check for required fields
    required_fields = ["last name", "first name", "signature", "date"]
    missing_fields = [field for field in required_fields if field not in text]
    if missing_fields:
        warnings.append(f"Missing I-9 fields: {', '.join(missing_fields)}")
    
    status = "compliant" if not errors else ("needs_review" if warnings else "non_compliant")
    return {"status": status, "errors": errors, "warnings": warnings}


def validate_w4_compliance(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate W-4 form compliance"""
    errors = []
    warnings = []
    text = extracted_data.get("extracted_text", "").lower()
    
    # Check for W-4 form identifier
    if "form w-4" not in text and "w-4" not in text:
        warnings.append("W-4 form identifier not clearly found")
    
    # Check for required fields
    required_fields = ["employee's name", "social security number", "address"]
    missing_fields = [field for field in required_fields if field not in text]
    if missing_fields:
        warnings.append(f"Missing W-4 fields: {', '.join(missing_fields)}")
    
    # Check for signature
    if "signature" not in text and "sign" not in text:
        warnings.append("W-4 signature not found")
    
    status = "compliant" if not errors else ("needs_review" if warnings else "non_compliant")
    return {"status": status, "errors": errors, "warnings": warnings}


def validate_id_compliance(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate ID document compliance"""
    errors = []
    warnings = []
    text = extracted_data.get("extracted_text", "")
    
    # Check for name
    if not re.search(r'\b[a-z]+\s+[a-z]+\b', text.lower()):
        warnings.append("Name not clearly found in ID document")
    
    # Check for date (birth date or expiration)
    if not re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text):
        warnings.append("Date not found in ID document")
    
    # Check for ID number pattern
    if not re.search(r'[a-z0-9]{5,}', text.lower()):
        warnings.append("ID number not clearly found")
    
    status = "compliant" if not errors else ("needs_review" if warnings else "non_compliant")
    return {"status": status, "errors": errors, "warnings": warnings}

