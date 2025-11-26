#!/usr/bin/env python3
"""
Test script to trigger document upload and CrewAI processing
Usage: python3 scripts/test_document_upload.py [document_type] [user_id] [file_path]
"""

import sys
import os
import requests
import uuid
from pathlib import Path
from PIL import Image, ImageDraw
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

API_URL = "http://localhost:8000"


def create_test_image(file_path: str, document_type: str):
    """Create a test image file"""
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add text to image
    text = f"Test {document_type} Document\nGenerated for testing"
    try:
        # Try to use a default font
        draw.text((400, 300), text, fill='black', anchor='mm')
    except:
        # Fallback if font not available
        draw.text((400, 300), text, fill='black')
    
    img.save(file_path)
    print(f"✅ Created test image: {file_path}")


def check_server_health():
    """Check if server is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            print("✅ Server is running")
            return True
    except requests.exceptions.RequestException:
        pass
    
    print("⚠️  Server not running. Please start the server:")
    print("   cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    return False


def upload_document(file_path: str, document_type: str, user_id: str):
    """Upload document and trigger CrewAI processing"""
    print(f"\n📤 Uploading document...")
    print(f"   Document Type: {document_type}")
    print(f"   User ID: {user_id}")
    print(f"   File: {file_path}")
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'image/jpeg')}
            data = {
                'document_type': document_type,
                'user_id': user_id
            }
            
            response = requests.post(
                f"{API_URL}/api/v1/documents/upload",
                files=files,
                data=data,
                timeout=30
            )
        
        print(f"\n📥 Response (HTTP {response.status_code}):")
        
        if response.status_code == 200:
            result = response.json()
            print(json.dumps(result, indent=2))
            
            document_id = result.get('document_id')
            if document_id:
                print(f"\n📄 Document ID: {document_id}")
                print("\n⏳ CrewAI processing has been triggered...")
                print("   Check server logs for processing status")
                
                # Wait a bit and check status
                import time
                time.sleep(2)
                
                print("\n📊 Checking onboarding status...")
                status_response = requests.get(
                    f"{API_URL}/api/v1/onboarding/{user_id}/status"
                )
                if status_response.status_code == 200:
                    print(json.dumps(status_response.json(), indent=2))
            
            return True
        else:
            print(f"❌ Upload failed: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {str(e)}")
        return False


def main():
    """Main function"""
    # Parse arguments
    document_type = sys.argv[1] if len(sys.argv) > 1 else "I9"
    user_id = sys.argv[2] if len(sys.argv) > 2 else str(uuid.uuid4())
    file_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    print("=" * 50)
    print("Document Upload Test")
    print("=" * 50)
    
    # Check server
    if not check_server_health():
        sys.exit(1)
    
    # Create test file if needed
    if not file_path or not os.path.exists(file_path):
        file_path = f"/tmp/test_document_{document_type}.jpg"
        create_test_image(file_path, document_type)
    
    # Upload document
    success = upload_document(file_path, document_type, user_id)
    
    print("\n" + "=" * 50)
    print("Test Complete")
    print("=" * 50)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

