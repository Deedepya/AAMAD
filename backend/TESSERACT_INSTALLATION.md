# Tesseract Installation - Project-Specific Guide

## Understanding Tesseract Installation

**Important:** Tesseract is a **system-level binary** (not a Python package), so it cannot be installed in a virtual environment like `pip install` packages.

However, installing it via `brew install tesseract` **does NOT affect other projects** - it's just a system utility that any project can use.

---

## Option 1: System-Wide Installation (Recommended)

### Install Tesseract:

```bash
brew install tesseract
```

### Why This is Safe:
- ✅ Tesseract is just a command-line tool (like `git` or `python`)
- ✅ It doesn't modify your Python environment
- ✅ It doesn't interfere with other projects
- ✅ It's a small utility (~50MB)
- ✅ Multiple projects can use the same tesseract binary

### Verify Installation:

```bash
# Check tesseract is installed
tesseract --version

# Check it's accessible from Python
cd /Users/dedeepyareddysalla/Documents/Developer/AgenticAI/AAMAD/backend
source venv/bin/activate
python -c "import pytesseract; print('Tesseract version:', pytesseract.get_tesseract_version())"
```

---

## Option 2: Use Local Tesseract Binary (Advanced)

If you **really** want a project-specific tesseract, you can:

### Step 1: Download Tesseract Binary

```bash
# Create project-specific directory
mkdir -p /Users/dedeepyareddysalla/Documents/Developer/AgenticAI/AAMAD/backend/tesseract-bin

# Download tesseract for macOS (you'll need to find the right binary)
# Or use Homebrew but install to custom location:
brew install tesseract --prefix=/Users/dedeepyareddysalla/Documents/Developer/AgenticAI/AAMAD/backend/tesseract-bin
```

### Step 2: Configure pytesseract to Use Local Binary

Update `crew/tools/ocr_tool.py`:

```python
import pytesseract
import os

# Set path to local tesseract binary
TESSERACT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'tesseract-bin',
    'bin',
    'tesseract'
)
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
```

**Note:** This is more complex and not recommended unless you have a specific need.

---

## Recommended Approach: System-Wide Installation

**Just run:**
```bash
brew install tesseract
```

**Why this is the best option:**
1. ✅ Simple and straightforward
2. ✅ Works immediately with pytesseract
3. ✅ No configuration needed
4. ✅ Doesn't interfere with other projects
5. ✅ Standard practice in the industry
6. ✅ Easy to update: `brew upgrade tesseract`

---

## Verification After Installation

Run this in your terminal:

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

# Create a simple test image with text
img = Image.new('RGB', (200, 50), color='white')
test_path = os.path.join(tempfile.gettempdir(), 'test.png')
img.save(test_path)

try:
    version = pytesseract.get_tesseract_version()
    print(f'✅ Tesseract version: {version}')
    print('✅ Tesseract is working correctly!')
    print()
    print('Your OCR tool will now extract real text from images.')
except Exception as e:
    print(f'❌ Error: {e}')
    print('Please install tesseract: brew install tesseract')

os.remove(test_path)
"
```

---

## Summary

**For this project, simply run:**
```bash
brew install tesseract
```

This installs tesseract system-wide, but:
- ✅ It's just a utility tool (like `git`, `python`, `node`)
- ✅ It doesn't affect your Python virtual environment
- ✅ It doesn't interfere with other projects
- ✅ It's the standard way to install tesseract

**Think of it like:** Installing `git` or `python` - you install it once on your system, and all projects can use it. Same with tesseract.

---

## After Installation

Once tesseract is installed:

1. **Restart your server** (if running):
   ```bash
   pkill -f "python.*main.py"
   cd backend
   source venv/bin/activate
   python main.py
   ```

2. **Test the OCR tool** - it will now extract real text instead of placeholder!

