# Fix: Tesseract Not Found Error

## Problem

You're seeing this error:
```
pytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your PATH
```

## Solution

### Quick Fix (Run in Terminal):

```bash
# Install Tesseract using Homebrew
brew install tesseract

# Verify installation
tesseract --version
```

### After Installation, Verify from Python:

```bash
cd /Users/dedeepyareddysalla/Documents/Developer/AgenticAI/AAMAD/backend
source venv/bin/activate
python -c "import pytesseract; print('Tesseract version:', pytesseract.get_tesseract_version())"
```

**Expected output:** Should show tesseract version (e.g., `Tesseract version: 5.3.3`)

---

## Alternative: Use Installation Script

I've created a script to help with installation:

```bash
cd /Users/dedeepyareddysalla/Documents/Developer/AgenticAI/AAMAD/backend
./INSTALL_TESSERACT.sh
```

---

## Troubleshooting

### If `brew install tesseract` fails:

1. **Update Homebrew:**
   ```bash
   brew update
   ```

2. **Check Homebrew is working:**
   ```bash
   brew doctor
   ```

3. **Try installing again:**
   ```bash
   brew install tesseract
   ```

### If tesseract is installed but Python can't find it:

1. **Check tesseract location:**
   ```bash
   which tesseract
   ```

2. **Check if it's in PATH:**
   ```bash
   echo $PATH | grep -i tesseract
   ```

3. **Manually set path in Python (temporary fix):**
   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'  # or wherever brew installed it
   ```

### If you don't have Homebrew:

Install Homebrew first:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then install tesseract:
```bash
brew install tesseract
```

---

## Verify Everything Works

After installation, run this complete test:

```bash
cd /Users/dedeepyareddysalla/Documents/Developer/AgenticAI/AAMAD/backend
source venv/bin/activate

python -c "
import pytesseract
from PIL import Image
import tempfile
import os

print('Testing Tesseract installation...')
print()

# Check version
try:
    version = pytesseract.get_tesseract_version()
    print(f'✅ Tesseract version: {version}')
except Exception as e:
    print(f'❌ Error: {e}')
    exit(1)

# Test OCR on a simple image
try:
    img = Image.new('RGB', (200, 50), color='white')
    test_path = os.path.join(tempfile.gettempdir(), 'test_ocr.png')
    img.save(test_path)
    
    # This should work without errors
    text = pytesseract.image_to_string(img)
    print('✅ OCR extraction test passed')
    print('✅ Tesseract is fully functional!')
    
    os.remove(test_path)
except Exception as e:
    print(f'❌ OCR test failed: {e}')
    exit(1)
"
```

---

## Next Steps

Once tesseract is installed:

1. **Restart your server** (if running):
   ```bash
   pkill -f "python.*main.py"
   cd backend
   source venv/bin/activate
   python main.py
   ```

2. **Test document upload** - OCR tool will now extract real text!

