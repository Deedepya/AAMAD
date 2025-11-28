#!/usr/bin/env python3
"""
Detailed test script to capture complete document upload flow
"""

import asyncio
import io
import sys
import os
import logging

# Configure logging to see all details
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.DocumentUpload.document_upload_service import DocumentUploadService
from services.DocumentUpload.direct_upload_client import DirectDocumentUploadClient
from crew.crew_service import CrewAIService

async def test_detailed_flow():
    """Test with detailed logging of each step"""
    
    file_path = '/Users/dedeepyareddysalla/Documents/Developer/AgenticAI/AAMAD/backend/Testing+Debug-Guide/i-94-Test.png'
    if not os.path.exists(file_path):
        file_path = '/Users/dedeepyareddysalla/Desktop/i-94-Test.png'
    
    if not os.path.exists(file_path):
        print('❌ File not found')
        return
    
    print('=' * 80)
    print('DETAILED DOCUMENT UPLOAD FLOW TEST')
    print('=' * 80)
    print(f'\nFile: {file_path}')
    print(f'File Size: {os.path.getsize(file_path)} bytes')
    print(f'Document Type: I9')
    print(f'User ID: 550e8400-e29b-41d4-a716-446655440000\n')
    
    # Step 1: Initialize CrewAI Service
    print('-' * 80)
    print('[STEP 1] Initializing CrewAI Service')
    print('-' * 80)
    try:
        crewai_service = CrewAIService()
        print(f'✅ CrewAI service initialized')
        print(f'   - Agents: {len(crewai_service.crew.agents)}')
        for agent in crewai_service.crew.agents:
            print(f'     • {agent.role} (tools: {len(agent.tools)})')
        print(f'   - Tasks: {len(crewai_service.crew.tasks)}')
        for task in crewai_service.crew.tasks:
            print(f'     • {task.description[:60]}...')
    except Exception as e:
        print(f'❌ CrewAI initialization failed: {str(e)}')
        crewai_service = None
    
    # Step 2: Initialize Upload Client
    print('\n' + '-' * 80)
    print('[STEP 2] Initializing Upload Client')
    print('-' * 80)
    upload_client = DirectDocumentUploadClient(
        storage_manager=None,
        crewai_service=crewai_service
    )
    print('✅ Upload client initialized')
    print(f'   - CrewAI service: {"Available" if crewai_service else "Not available"}')
    
    # Step 3: Initialize Upload Service
    print('\n' + '-' * 80)
    print('[STEP 3] Initializing Upload Service')
    print('-' * 80)
    upload_service = DocumentUploadService(client=upload_client)
    print('✅ Upload service initialized')
    
    # Step 4: Read file
    print('\n' + '-' * 80)
    print('[STEP 4] Reading File')
    print('-' * 80)
    with open(file_path, 'rb') as f:
        file_content = f.read()
    
    test_file = io.BytesIO(file_content)
    test_file.name = os.path.basename(file_path)
    print(f'✅ File read: {test_file.name} ({len(file_content)} bytes)')
    
    # Step 5: Upload document
    print('\n' + '-' * 80)
    print('[STEP 5] Uploading Document via Service')
    print('-' * 80)
    print('Input to DocumentUploadService.upload_document():')
    print(f'   - file: BytesIO ({len(file_content)} bytes)')
    print(f'   - document_type: "I9"')
    print(f'   - user_id: "550e8400-e29b-41d4-a716-446655440000"')
    
    result = await upload_service.upload_document(
        file=test_file,
        document_type='I9',
        user_id='550e8400-e29b-41d4-a716-446655440000'
    )
    
    # Display results
    print('\n' + '=' * 80)
    print('FINAL RESULT')
    print('=' * 80)
    if hasattr(result, 'error_code'):
        print(f'❌ Upload Failed')
        print(f'   Error Code: {result.error_code}')
        print(f'   Error Message: {result.error_message}')
    else:
        print(f'✅ Upload Successful')
        print(f'   Document ID: {result.document_id}')
        print(f'   Status: {result.status}')
        print(f'   Message: {result.message}')
        
        if result.status == "processed":
            print('\n✅ CrewAI processing was executed')
        elif result.status == "uploaded":
            print('\n⚠️  CrewAI processing was skipped')
    
    print('\n' + '=' * 80)
    return result

if __name__ == "__main__":
    asyncio.run(test_detailed_flow())

