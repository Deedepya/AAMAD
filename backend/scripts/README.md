# Test Scripts

Scripts to test and trigger the document upload and CrewAI processing.

## Quick Start

### Option 1: Python Script (Recommended)

```bash
cd backend
python3 scripts/test_document_upload.py
```

With custom parameters:
```bash
python3 scripts/test_document_upload.py I9 "550e8400-e29b-41d4-a716-446655440000" /path/to/document.jpg
```

### Option 2: Shell Script

```bash
cd backend
./scripts/test_document_upload.sh
```

With custom parameters:
```bash
./scripts/test_document_upload.sh I9 "550e8400-e29b-41d4-a716-446655440000" /path/to/document.jpg
```

### Option 3: Direct curl Command

```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@/path/to/document.jpg" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"
```

## Prerequisites

1. **Start the server:**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Install dependencies:**
   ```bash
   pip install requests pillow
   ```

## Parameters

- **document_type**: I9, W4, ID, PASSPORT, DRIVERSLICENSE, SOCIALSECURITYCARD (default: I9)
- **user_id**: UUID string (default: random UUID)
- **file_path**: Path to document image (default: creates test image)

## Examples

### Test with I-9 document
```bash
python3 scripts/test_document_upload.py I9
```

### Test with W-4 document
```bash
python3 scripts/test_document_upload.py W4
```

### Test with specific user and file
```bash
python3 scripts/test_document_upload.py I9 "550e8400-e29b-41d4-a716-446655440000" ~/Documents/i9_form.jpg
```

## What Happens

1. Script checks if server is running
2. Creates test image if no file provided
3. Uploads document to `/api/v1/documents/upload`
4. Server triggers CrewAI crew processing:
   - Document Processing Agent (OCR, validation)
   - Compliance Agent (I-9/W-4 checks)
   - Notification Agent (status updates)
5. Returns document ID and status
6. Checks onboarding status

## Monitoring

Watch server logs to see CrewAI processing:
```bash
# In another terminal
tail -f logs/crewai-execution.log
```

Or watch the server output for processing logs.

