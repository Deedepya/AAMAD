"""
Run the document upload FastAPI server for testing
"""

import uvicorn
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

if __name__ == "__main__":
    uvicorn.run(
        "documentupload.fastapi_document_upload:app",
        host="0.0.0.0",
        port=8001,  # Different port to avoid conflicts
        reload=True
    )

