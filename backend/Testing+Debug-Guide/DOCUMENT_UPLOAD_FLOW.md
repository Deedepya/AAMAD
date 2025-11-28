# Document Upload Flow - Complete Process Documentation

## Overview

This document describes the complete flow of a `POST /documents/upload` request from API endpoint through CrewAI processing and back to the final response.

---

## 1. API Endpoint Receives Request

**Endpoint:** `POST /documents/upload`  
**Location:** `app_routes/document_routes.py`

### Input Received:
```json
{
  "file": UploadFile (multipart/form-data),
  "document_type": "I9" (form field, default: "I9"),
  "user_id": "550e8400-e29b-41d4-a716-446655440000" (form field)
}
```

### What It Does:
1. **Extracts form data** - Reads `document_type` and `user_id` from multipart form
2. **Reads file content** - Converts `UploadFile` to `BytesIO` object
3. **Sets filename** - Preserves original filename in BytesIO object
4. **Calls service** - Passes to `DocumentUploadService.upload_document()`

### Data Passed to Service:
```python
{
    "file": BytesIO(file_content),  # File as BytesIO with .name attribute
    "document_type": "I9",          # Uppercase validated
    "user_id": "550e8400-..."       # UUID format
}
```

---

## 2. Document Upload Service (Validation Layer)

**Location:** `services/DocumentUpload/document_upload_service.py`

### What It Does:
1. **Validates file exists** - Checks file is not None
2. **Validates file size** - Ensures file is not empty and ≤ 10MB
3. **Validates file object** - Checks file has seek/tell methods
4. **Validates document type** - Checks against valid types: `["I9", "W4", "ID", "PASSPORT", "DRIVERSLICENSE", "SOCIALSECURITYCARD"]`
5. **Validates user_id** - Ensures UUID format is valid
6. **Converts document_type** - Converts to uppercase

### Validation Checks:
- ✅ File exists and is not None
- ✅ File size > 0 bytes
- ✅ File size ≤ 10MB
- ✅ Document type is valid
- ✅ User ID is provided and valid UUID format

### If Validation Fails:
Returns `UploadFailure` with:
```python
{
    "error_code": 400,
    "error_message": "Specific validation error message"
}
```

### If Validation Passes:
Calls `client.documentUploadRequest()` with:
```python
{
    "file": BytesIO,           # Same file object (position reset)
    "document_type": "I9",     # Uppercase
    "user_id": "550e8400-..."  # UUID string
}
```

---

## 3. Direct Upload Client (Processing Layer)

**Location:** `services/DocumentUpload/direct_upload_client.py`

### What It Does:
1. **Generates document_id** - Creates UUID: `"4b8a47f2-f713-4e24-9097-9f71e055b999"`
2. **Saves to storage** (if storage_manager available) - Currently skipped (storage_manager=None)
3. **Processes with CrewAI** (if crewai_service available) - Main processing step
4. **Returns result** - UploadSuccess or UploadFailure

### Data Handed to CrewAI:
```python
{
    "file": BytesIO,                    # File content (position reset to 0)
    "document_type": "I9",              # Document type
    "user_id": "550e8400-...",          # User identifier
    "document_id": "4b8a47f2-..."       # Generated document ID
}
```

### If CrewAI Processing Succeeds:
Returns `UploadSuccess`:
```python
{
    "document_id": "4b8a47f2-...",
    "status": "processed",
    "message": "Document uploaded and processed successfully. Validation: valid"
}
```

### If CrewAI Processing Fails:
Returns `UploadSuccess` (graceful degradation):
```python
{
    "document_id": "4b8a47f2-...",
    "status": "uploaded",
    "message": "Document uploaded successfully (processing skipped due to error)"
}
```

### If No CrewAI Service:
Returns `UploadSuccess`:
```python
{
    "document_id": "4b8a47f2-...",
    "status": "uploaded",
    "message": "Document uploaded successfully"
}
```

---

## 4. CrewAI Service (Agent Orchestration)

**Location:** `crew/crew_service.py`

### What It Does:
1. **Saves file temporarily** - Writes BytesIO to temp file: `/tmp/{document_id}.jpg`
2. **Prepares context** - Creates context string with file path, document_id, document_type, user_id
3. **Updates task description** - Injects context into first task (process_document_upload)
4. **Executes crew** - Calls `crew.kickoff()` to run all agents and tasks
5. **Parses results** - Extracts structured data from crew output
6. **Cleans up** - Removes temporary file
7. **Returns result** - `DocumentProcessingResult` object

