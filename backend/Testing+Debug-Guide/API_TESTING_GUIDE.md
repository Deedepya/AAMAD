# API Testing Guide

## Prerequisites

1. **Server Status**: Ensure the server is running
   ```bash
   cd backend
   source venv/bin/activate
   python main.py
   ```
   Server runs on: `http://localhost:8000`

2. **Verify Server is Running**:
   ```bash
   curl http://localhost:8000/documents/health
   ```
   Expected: `{"status":"ok"}`

---

## Testing Methods

### Method 1: Using Swagger UI (Interactive Testing)

1. **Open Browser**: Navigate to `http://localhost:8000/docs`
2. **Explore Endpoints**: You'll see all available endpoints
3. **Test Health Endpoint**:
   - Click on `GET /documents/health`
   - Click "Try it out"
   - Click "Execute"
   - Verify response: `{"status":"ok"}`

4. **Test Upload Endpoint**:
   - Click on `POST /documents/upload`
   - Click "Try it out"
   - Fill in:
     - `file`: Click "Choose File" and select a test file
     - `document_type`: Enter "I9" (or other valid type)
     - `user_id`: Enter a UUID (e.g., "550e8400-e29b-41d4-a716-446655440000")
   - Click "Execute"
   - Review the response

---

### Method 2: Using cURL Commands

#### Step 1: Health Check Test

```bash
curl -X GET http://localhost:8000/documents/health
```

**Expected Response:**
```json
{"status":"ok"}
```

**Status Code:** `200 OK`

---

#### Step 2: Create a Test File

Create a small test file for upload testing:

```bash
# Create a simple test file
echo "This is a test document" > /tmp/test_document.txt

# Or use an existing image file
# cp /path/to/your/image.jpg /tmp/test_document.jpg
```

---

#### Step 3: Test Document Upload - Success Case

```bash
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@/tmp/test_document.txt" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000" \
  -v
```

**Expected Response (Success):**
```json
{
  "document_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "uploaded",
  "message": "Document uploaded successfully and processing started"
}
```

**Status Code:** `200 OK`

---

#### Step 4: Test Error Cases

**Test 4a: Missing File**
```bash
curl -X POST http://localhost:8000/documents/upload \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000" \
  -v
```

**Expected:** `400 Bad Request` with error message about missing file

---

**Test 4b: Invalid Document Type**
```bash
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@/tmp/test_document.txt" \
  -F "document_type=INVALID_TYPE" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000" \
  -v
```

**Expected:** `400 Bad Request` with error about invalid document type

**Valid document types:** `I9`, `W4`, `ID`, `PASSPORT`, `DRIVERSLICENSE`, `SOCIALSECURITYCARD`

---

**Test 4c: Empty user_id**
```bash
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@/tmp/test_document.txt" \
  -F "document_type=I9" \
  -F "user_id=" \
  -v
```

**Expected:** May return success (user_id is optional with default empty string) or validation error

---

**Test 4d: File Too Large**

Create a large file (if size validation is implemented):
```bash
# Create 11MB file
dd if=/dev/zero of=/tmp/large_file.txt bs=1M count=11

curl -X POST http://localhost:8000/documents/upload \
  -F "file=@/tmp/large_file.txt" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000" \
  -v
```

**Expected:** `400 Bad Request` if file size limit is enforced

---

#### Step 5: Test with Different Document Types

```bash
# Test with W4
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@/tmp/test_document.txt" \
  -F "document_type=W4" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"

# Test with ID
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@/tmp/test_document.txt" \
  -F "document_type=ID" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"

# Test with PASSPORT
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@/tmp/test_document.txt" \
  -F "document_type=PASSPORT" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"
```

---

### Method 3: Using Python Script

Create a test script `test_api.py`:

```python
import requests
import uuid

BASE_URL = "http://localhost:8000"

# Test 1: Health Check
print("Test 1: Health Check")
response = requests.get(f"{BASE_URL}/documents/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}\n")

# Test 2: Document Upload
print("Test 2: Document Upload")
test_file_content = b"This is a test document content"
files = {"file": ("test_document.txt", test_file_content, "text/plain")}
data = {
    "document_type": "I9",
    "user_id": str(uuid.uuid4())
}

response = requests.post(f"{BASE_URL}/documents/upload", files=files, data=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}\n")

# Test 3: Missing File
print("Test 3: Missing File (Error Case)")
data = {
    "document_type": "I9",
    "user_id": str(uuid.uuid4())
}
response = requests.post(f"{BASE_URL}/documents/upload", data=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}\n")
```

Run the script:
```bash
cd backend
source venv/bin/activate
pip install requests  # if not already installed
python test_api.py
```

---

### Method 4: Using HTTPie (if installed)

```bash
# Health check
http GET http://localhost:8000/documents/health

# Upload document
http -f POST http://localhost:8000/documents/upload \
  file@/tmp/test_document.txt \
  document_type=I9 \
  user_id=550e8400-e29b-41d4-a716-446655440000
```

---

## Quick Test Checklist

- [ ] Server starts without errors
- [ ] Health endpoint returns `{"status":"ok"}`
- [ ] Swagger UI is accessible at `/docs`
- [ ] Upload endpoint accepts valid file upload
- [ ] Upload endpoint rejects missing file
- [ ] Upload endpoint validates document_type
- [ ] Upload endpoint handles different document types
- [ ] Error responses are in JSON format
- [ ] Status codes are correct (200 for success, 400 for errors)

---

## Troubleshooting

### Server won't start
- Check if port 8000 is already in use: `lsof -i :8000`
- Verify virtual environment is activated
- Check for import errors in terminal output

### Connection refused
- Ensure server is running: `ps aux | grep "python main.py"`
- Check firewall settings
- Verify correct port (8000)

### Import errors
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

### File upload fails
- Check file path is correct
- Verify file exists: `ls -la /tmp/test_document.txt`
- Check file permissions
- Ensure file is not empty

---

## API Endpoints Summary

| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/documents/health` | GET | Health check | ✅ Working |
| `/documents/upload` | POST | Upload document | ✅ Working |
| `/docs` | GET | Swagger UI | ✅ Working |
| `/openapi.json` | GET | OpenAPI schema | ✅ Working |

---

## Next Steps

After successful testing:
1. Integrate with frontend application
2. Add authentication/authorization
3. Implement file storage (S3, local, etc.)
4. Add document processing pipeline
5. Set up monitoring and logging

