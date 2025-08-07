#!/bin/bash

# App Duplicate Remover - Quick Setup Script
# This script sets up the executable scripts for immediate use

echo "🚀 App Duplicate Remover - Quick Setup"
echo "======================================"

# Make scripts executable
echo "📋 Setting executable permissions..."
chmod +x app_remover_standalone.py
chmod +x run_app_remover.sh
chmod +x build_executable.sh

echo "✅ Scripts are now executable!"
echo ""
echo "🎯 Ready to use! Choose your method:"
echo ""
echo "   🥇 STANDALONE (Recommended):"
echo "      ./app_remover_standalone.py --dry-run    # Preview"
echo "      ./app_remover_standalone.py              # Execute"
echo ""
echo "   🛠️  AUTO-SETUP:"
echo "      ./run_app_remover.sh --dry-run           # Auto environment + preview"
echo "      ./run_app_remover.sh                     # Auto environment + execute"
echo ""
echo "   🔧 BINARY EXECUTABLE:"
echo "      ./build_executable.sh                    # Create binary"
echo "      ./dist/AppDuplicateRemover --dry-run     # Use binary"
echo ""
echo "💡 Pro tip: Always run --dry-run first to preview changes!"
echo ""
echo "📋 Your current directory has:"
ls -1 *.app 2>/dev/null | wc -l | xargs echo "   " "app files"
echo ""
echo "🎉 Setup complete! You can now run the app remover without VS Code."