### Context Passed to Crew:
```
Document Processing Context:
- File Path: /tmp/4b8a47f2-f713-4e24-9097-9f71e055b999.jpg
- Document ID: 4b8a47f2-f713-4e24-9097-9f71e055b999
- Document Type: I9
- User ID: 550e8400-e29b-41d4-a716-446655440000
- Filename: i-94-Test.png
```

### Crew Execution:
1. **Task 1: process_document_upload** (Document Processing Agent)
   - Uses tools: `ocr_tool`, `document_validation_tool`, `image_processing_tool`
   - Extracts text, validates format, processes image
   - Output: Extracted document data with validation status

2. **Task 2: verify_compliance** (Compliance Agent)
   - Uses tools: `compliance_validation_tool`, `audit_logging_tool`, `hris_integration_tool`
   - Verifies regulatory compliance, creates audit log
   - Output: Compliance status and audit log

### Crew Returns:
Raw result from `crew.kickoff()` (can be string, dict, or CrewAI result object)

### Parsed Result Returned:
```python
DocumentProcessingResult(
    document_id="4b8a47f2-...",
    document_type="I9",
    extracted_data={
        "document_type": "I9",
        "extracted_data": {...},
        "validation_status": "valid|invalid|needs-review",
        "confidence_scores": {...}
    },
    validation_status="valid",
    compliance_status="compliant",
    compliance_data={
        "compliance_status": "compliant",
        "compliance_type": "I9",
        "audit_log": {...}
    }
)
```

---

## 5. Tools Execution (Within CrewAI Agents)

### Tool 1: OCR Tool
**Input:** `file_path` (string)  
**Output:** Extracted text from document  
**What it does:** Uses pytesseract/PIL to extract text from image

### Tool 2: Document Validation Tool
**Input:** `file_path` (string), `document_type` (string)  
**Output:** JSON validation result  
**What it does:** Validates file size, format, content requirements

### Tool 3: Image Processing Tool
**Input:** `file_path` (string)  
**Output:** Processing result  
**What it does:** Optimizes image for OCR (resize, enhance contrast, etc.)

### Tool 4: Compliance Validation Tool
**Input:** `document_type` (string), `extracted_data` (string/JSON)  
**Output:** Compliance validation JSON  
**What it does:** Validates regulatory compliance (I-9, W-4 requirements)

### Tool 5: Audit Logging Tool
**Input:** `document_id`, `user_id`, `action`, `details`  
**Output:** Audit log entry JSON  
**What it does:** Creates audit trail entry

### Tool 6: HRIS Integration Tool
**Input:** `user_id`, `document_type`, `document_data`  
**Output:** Sync status JSON (stub)  
**What it does:** Syncs with HRIS system (stubbed for MVP)

---

## 6. Response Flow Back to API

### CrewAI Service → Direct Upload Client:
```python
DocumentProcessingResult(
    document_id="4b8a47f2-...",
    document_type="I9",
    extracted_data={...},
    validation_status="valid",
    compliance_status="compliant",
    compliance_data={...}
)
```

### Direct Upload Client → Document Upload Service:
```python
UploadSuccess(
    document_id="4b8a47f2-...",
    status="processed",  # or "uploaded" if CrewAI failed
    message="Document uploaded and processed successfully. Validation: valid"
)
```

### Document Upload Service → API Route:
```python
UploadSuccess(
    document_id="4b8a47f2-...",
    status="processed",
    message="Document uploaded and processed successfully. Validation: valid"
)
```

---

## 7. Final API Response

**Location:** `app_routes/document_routes.py`

### Success Response (200 OK):
```json
{
    "document_id": "4b8a47f2-f713-4e24-9097-9f71e055b999",
    "status": "processed",
    "message": "Document uploaded and processed successfully. Validation: valid"
}
```

### Error Response (400 Bad Request):
```json
{
    "detail": "No file provided"
}
```
or
```json
{
    "detail": "File size (11.00MB) exceeds maximum (10MB)"
}
```
or
```json
{
    "detail": "Invalid document type. Valid types: I9, W4, ID, PASSPORT, DRIVERSLICENSE, SOCIALSECURITYCARD"
}
```
or
```json
{
    "detail": "User ID is required"
}
```

### Error Response (500 Internal Server Error):
```json
{
    "detail": "Internal error: [error message]"
}
```

