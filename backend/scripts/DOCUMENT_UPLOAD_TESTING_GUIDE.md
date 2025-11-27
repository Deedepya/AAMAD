# Document Upload Testing Guide

This guide provides step-by-step instructions to verify that documents uploaded from the iOS app are received by the server's API endpoint and that the server returns the expected response.

## Overview

The backend API endpoint is:
- **Endpoint**: `POST /api/v1/documents/upload`
- **Location**: `backend/main.py` (lines 109-212)
- **Expected Response**: JSON with `document_id`, `status`, and `message`

**Note**: The iOS app currently uses a mock implementation. You'll need to update it to connect to the real backend (see Step 4).

---

## Step 1: Verify Server is Running

### 1.1 Check Server Health

```bash
# From backend directory
cd backend

# Check if server is running
curl http://localhost:8000/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

### 1.2 Start Server (if not running)

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Look for**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

---

## Step 2: Test Backend Endpoint Directly

### 2.1 Using the Test Script (Recommended)

```bash
# From backend directory
cd backend

# Activate virtual environment
source venv/bin/activate

# Run test script
python scripts/test_document_upload.py I9 test-user-123

# Or with custom file
python scripts/test_document_upload.py I9 test-user-123 /path/to/your/image.jpg
```

**Expected Output**:
```
✅ Server is running
📤 Uploading document...
   Document Type: I9
   User ID: test-user-123
   File: /tmp/test_document_I9.jpg

📥 Response (HTTP 200):
{
  "document_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "uploaded",
  "message": "Document uploaded successfully and processing started"
}
```

### 2.2 Using curl (Manual Testing)

```bash
# Basic test with auto-generated test image
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@/path/to/your/document.jpg" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"
```

**Expected Response**:
```json
{
  "document_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "uploaded",
  "message": "Document uploaded successfully and processing started"
}
```

### 2.3 Valid Document Types

The server accepts these document types (case-insensitive):
- `I9`
- `W4`
- `ID`
- `PASSPORT`
- `DRIVERSLICENSE`
- `SOCIALSECURITYCARD`

**Example with different types**:
```bash
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@document.jpg" \
  -F "document_type=ID" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"
```

---

## Step 3: Check Server Logs

### 3.1 Monitor Server Logs in Real-Time

When the server is running, watch the terminal output for:

**Successful Upload Logs**:
```
INFO:     Document uploaded: 660e8400-e29b-41d4-a716-446655440001 (type: I9, user: test-user-123)
INFO:     Starting CrewAI crew execution for document 660e8400-e29b-41d4-a716-446655440001
```

**Error Logs** (if any):
```
ERROR:    Document upload error: <error message>
```

### 3.2 Check Database Records

```bash
# If using SQLite (default)
cd backend
sqlite3 onboarding.db

# Query documents table
SELECT id, user_id, document_type, status, created_at FROM documents ORDER BY created_at DESC LIMIT 5;

# Exit SQLite
.quit
```

---

## Step 4: Connect iOS App to Real Backend

**Current Status**: The iOS app uses a mock implementation. You need to update it to call the real API.

### 4.1 Update DocumentService.swift

The iOS app's `DocumentService.swift` currently has:
- Mock URL: `https://api.onboarding.example.com/v1`
- Mock implementation that doesn't make real network calls

**Required Changes**:

1. **Update Base URL** (line 45):
```swift
// Change from:
private let baseURL = "https://api.onboarding.example.com/v1" // Mock API URL

// To (for local development):
private let baseURL = "http://localhost:8000/api/v1"

// Or (for network access from iOS device/simulator):
private let baseURL = "http://<YOUR_MAC_IP>:8000/api/v1"
// Example: "http://192.168.1.100:8000/api/v1"
```

2. **Implement Real Network Call** (replace lines 71-94):

