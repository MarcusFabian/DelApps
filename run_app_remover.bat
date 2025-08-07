@echo off
REM App Duplicate Remover - Windows Batch Script

echo.
echo 🗂️  App Duplicate Remover (Windows)
echo ================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3 and add it to your PATH
    pause
    exit /b 1
)

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0

echo 🐍 Using Python to run App Duplicate Remover...
echo.

REM Run the standalone Python script with all arguments
python "%SCRIPT_DIR%app_remover_standalone.py" %*

echo.
echo ✅ App Duplicate Remover finished
pause
