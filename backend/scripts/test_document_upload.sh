#!/bin/bash
# Test script to trigger document upload and CrewAI processing
# Usage: ./scripts/test_document_upload.sh [document_type] [user_id] [file_path]

# Default values
DOCUMENT_TYPE=${1:-"I9"}
USER_ID=${2:-"550e8400-e29b-41d4-a716-446655440000"}
FILE_PATH=${3:-""}

# API endpoint
API_URL="http://localhost:8000"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Document Upload Test${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if server is running
echo -e "${YELLOW}Checking if server is running...${NC}"
if ! curl -s "${API_URL}/health" > /dev/null; then
    echo -e "${YELLOW}⚠️  Server not running. Starting server...${NC}"
    echo "Please run: cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
    echo "Then run this script again."
    exit 1
fi

echo -e "${GREEN}✅ Server is running${NC}"
echo ""

# Create a test image if no file provided
if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    echo -e "${YELLOW}Creating test image file...${NC}"
    FILE_PATH="/tmp/test_document_${DOCUMENT_TYPE}.jpg"
    
    # Create a simple test image using ImageMagick or Python
    if command -v convert > /dev/null; then
        convert -size 800x600 xc:white -pointsize 24 -fill black -gravity center \
            -annotate +0+0 "Test ${DOCUMENT_TYPE} Document\n$(date)" \
            "$FILE_PATH"
    elif command -v python3 > /dev/null; then
        python3 << EOF
from PIL import Image, ImageDraw, ImageFont
import os

img = Image.new('RGB', (800, 600), color='white')
draw = ImageDraw.Draw(img)
text = f"Test {os.environ.get('DOCUMENT_TYPE', 'I9')} Document"
draw.text((400, 300), text, fill='black', anchor='mm')
img.save('$FILE_PATH')
EOF
    else
        echo -e "${YELLOW}⚠️  Cannot create test image. Please provide a file path.${NC}"
        echo "Usage: $0 [document_type] [user_id] [file_path]"
        exit 1
    fi
    echo -e "${GREEN}✅ Created test image: $FILE_PATH${NC}"
fi

echo ""
echo -e "${BLUE}Uploading document...${NC}"
echo "  Document Type: $DOCUMENT_TYPE"
echo "  User ID: $USER_ID"
echo "  File: $FILE_PATH"
echo ""

# Upload document
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${API_URL}/api/v1/documents/upload" \
    -F "file=@${FILE_PATH}" \
    -F "document_type=${DOCUMENT_TYPE}" \
    -F "user_id=${USER_ID}")

# Extract HTTP status code and body
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

echo -e "${BLUE}Response:${NC}"
if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✅ Upload successful (HTTP $HTTP_CODE)${NC}"
    echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
    
    # Extract document_id from response
    DOCUMENT_ID=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin).get('document_id', ''))" 2>/dev/null)
    
    if [ -n "$DOCUMENT_ID" ]; then
        echo ""
        echo -e "${BLUE}Document ID: ${DOCUMENT_ID}${NC}"
        echo ""
        echo -e "${YELLOW}Waiting for CrewAI processing...${NC}"
        sleep 3
        
        # Check document status (if we had an endpoint for it)
        echo -e "${BLUE}Checking onboarding status...${NC}"
        curl -s "${API_URL}/api/v1/onboarding/${USER_ID}/status" | python3 -m json.tool 2>/dev/null || echo "Status check failed"
    fi
else
    echo -e "${YELLOW}⚠️  Upload failed (HTTP $HTTP_CODE)${NC}"
    echo "$BODY"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Test Complete${NC}"
echo -e "${BLUE}========================================${NC}"

