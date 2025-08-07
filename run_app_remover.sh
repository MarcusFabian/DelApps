#!/bin/bash

# App Duplicate Remover - Shell Script Launcher
# This script allows you to run the app duplicate remover from anywhere

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}🗂️  App Duplicate Remover${NC}"
echo -e "${BLUE}================================${NC}"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python 3 is not installed or not in PATH${NC}"
    exit 1
fi

# Check if virtual environment exists
VENV_PATH="$SCRIPT_DIR/venv"
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating one...${NC}"
    python3 -m venv "$VENV_PATH"
    
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    source "$VENV_PATH/bin/activate"
    pip install --upgrade pip
    pip install -r "$SCRIPT_DIR/requirements-dev.txt" 2>/dev/null || echo "Requirements file not found, continuing..."
    deactivate
fi

# Activate virtual environment
echo -e "${GREEN}🐍 Activating Python environment...${NC}"
source "$VENV_PATH/bin/activate"

# Run the standalone app remover
echo -e "${GREEN}🚀 Starting App Duplicate Remover...${NC}"
echo ""

python3 "$SCRIPT_DIR/_app_remover_standalone.py" "$@"

# Deactivate virtual environment
deactivate

echo ""
echo -e "${GREEN}✅ App Duplicate Remover finished${NC}"
