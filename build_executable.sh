#!/bin/bash

# Build Executable Script
# This script creates a standalone executable using PyInstaller

set -e

echo "🏗️  Building standalone executable..."

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Activated virtual environment"
else
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Install PyInstaller if not already installed
if ! python -c "import PyInstaller" 2>/dev/null; then
    echo "📦 Installing PyInstaller..."
    pip install pyinstaller
fi

# Create the executable
echo "🔨 Creating executable..."
pyinstaller \
    --onefile \
    --name "AppDuplicateRemover" \
    --add-data "app_cleanup.log:." \
    --console \
    --clean \
    app_remover_standalone.py

echo ""
echo "✅ Executable created successfully!"
echo "📁 Location: dist/AppDuplicateRemover"
echo ""
echo "Usage examples:"
echo "  ./dist/AppDuplicateRemover --help"
echo "  ./dist/AppDuplicateRemover --dry-run"
echo "  ./dist/AppDuplicateRemover -d /path/to/apps"

deactivate
