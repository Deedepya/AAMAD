#!/bin/bash
# Quick script to install Tesseract OCR

echo "============================================================"
echo "Installing Tesseract OCR for CrewAI"
echo "============================================================"
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is not installed."
    echo "   Install Homebrew first: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

echo "✅ Homebrew is installed"
echo ""

# Check if tesseract is already installed
if command -v tesseract &> /dev/null; then
    echo "✅ Tesseract is already installed"
    tesseract --version
    exit 0
fi

echo "Installing Tesseract..."
echo ""

# Install tesseract
brew install tesseract

# Verify installation
if command -v tesseract &> /dev/null; then
    echo ""
    echo "============================================================"
    echo "✅ Tesseract installed successfully!"
    echo "============================================================"
    tesseract --version
    echo ""
    echo "Now verify from Python:"
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  python -c \"import pytesseract; print('Version:', pytesseract.get_tesseract_version())\""
else
    echo ""
    echo "❌ Installation failed. Please check the error messages above."
    exit 1
fi

