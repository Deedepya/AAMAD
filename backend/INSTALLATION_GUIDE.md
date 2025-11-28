# Installation Guide - CrewAI Dependencies

This guide will help you install all required libraries for CrewAI tools to work 100%.

---

## Step 1: Install Tesseract OCR Binary (System Dependency)

Tesseract is the OCR engine that pytesseract uses. It needs to be installed at the system level.

### For macOS (using Homebrew):

```bash
# Install Homebrew if you don't have it
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install tesseract
brew install tesseract

# Verify installation
tesseract --version
```

**Expected output:** Should show tesseract version (e.g., `tesseract 5.x.x`)

### For Linux (Ubuntu/Debian):

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
tesseract --version
```

### For Linux (CentOS/RHEL):

```bash
sudo yum install tesseract
tesseract --version
```

---

## Step 2: Install Python Dependencies

Navigate to the backend directory and activate your virtual environment:

```bash
cd /Users/dedeepyareddysalla/Documents/Developer/AgenticAI/AAMAD/backend
source venv/bin/activate
```

### Install all required packages:

```bash
# Install from requirements.txt (includes pytesseract, Pillow, etc.)
pip install -r requirements.txt
```

### Or install specific packages individually:

```bash
# OCR and image processing
pip install pytesseract==0.3.10
pip install Pillow==10.1.0

# CrewAI framework (if not already installed)
pip install crewai==0.28.8
pip install crewai-tools==0.1.6
pip install langchain==0.1.0
pip install langchain-openai==0.0.2
```

---

## Step 3: Verify Installation

Run this verification script:

```bash
cd /Users/dedeepyareddysalla/Documents/Developer/AgenticAI/AAMAD/backend
source venv/bin/activate
python -c "
import sys
print('=' * 60)
print('DEPENDENCY VERIFICATION')
print('=' * 60)
print()

# Check pytesseract
try:
    import pytesseract
    print('✅ pytesseract (Python package) - INSTALLED')
except ImportError:
    print('❌ pytesseract (Python package) - MISSING')
    print('   Run: pip install pytesseract==0.3.10')
    sys.exit(1)

# Check Pillow
try:
    from PIL import Image
    print('✅ Pillow - INSTALLED')
except ImportError:
    print('❌ Pillow - MISSING')
    print('   Run: pip install Pillow==10.1.0')
    sys.exit(1)

# Check tesseract binary
try:
    import pytesseract
    version = pytesseract.get_tesseract_version()
    print(f'✅ Tesseract binary - INSTALLED (version: {version})')
except Exception as e:
    print(f'❌ Tesseract binary - MISSING')
    print(f'   Error: {str(e)[:100]}')
    print('   macOS: brew install tesseract')
    print('   Linux: sudo apt-get install tesseract-ocr')
    sys.exit(1)

print()
print('=' * 60)
print('✅ ALL DEPENDENCIES INSTALLED SUCCESSFULLY!')
print('=' * 60)
"
```

---

## Step 4: Test CrewAI Tools

After installation, test that OCR tool works:

```bash
cd /Users/dedeepyareddysalla/Documents/Developer/AgenticAI/AAMAD/backend
source venv/bin/activate
python -c "
from crew.tools.ocr_tool import ocr_tool
import tempfile
from PIL import Image
import os

# Create a test image
test_img = Image.new('RGB', (100, 100), color='white')
test_path = os.path.join(tempfile.gettempdir(), 'test_ocr.png')
test_img.save(test_path)

# Test OCR tool
result = ocr_tool(test_path)
print('OCR Tool Test Result:')
print(result[:200] if len(result) > 200 else result)

# Cleanup
os.remove(test_path)
print('✅ OCR tool is working!')
"
```

---

## Troubleshooting

### Issue: "tesseract is not installed or it's not in your PATH"

**Solution:**
1. Install tesseract binary (see Step 1)
2. Verify it's in your PATH:
   ```bash
   which tesseract
   ```
3. If not found, add to PATH or reinstall

### Issue: "ModuleNotFoundError: No module named 'pytesseract'"

**Solution:**
```bash
cd backend
source venv/bin/activate
pip install pytesseract==0.3.10
```

### Issue: "ModuleNotFoundError: No module named 'PIL'"

**Solution:**
```bash
cd backend
source venv/bin/activate
pip install Pillow==10.1.0
```

### Issue: OCR tool still shows placeholder text

**Check:**
1. Is tesseract binary installed? `tesseract --version`
2. Is pytesseract installed? `python -c "import pytesseract; print('OK')"`
3. Check if file path is correct and file exists

---

## Quick Installation Commands (Copy-Paste)

### For macOS:

```bash
# 1. Install tesseract binary
brew install tesseract

# 2. Install Python packages
cd /Users/dedeepyareddysalla/Documents/Developer/AgenticAI/AAMAD/backend
source venv/bin/activate
pip install -r requirements.txt

# 3. Verify
python -c "import pytesseract; from PIL import Image; print('✅ All dependencies OK')"
```

### For Linux:

```bash
# 1. Install tesseract binary
sudo apt-get update
sudo apt-get install tesseract-ocr

# 2. Install Python packages
cd /path/to/backend
source venv/bin/activate
pip install -r requirements.txt

# 3. Verify
python -c "import pytesseract; from PIL import Image; print('✅ All dependencies OK')"
```

---

## What Each Dependency Does

1. **tesseract** (system binary)
   - OCR engine that extracts text from images
   - Required by pytesseract

2. **pytesseract** (Python package)
   - Python wrapper for tesseract
   - Used by OCR tool in CrewAI

3. **Pillow** (Python package)
   - Image processing library
   - Used by OCR tool and Image Processing tool

4. **crewai** (Python package)
   - Main CrewAI framework
   - Required for agents and tasks

5. **crewai-tools** (Python package)
   - Tool decorators for CrewAI
   - Required for @tool decorator

---

## After Installation

Once everything is installed:

1. **Restart your server** (if running):
   ```bash
   # Stop server
   pkill -f "python.*main.py"
   
   # Start server
   cd backend
   source venv/bin/activate
   python main.py
   ```

2. **Test the upload flow**:
   ```bash
   curl -X POST http://localhost:8000/documents/upload \
     -F "file=@/path/to/test/image.png" \
     -F "document_type=I9" \
     -F "user_id=550e8400-e29b-41d4-a716-446655440000"
   ```

3. **Check logs** - OCR tool should now extract actual text instead of placeholder

---

**Need Help?** Check the error messages and refer to the Troubleshooting section above.

