"""
OCR Tool for CrewAI
Extracts text from document images using OCR
"""

from crewai.tools import tool
import logging
import os

logger = logging.getLogger(__name__)


@tool("OCR Tool - Extract text from document images")
def ocr_tool(file_path: str) -> str:
    """
    Extract text from a document image using OCR.
    
    Args:
        file_path: Path to the document image file
        
    Returns:
        Extracted text from the document
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File not found at {file_path}"
        
        # For MVP: Use pytesseract or cloud OCR
        # This is a simplified implementation
        try:
            import pytesseract
            from PIL import Image
            
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            logger.info(f"OCR extracted {len(text)} characters from {file_path}")
            return text
            
        except ImportError:
            # Fallback: Return placeholder if OCR library not available
            logger.warning("pytesseract not available, using placeholder OCR")
            return f"[OCR Placeholder] Text extracted from {os.path.basename(file_path)}. " \
                   f"Document appears to be a valid image file. " \
                   f"Install pytesseract and Pillow for actual OCR functionality."
        
    except Exception as e:
        logger.error(f"OCR error: {str(e)}")
        return f"Error extracting text: {str(e)}"

