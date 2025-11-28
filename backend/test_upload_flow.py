#!/usr/bin/env python3
"""
Test script for document upload flow with CrewAI integration
"""

import asyncio
import io
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from services.DocumentUpload.document_upload_service import DocumentUploadService
from services.DocumentUpload.direct_upload_client import DirectDocumentUploadClient
from crew.crew_service import CrewAIService


async def test_upload_flow():
    """Test the complete document upload flow"""
    
    print("=" * 60)
    print("TESTING DOCUMENT UPLOAD FLOW WITH CREWAI")
    print("=" * 60)
    
    # Step 1: Initialize CrewAI Service
    print("\n[1/5] Initializing CrewAI Service...")
    try:
        crewai_service = CrewAIService()
        print("✓ CrewAI service initialized successfully")
        print(f"  - Agents: {len(crewai_service.crew.agents)}")
        print(f"  - Tasks: {len(crewai_service.crew.tasks)}")
    except Exception as e:
        print(f"✗ CrewAI initialization failed: {str(e)}")
        print("  Continuing without CrewAI...")
        crewai_service = None
    
    # Step 2: Initialize Upload Client
    print("\n[2/5] Initializing Upload Client...")
    upload_client = DirectDocumentUploadClient(
        storage_manager=None,
        crewai_service=crewai_service
    )
    print("✓ Upload client initialized")
    
    # Step 3: Initialize Upload Service
    print("\n[3/5] Initializing Upload Service...")
    upload_service = DocumentUploadService(client=upload_client)
    print("✓ Upload service initialized")
    
    # Step 4: Create test file
    print("\n[4/5] Creating test document...")
    test_content = b"This is a test I-9 document for employee verification."
    test_file = io.BytesIO(test_content)
    test_file.name = "test_i9_document.txt"
    document_type = "I9"
    user_id = "550e8400-e29b-41d4-a716-446655440000"
    print(f"✓ Test file created: {test_file.name} ({len(test_content)} bytes)")
    
    # Step 5: Upload document
    print("\n[5/5] Uploading document...")
    print(f"  - Document Type: {document_type}")
    print(f"  - User ID: {user_id}")
    
    result = await upload_service.upload_document(
        file=test_file,
        document_type=document_type,
        user_id=user_id
    )
    
    # Display results
    print("\n" + "=" * 60)
    print("UPLOAD RESULT")
    print("=" * 60)
    
    if hasattr(result, 'error_code'):
        print(f"✗ Upload Failed")
        print(f"  Error Code: {result.error_code}")
        print(f"  Error Message: {result.error_message}")
    else:
        print(f"✓ Upload Successful")
        print(f"  Document ID: {result.document_id}")
        print(f"  Status: {result.status}")
        print(f"  Message: {result.message}")
        
        if result.status == "processed":
            print("\n✓ CrewAI processing was executed")
        elif result.status == "uploaded":
            print("\n⚠️  CrewAI processing was skipped (service not available or failed)")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    
    return result


if __name__ == "__main__":
    result = asyncio.run(test_upload_flow())
    sys.exit(0 if not hasattr(result, 'error_code') else 1)

