# How to Upload Files with curl

## Using Real Image Files

Yes, you should upload a **real image file** (`.jpg`, `.png`, etc.) when testing. The `@` symbol in curl tells it to read from a file path.

## Basic Syntax

```bash
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@/path/to/your/file.jpg" \
  -F "document_type=I9" \
  -F "user_id=test-user-id"
```

## Examples with Real File Paths

### Example 1: Upload from Current Directory
```bash
# If your image is in the current directory
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@document.jpg" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"
```

### Example 2: Upload from Desktop
```bash
# macOS/Linux
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@~/Desktop/my_document.jpg" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"

# Windows (Git Bash or WSL)
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@/c/Users/YourName/Desktop/my_document.jpg" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"
```

### Example 3: Upload from Downloads Folder
```bash
# macOS/Linux
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@~/Downloads/i9_form.jpg" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"
```

### Example 4: Upload with Full Absolute Path
```bash
# macOS/Linux
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@/Users/yourname/Documents/onboarding/i9.jpg" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"
```

## Step-by-Step Guide

### 1. Find Your Image File
```bash
# List files in current directory
ls *.jpg *.png

# Or search for image files
find ~ -name "*.jpg" -type f | head -5
```

### 2. Copy the Full Path
- **macOS/Linux**: Right-click file → "Get Info" → Copy path
- **Or use**: `realpath filename.jpg` to get full path

### 3. Use the Path in curl
```bash
# Replace /path/to/your/file.jpg with your actual path
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@/path/to/your/file.jpg" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"
```

## Important Notes

### The `@` Symbol
- `@` means "read from this file"
- **With @**: `file=@document.jpg` → Reads file from disk
- **Without @**: `file=document.jpg` → Sends the literal string "document.jpg" (wrong!)

### File Path Rules
- **Relative path**: `@document.jpg` (from current directory)
- **Home directory**: `@~/Desktop/file.jpg` (macOS/Linux)
- **Absolute path**: `@/Users/name/Documents/file.jpg` (full path)
- **Spaces in path**: Use quotes: `@"~/My Documents/file.jpg"`

### Valid Document Types
- `I9`
- `W4`
- `ID`
- `PASSPORT`
- `DRIVERSLICENSE`
- `SOCIALSECURITYCARD`

## Quick Test Commands

### Test with a Photo from Your Phone
```bash
# If you saved a photo to Desktop
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@~/Desktop/IMG_1234.jpg" \
  -F "document_type=ID" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"
```

### Test with Any Image
```bash
# Any .jpg, .png, .jpeg file will work
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@/path/to/any/image.jpg" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"
```

## Expected Response

If successful, you'll get:
```json
{
  "document_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "uploaded",
  "message": "Document uploaded successfully and processing started"
}
```

## Troubleshooting

### File Not Found Error
```bash
# Make sure the file path is correct
ls -la /path/to/your/file.jpg

# Use absolute path if relative doesn't work
curl -X POST ... -F "file=@$(pwd)/document.jpg" ...
```

### Permission Denied
```bash
# Make sure file is readable
chmod 644 document.jpg
```

### File Too Large
- Maximum file size: 10MB
- Check file size: `ls -lh document.jpg`
- Compress if needed: `convert document.jpg -quality 85 document_small.jpg`

