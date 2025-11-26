# Image Processing Tool
# Processes and optimizes document images

try:
    from crewai_tools import tool
except ImportError:
    from crewai import tool
from PIL import Image
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


@tool("Image Processing Tool")
def image_processing_tool(file_path: str, output_path: str = None) -> Dict[str, Any]:
    """
    Process and optimize document image for OCR.
    
    Args:
        file_path: Path to the input image file
        output_path: Optional path for processed image output
        
    Returns:
        Dictionary with processing results
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Image file not found: {file_path}")
        
        # Open image
        image = Image.open(file_path)
        original_size = image.size
        original_format = image.format
        
        # Convert to RGB if necessary (for JPEG compatibility)
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Enhance image for OCR (optional - can add more processing)
        # For now, just ensure it's in a good format
        
        # Save processed image
        if output_path is None:
            output_path = file_path.replace(".", "_processed.")
        
        image.save(output_path, "JPEG", quality=95, optimize=True)
        processed_size = os.path.getsize(output_path)
        
        result = {
            "status": "success",
            "original_path": file_path,
            "processed_path": output_path,
            "original_size": original_size,
            "original_format": original_format,
            "processed_file_size": processed_size,
            "image_mode": image.mode
        }
        
        logger.info(f"Image processing completed for {file_path}")
        return result
        
    except Exception as e:
        logger.error(f"Image processing failed for {file_path}: {str(e)}")
        return {
            "status": "failed",
            "error": str(e),
            "original_path": file_path
        }