---

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ 1. POST /documents/upload                                   │
│    Input: file, document_type, user_id                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. DocumentUploadService.upload_document()                  │
│    - Validates file (size, empty, format)                   │
│    - Validates document_type                                │
│    - Validates user_id (UUID format)                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼ (if validation passes)
┌─────────────────────────────────────────────────────────────┐
│ 3. DirectDocumentUploadClient.documentUploadRequest()      │
│    - Generates document_id (UUID)                           │
│    - Saves file to temp storage (if storage_manager)        │
│    - Calls CrewAI service (if available)                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼ (if crewai_service available)
┌─────────────────────────────────────────────────────────────┐
│ 4. CrewAIService.process_document()                         │
│    - Saves file to /tmp/{document_id}.jpg                   │
│    - Prepares context with file_path, document_id, etc.      │
│    - Updates task description with context                   │
│    - Executes crew.kickoff()                                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. CrewAI Crew Execution                                     │
│    ┌──────────────────────────────────────────────┐         │
│    │ Task 1: process_document_upload              │         │
│    │ Agent: Document Processing Specialist        │         │
│    │ Tools: ocr_tool, document_validation_tool,   │         │
│    │        image_processing_tool                 │         │
│    │ Output: Extracted data + validation status   │         │
│    └──────────────────┬───────────────────────────┘         │
│                       │                                      │
│                       ▼                                      │
│    ┌──────────────────────────────────────────────┐         │
│    │ Task 2: verify_compliance                     │         │
│    │ Agent: Compliance Verification Specialist    │         │
│    │ Tools: compliance_validation_tool,            │         │
│    │        audit_logging_tool,                    │         │
│    │        hris_integration_tool                  │         │
│    │ Output: Compliance status + audit log         │         │
│    └──────────────────────────────────────────────┘         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. CrewAI Returns Result                                     │
│    - Raw result from crew.kickoff()                          │
│    - Parsed into DocumentProcessingResult                    │
│    - Temp file cleaned up                                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. DirectUploadClient Returns                                │
│    UploadSuccess(                                            │
│      document_id="...",                                      │
│      status="processed",                                     │
│      message="Document uploaded and processed..."             │
│    )                                                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. API Returns Final Response                                │
│    {                                                         │
│      "document_id": "...",                                   │
│      "status": "processed",                                  │
│      "message": "Document uploaded and processed..."         │
│    }                                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Transformation Summary

| Layer | Input | Output |
|-------|-------|--------|
| **API Route** | `UploadFile`, form fields | `BytesIO`, `document_type`, `user_id` |
| **Upload Service** | `BytesIO`, `document_type`, `user_id` | Validated inputs → `UploadResult` |
| **Upload Client** | `BytesIO`, `document_type`, `user_id` | `document_id` + calls CrewAI → `UploadSuccess` |
| **CrewAI Service** | `BytesIO`, `document_type`, `user_id`, `document_id` | Temp file + context → Crew execution → `DocumentProcessingResult` |
| **CrewAI Crew** | Context string with file_path | Agent execution → Raw result |
| **Tools** | File paths, document data | Tool-specific outputs (text, validation, compliance) |
| **CrewAI Service** | Raw crew result | Parsed `DocumentProcessingResult` |
| **Upload Client** | `DocumentProcessingResult` | `UploadSuccess` with status/message |
| **API Route** | `UploadSuccess` | JSON response to client |

---

## Key Points

1. **Validation happens first** - File, document_type, and user_id are validated before any processing
2. **CrewAI is optional** - If CrewAI fails or isn't available, upload still succeeds
3. **File is saved temporarily** - For CrewAI tools to access, then cleaned up
4. **Two agents work sequentially** - Document Processing → Compliance Verification
5. **Tools are called by agents** - Agents use tools to perform actual work
6. **Results are parsed** - CrewAI output is parsed into structured format
7. **Final response is simple** - API returns document_id, status, and message (not full processing details)

---

## Example Complete Flow

**Request:**
```bash
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@document.jpg" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"
```

**Processing:**
1. API receives file, validates form data
2. Service validates file size, type, user_id
3. Client generates document_id: `4b8a47f2-f713-4e24-9097-9f71e055b999`
4. CrewAI saves file to `/tmp/4b8a47f2-f713-4e24-9097-9f71e055b999.jpg`
5. Document Processing Agent extracts text, validates document
6. Compliance Agent verifies I-9 compliance, creates audit log
7. CrewAI returns processing results
8. Results parsed into `DocumentProcessingResult`
9. Client creates `UploadSuccess` with status "processed"
10. API returns JSON response

**Response:**
```json
{
    "document_id": "4b8a47f2-f713-4e24-9097-9f71e055b999",
    "status": "processed",
    "message": "Document uploaded and processed successfully. Validation: valid"
}
```

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-28

