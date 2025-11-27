# User ID Guide for Document Upload

## Quick Answer

**You can use ANY valid UUID string!** The backend will automatically create the user if it doesn't exist.

## Format Required

The `user_id` must be in **UUID format** (Universally Unique Identifier):

```
550e8400-e29b-41d4-a716-446655440000
```

Format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` (32 hex digits in 5 groups)

## Options for user_id

### Option 1: Use a Fixed Test User ID (Recommended for Testing)

Use the same user_id for all your test uploads:

```bash
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@document.jpg" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"
```

**Benefits:**
- All documents will be associated with the same user
- Easy to track all uploads for one test user
- Can check status: `GET /api/v1/onboarding/550e8400-e29b-41d4-a716-446655440000/status`

### Option 2: Generate a New UUID Each Time

**On macOS/Linux:**
```bash
# Generate a new UUID
uuidgen
# Output: 550e8400-e29b-41d4-a716-446655440000

# Use it in curl
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@document.jpg" \
  -F "document_type=I9" \
  -F "user_id=$(uuidgen)"
```

**On Python:**
```python
import uuid
print(str(uuid.uuid4()))
# Output: 550e8400-e29b-41d4-a716-446655440000
```

**Online:**
- Visit: https://www.uuidgenerator.net/
- Copy a UUID and use it

### Option 3: Use Any Valid UUID String

You can literally make one up (as long as it's valid format):

```bash
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@document.jpg" \
  -F "document_type=I9" \
  -F "user_id=12345678-1234-1234-1234-123456789abc"
```

## What Happens Behind the Scenes

Looking at the code (lines 132-144 in `main.py`):

1. **Backend checks if user exists:**
   ```python
   user = db.query(User).filter(User.id == user_id).first()
   ```

2. **If user doesn't exist, it creates one automatically:**
   ```python
   if not user:
       user = User(
           id=uuid.UUID(user_id),
           email=f"user_{user_id}@example.com",  # Placeholder email
           first_name="",
           last_name=""
       )
       db.add(user)
       db.commit()
   ```

3. **Document is linked to this user**

## Examples

### Example 1: First Upload (User Created Automatically)
```bash
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@i9.jpg" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"
```

**Result:** User is created automatically, document is uploaded

### Example 2: Second Upload (Same User)
```bash
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@w4.jpg" \
  -F "document_type=W4" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"
```

**Result:** Same user (already exists), new document added

### Example 3: Check User's Status
```bash
curl http://localhost:8000/api/v1/onboarding/550e8400-e29b-41d4-a716-446655440000/status
```

**Result:** Shows all documents and tasks for this user

## Common UUIDs for Testing

You can use these pre-made UUIDs:

```bash
# Test User 1
user_id=550e8400-e29b-41d4-a716-446655440000

# Test User 2
user_id=660e8400-e29b-41d4-a716-446655440001

# Test User 3
user_id=770e8400-e29b-41d4-a716-446655440002
```

## Invalid Formats (Will Cause Errors)

❌ **Wrong:**
```bash
-F "user_id=test-user"           # Not UUID format
-F "user_id=123"                 # Not UUID format
-F "user_id=john.doe@email.com" # Not UUID format
```

✅ **Correct:**
```bash
-F "user_id=550e8400-e29b-41d4-a716-446655440000"  # Valid UUID
```

## Quick Reference

**For testing, just use:**
```bash
-F "user_id=550e8400-e29b-41d4-a716-446655440000"
```

This will work every time, and the user will be created automatically if it doesn't exist!

