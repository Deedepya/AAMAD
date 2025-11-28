# Fix: ModuleNotFoundError: No module named 'crewai'

## Error
```
ModuleNotFoundError: No module named 'crewai'
```

## Root Cause
The `crewai` package is not installed, OR there's a Python version incompatibility.

## Solution 1: Install CrewAI (Quick Fix)

```bash
cd backend
python3 -m pip install crewai langchain langchain-openai
```

## Solution 2: Install All Dependencies

```bash
cd backend
python3 -m pip install -r requirements.txt
```

## Solution 3: Python Version Issue

**Problem:** CrewAI 0.28.8 requires Python 3.10+, but you have Python 3.9.6

**Check your Python version:**
```bash
python3 --version
```

**If you have Python 3.9, you have two options:**

### Option A: Upgrade Python (Recommended)
```bash
# Install Python 3.10+ using Homebrew (macOS)
brew install python@3.11

# Then use it
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Option B: Use Compatible CrewAI Version
```bash
# Install older version compatible with Python 3.9
pip install "crewai<0.20" langchain langchain-openai
```

**Note:** This may have limited features.

## Solution 4: Use Virtual Environment (Best Practice)

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Current Status

The code has been updated to handle missing CrewAI gracefully:
- Server will start even if CrewAI is not installed
- Document uploads will work (files will be saved)
- AI processing will be skipped if CrewAI is unavailable
- You'll see warnings in logs but server will run

## Verify Installation

After installing, verify:
```bash
python3 -c "import crewai; print('CrewAI version:', crewai.__version__)"
```

## Expected Behavior After Fix

1. **With CrewAI installed:**
   - Server starts normally
   - Documents are processed with AI agents
   - Full functionality available

2. **Without CrewAI:**
   - Server starts with warnings
   - Documents are uploaded and saved
   - AI processing is skipped
   - Basic functionality works

## Quick Test

After installing, try starting the server again:
```bash
cd backend
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Database initialized
INFO:     CrewAI crew initialized  ← This confirms CrewAI is working
INFO:     Application startup complete.
```

