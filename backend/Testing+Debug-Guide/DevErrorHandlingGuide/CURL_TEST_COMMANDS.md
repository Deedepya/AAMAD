# CURL Test Commands for Document Upload Endpoint

## Server Setup

First, start the server:
```bash
cd backend/documentupload
source ../venv/bin/activate
python run_server.py
```

Or if you're in the backend directory:
```bash
cd backend
source venv/bin/activate
python -m documentupload.run_server
```

Server will run on: `http://localhost:8001`

---

## Test Cases - Failure Scenarios

### Test 1: Missing File (400 Bad Request)
**Expected:** Error about missing file

```bash
curl -X POST http://localhost:8001/api/v1/documents/upload \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000" \
  -v
```

**Expected Response:**
```json
{
  "detail": "No file provided. File is required."
}
```
**Status Code:** `400`

---

### Test 2: Missing document_type (400 Bad Request)
**Expected:** Error about missing document_type

```bash
curl -X POST http://localhost:8001/api/v1/documents/upload \
  -F "file=@/path/to/test.jpg" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000" \
  -v
```

**Expected Response:**
```json
{
  "detail": "document_type is required"
}
```
**Status Code:** `400`

---

### Test 3: Missing user_id (400 Bad Request)
**Expected:** Error about missing user_id

```bash
curl -X POST http://localhost:8001/api/v1/documents/upload \
  -F "file=@/path/to/test.jpg" \
  -F "document_type=I9" \
  -v
```

**Expected Response:**
```json
{
  "detail": "user_id is required"
}
```
**Status Code:** `400`

---

### Test 4: Invalid document_type (400 Bad Request)
**Expected:** Error about invalid document type

```bash
curl -X POST http://localhost:8001/api/v1/documents/upload \
  -F "file=@/path/to/test.jpg" \
  -F "document_type=INVALID_TYPE" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000" \
  -v
```

**Expected Response:**
```json
{
  "detail": "Invalid document_type: 'INVALID_TYPE'. Valid types: I9, W4, ID, PASSPORT, DRIVERSLICENSE, SOCIALSECURITYCARD"
}
```
**Status Code:** `400`

---

### Test 5: File Too Large (400 Bad Request)
**Expected:** Error about file size exceeding limit

First, create a large test file (11MB):
```bash
# Create a 11MB test file
dd if=/dev/zero of=/tmp/large_file.jpg bs=1M count=11
```

Then test:
```bash
curl -X POST http://localhost:8001/api/v1/documents/upload \
  -F "file=@/tmp/large_file.jpg" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000" \
  -v
```

**Expected Response:**
```json
{
  "detail": "File size (11.00MB) exceeds maximum (10MB)"
}
```
**Status Code:** `400`

---

### Test 6: Empty File (400 Bad Request)
**Expected:** Error about empty file

First, create an empty file:
```bash
touch /tmp/empty_file.jpg
```

Then test:
```bash
curl -X POST http://localhost:8001/api/v1/documents/upload \
  -F "file=@/tmp/empty_file.jpg" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000" \
  -v
```

**Expected Response:**
```json
{
  "detail": "File is empty"
}
```
**Status Code:** `400`

---

### Test 7: All Fields Valid (501 Not Implemented)
**Expected:** Error because endpoint is configured for failure testing only

```bash
curl -X POST http://localhost:8001/api/v1/documents/upload \
  -F "file=@/path/to/test.jpg" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000" \
  -v
```

**Expected Response:**
```json
{
  "detail": "Upload endpoint configured for failure testing only. Implement success logic to proceed."
}
```
**Status Code:** `501`

---

## Health Check

Test that the server is running:
```bash
curl http://localhost:8001/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "document_upload"
}
```

---

## Postman Collection

### Import to Postman

1. Open Postman
2. Click "Import"
3. Create a new request for each test case above

### Postman Request Setup

**Method:** `POST`
**URL:** `http://localhost:8001/api/v1/documents/upload`
**Body Type:** `form-data`

**Form Data Fields:**
- `file` (type: File) - Select a file
- `document_type` (type: Text) - Enter document type
- `user_id` (type: Text) - Enter user ID

### Postman Test Cases

1. **Missing File**
   - Remove `file` field
   - Keep `document_type` and `user_id`
   - Expected: 400 error

2. **Missing document_type**
   - Keep `file` and `user_id`
   - Remove `document_type` field
   - Expected: 400 error

3. **Missing user_id**
   - Keep `file` and `document_type`
   - Remove `user_id` field
   - Expected: 400 error

4. **Invalid document_type**
   - Set `document_type` to "INVALID"
   - Expected: 400 error with list of valid types

5. **File Too Large**
   - Upload a file larger than 10MB
   - Expected: 400 error with file size details

6. **Empty File**
   - Upload an empty file
   - Expected: 400 error

7. **All Valid (but endpoint not implemented)**
   - All fields valid
   - Expected: 501 error

---

## Quick Test Script

Save this as `test_failures.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:8001/api/v1/documents/upload"

echo "Test 1: Missing File"
curl -X POST "$BASE_URL" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000" \
  -w "\nStatus: %{http_code}\n\n"

echo "Test 2: Missing document_type"
curl -X POST "$BASE_URL" \
  -F "file=@test.jpg" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000" \
  -w "\nStatus: %{http_code}\n\n"

echo "Test 3: Missing user_id"
curl -X POST "$BASE_URL" \
  -F "file=@test.jpg" \
  -F "document_type=I9" \
  -w "\nStatus: %{http_code}\n\n"

echo "Test 4: Invalid document_type"
curl -X POST "$BASE_URL" \
  -F "file=@test.jpg" \
  -F "document_type=INVALID" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000" \
  -w "\nStatus: %{http_code}\n\n"
```

Make it executable:
```bash
chmod +x test_failures.sh
./test_failures.sh
```