```swift
// Replace the mock implementation with:
func uploadDocument(
    _ image: UIImage,
    documentType: DocumentType,
    progressHandler: @escaping (Double) -> Void
) async throws -> Document {
    // Validate image
    guard validateImageResolution(image) else {
        throw DocumentServiceError.invalidImage
    }
    
    // Compress image if needed
    let imageData = try compressImage(image, maxSizeMB: maxFileSizeMB)
    
    // Validate file size
    guard validateFileSize(imageData, maxSizeMB: maxFileSizeMB) else {
        throw DocumentServiceError.fileSizeExceeded
    }
    
    // Extract metadata
    let metadata = extractImageMetadata(image)
    
    // Create multipart form data request
    let url = URL(string: "\(baseURL)/documents/upload")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    
    // Create boundary for multipart form
    let boundary = UUID().uuidString
    request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
    
    // Build multipart body
    var body = Data()
    
    // Add file
    body.append("--\(boundary)\r\n".data(using: .utf8)!)
    body.append("Content-Disposition: form-data; name=\"file\"; filename=\"document.jpg\"\r\n".data(using: .utf8)!)
    body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
    body.append(imageData)
    body.append("\r\n".data(using: .utf8)!)
    
    // Add document_type
    body.append("--\(boundary)\r\n".data(using: .utf8)!)
    body.append("Content-Disposition: form-data; name=\"document_type\"\r\n\r\n".data(using: .utf8)!)
    body.append(documentType.rawValue.uppercased().data(using: .utf8)!)
    body.append("\r\n".data(using: .utf8)!)
    
    // Add user_id (you'll need to get this from authentication)
    let userId = UUID() // TODO: Get from auth system
    body.append("--\(boundary)\r\n".data(using: .utf8)!)
    body.append("Content-Disposition: form-data; name=\"user_id\"\r\n\r\n".data(using: .utf8)!)
    body.append(userId.uuidString.data(using: .utf8)!)
    body.append("\r\n".data(using: .utf8)!)
    
    // Close boundary
    body.append("--\(boundary)--\r\n".data(using: .utf8)!)
    
    request.httpBody = body
    
    // Simulate progress (you can implement real progress tracking with URLSessionDelegate)
    progressHandler(0.3)
    
    // Make network request
    do {
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw DocumentServiceError.networkError("Invalid response")
        }
        
        progressHandler(0.8)
        
        guard httpResponse.statusCode == 200 else {
            let errorMessage = String(data: data, encoding: .utf8) ?? "Upload failed"
            throw DocumentServiceError.uploadFailed(errorMessage)
        }
        
        // Parse response
        let json = try JSONDecoder().decode(UploadResponse.self, from: data)
        
        progressHandler(1.0)
        
        // Convert to Document model
        return Document(
            id: UUID(uuidString: json.documentId) ?? UUID(),
            userId: userId,
            documentType: documentType,
            status: .processing, // Will be updated when status endpoint is called
            fileName: "\(documentType.rawValue.replacingOccurrences(of: " ", with: "_")).jpg",
            fileSize: imageData.count,
            createdAt: Date(),
            resolution: metadata
        )
    } catch {
        throw DocumentServiceError.networkError(error.localizedDescription)
    }
}

// Add response model
struct UploadResponse: Codable {
    let documentId: String
    let status: String
    let message: String
    
    enum CodingKeys: String, CodingKey {
        case documentId = "document_id"
        case status
        case message
    }
}
```

### 4.2 Get Your Mac's IP Address (for iOS Simulator/Device)

```bash
# macOS
ifconfig | grep "inet " | grep -v 127.0.0.1

# Or more specific
ipconfig getifaddr en0  # For Wi-Fi
ipconfig getifaddr en1  # For Ethernet
```

Use this IP in the baseURL (e.g., `http://192.168.1.100:8000/api/v1`)

### 4.3 Test from iOS App

1. Build and run the iOS app
2. Select a document type
3. Capture/select an image
4. Upload the document
5. Check server logs to see the request arrive
6. Verify the response in the app

---

## Step 5: Verify Expected Response Format

### 5.1 Response Structure

The server returns this JSON structure:

```json
{
  "document_id": "string (UUID)",
  "status": "uploaded",
  "message": "Document uploaded successfully and processing started"
}
```

### 5.2 Response Validation Checklist

- [ ] HTTP Status Code: `200 OK`
- [ ] Response contains `document_id` (UUID format)
- [ ] Response contains `status` field with value `"uploaded"`
- [ ] Response contains `message` field
- [ ] Server logs show document was saved
- [ ] Database contains new document record

### 5.3 Error Response Examples

**File Too Large** (HTTP 400):
```json
{
  "detail": "File size (12.5MB) exceeds maximum (10MB)"
}
```

**Invalid Document Type** (HTTP 400):
```json
{
  "detail": "Invalid document type. Valid types: I9, W4, ID, PASSPORT, DRIVERSLICENSE, SOCIALSECURITYCARD"
}
```

**Server Error** (HTTP 500):
```json
{
  "detail": "Upload failed: <error message>"
}
```

---

## Step 6: End-to-End Testing Workflow

### 6.1 Complete Test Sequence

1. **Start Server**:
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Test Backend Directly** (verify endpoint works):
   ```bash
   python scripts/test_document_upload.py I9 test-user-123
   ```

3. **Update iOS App** (connect to real backend - see Step 4)

4. **Test from iOS App**:
   - Open iOS app
   - Upload a document
   - Watch server logs
   - Verify response in app

5. **Verify Database**:
   ```bash
   sqlite3 onboarding.db "SELECT * FROM documents ORDER BY created_at DESC LIMIT 1;"
   ```

### 6.2 Troubleshooting

**Issue**: iOS app can't connect to server
- **Solution**: Use your Mac's IP address instead of `localhost`
- **Solution**: Ensure server is bound to `0.0.0.0` (not `127.0.0.1`)
- **Solution**: Check firewall settings

**Issue**: CORS errors
- **Solution**: CORS is already configured in `main.py` (line 47-53) to allow all origins

**Issue**: File not received
- **Solution**: Check server logs for errors
- **Solution**: Verify multipart form data format in iOS request
- **Solution**: Test with curl first to isolate issue

**Issue**: Wrong response format
- **Solution**: Check `DocumentUploadResponse` model in `main.py` (lines 79-82)
- **Solution**: Verify JSON keys match (`document_id` not `documentId`)

---

## Quick Reference

### Test Commands

```bash
# Health check
curl http://localhost:8000/health

# Upload test
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@test.jpg" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"

# Using test script
python scripts/test_document_upload.py I9 test-user-123

# Check database
sqlite3 onboarding.db "SELECT * FROM documents;"
```

### Expected Response

```json
{
  "document_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "uploaded",
  "message": "Document uploaded successfully and processing started"
}
```

---

## Next Steps

After verifying the upload works:

1. **Implement Status Checking**: Add endpoint to check document processing status
2. **Add Error Handling**: Improve error messages and retry logic
3. **Add Progress Tracking**: Implement real upload progress from URLSession
4. **Add Authentication**: Replace placeholder user_id with real authentication

