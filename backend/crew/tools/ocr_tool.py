# OCR Tool
# Extracts text from document images using OCR technology

try:
    from crewai_tools import tool
except ImportError:
    # Fallback for different CrewAI versions
    from crewai import tool
from PIL import Image
import pytesseract
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


@tool("OCR Tool")
def ocr_tool(file_path: str) -> Dict[str, Any]:
    """
    Extract text from document image using OCR.
    
    Args:
        file_path: Path to the document image file
        
    Returns:
        Dictionary with extracted text and metadata
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Document file not found: {file_path}")
        
        # Open and process image
        image = Image.open(file_path)
        
        # Perform OCR
        extracted_text = pytesseract.image_to_string(image)
        
        # Get detailed OCR data with confidence scores
        ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        
        # Calculate average confidence
        confidences = [int(conf) for conf in ocr_data.get("conf", []) if int(conf) > 0]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        result = {
            "extracted_text": extracted_text,
            "confidence_score": avg_confidence,
            "word_count": len(extracted_text.split()),
            "ocr_data": ocr_data,
            "status": "success"
        }
        
        logger.info(f"OCR extraction completed for {file_path} with confidence {avg_confidence:.2f}%")
        return result
        
    except Exception as e:
        logger.error(f"OCR extraction failed for {file_path}: {str(e)}")
        return {
            "extracted_text": "",
            "confidence_score": 0,
            "word_count": 0,
            "error": str(e),
            "status": "failed"
        }

