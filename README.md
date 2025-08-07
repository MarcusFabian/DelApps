# Python Project

A modern Python project with a clean structure and development tools, including an App Duplicate Remover utility.

## Project Structure

```
.
├── 🚀 EXECUTABLE SCRIPTS (No VS Code needed)
│   ├── app_remover_standalone.py      # Standalone Python executable
│   ├── run_app_remover.sh            # Shell wrapper (macOS/Linux)
│   ├── run_app_remover.bat           # Batch script (Windows)
│   ├── build_executable.sh           # Build binary executable
│   └── setup.sh                      # One-command setup
├── src/                              # Development source code
│   ├── main.py                       # Main application entry point
│   ├── app_duplicate_remover.py      # Core duplicate removal module
│   └── example_usage.py              # Usage examples
├── tests/                            # Unit tests
│   ├── test_main.py                  # Unit tests for main
│   └── test_app_duplicate_remover.py # Unit tests for duplicate remover
├── .github/
│   └── copilot-instructions.md       # AI coding instructions
├── .vscode/
│   └── tasks.json                    # VS Code tasks
├── requirements.txt                  # Production dependencies
├── requirements-dev.txt              # Development dependencies
├── .gitignore                       # Git ignore file
└── README.md                        # This file
```

## App Duplicate Remover

This project includes a specialized utility for managing .app file duplicates with **multiple ways to run without VS Code**:

### 🚀 **Executable Options (No VS Code Required)**

#### 1. Standalone Python Script (Recommended)
```bash
# Direct execution (no VS Code needed)
./app_remover_standalone.py --dry-run    # Preview
./app_remover_standalone.py              # Execute deletion

# Or with python3
python3 app_remover_standalone.py --help
```

#### 2. Shell Script Wrapper (macOS/Linux)
```bash
# Automated environment setup and execution
./run_app_remover.sh --dry-run           # Preview
./run_app_remover.sh                     # Execute deletion
./run_app_remover.sh -d /path/to/apps    # Different directory
```

#### 3. Binary Executable (Advanced)
```bash
# Create standalone binary (requires PyInstaller)
./build_executable.sh

# Then run the binary anywhere
./dist/AppDuplicateRemover --dry-run
./dist/AppDuplicateRemover -d /path/to/apps
```

### Features
- **Execute by Default**: Program deletes duplicate files by default (no dry-run mode)
- **Optional Dry Run**: Use `--dry-run` flag to preview what would be deleted
- **Version Comparison**: Intelligently compares version numbers (e.g., 25.0.11.0 vs 24.9.9.0)
- **Detailed Logging**: Comprehensive logging to both console and log file
- **Flexible**: Command-line interface and programmatic API

### File Format Expected
Files should follow the pattern: `[name_part]_[version].app`

Examples:
- `EOS Solutions_Common Data Layer_25.0.11.0.app`
- `Marcus Fabian_EPCIS Migros_24.9.9.0.app`
- `Microsoft_Base Application_25.0.23364.25858.app`

### Usage

#### Standalone Executables (No VS Code Required) ⭐
```bash
# Standalone Python script (recommended)
./app_remover_standalone.py --dry-run    # Preview
./app_remover_standalone.py              # Execute deletion

# Shell wrapper (auto-setup)
./run_app_remover.sh --dry-run           # Preview with auto environment
./run_app_remover.sh                     # Execute with auto environment

# Binary executable (after building)
./dist/AppDuplicateRemover --dry-run     # Completely standalone binary
```

#### VS Code Development Mode
```bash
# Command Line (from VS Code terminal)
python src/app_duplicate_remover.py --directory . --dry-run
python src/app_duplicate_remover.py --directory .

# VS Code Tasks
# Use Command Palette (Cmd+Shift+P) → "Tasks: Run Task":
# - "Remove App Duplicates (Execute)" - Deletes duplicates
# - "Remove App Duplicates (Dry Run)" - Safe preview

# Programmatic Usage
from src.app_duplicate_remover import main
main(directory="/path/to/app/files", dry_run=False)  # Execute
main(directory="/path/to/app/files", dry_run=True)   # Preview
```

## Quick Start (No VS Code Required)

### 🚀 **One-Command Setup**
```bash
# Automatic setup for all platforms
./setup.sh
```

### 🎯 **Instant Usage** (After setup)

#### macOS/Linux
```bash
# Preview what would be deleted (safe)
./app_remover_standalone.py --dry-run

# Execute deletion when ready
./app_remover_standalone.py

# Auto-environment version
./run_app_remover.sh --dry-run
```

#### Windows
```cmd
# Double-click or run from command prompt
run_app_remover.bat --dry-run
run_app_remover.bat
```

### 🛠️ **Advanced: Binary Executable**
```bash
# Create standalone binary (no Python dependency)
./build_executable.sh

# Use binary anywhere
./dist/AppDuplicateRemover --dry-run
```

## Development Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   ```bash
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

## Running the Project

### Main Application
```bash
python src/main.py
```

### App Duplicate Remover
```bash
# Execute deletion (default behavior)
python src/app_duplicate_remover.py

# Preview what would be deleted (dry run)
python src/app_duplicate_remover.py --dry-run
```

## Running Tests

```bash
pytest tests/
```

## Development

- Use `black` for code formatting
- Use `flake8` for linting
- Use `pytest` for testing
- Type hints are encouraged using `mypy`

## VS Code Integration

This project includes VS Code tasks for common operations:
- **Run the application**: "Run Main App"
- **Run tests**: "Run Tests"
- **Remove app duplicates (dry run)**: "Remove App Duplicates (Dry Run)"
- **Remove app duplicates (execute)**: "Remove App Duplicates (Execute)"

Access tasks via Command Palette (Cmd+Shift+P) → "Tasks: Run Task"

## Safety Features

The App Duplicate Remover includes several safety features:
- **Optional Dry Run**: Use `--dry-run` flag to preview what would be deleted
- **Comprehensive logging**: All operations logged to `app_cleanup.log`
- **Version validation**: Robust version parsing and comparison
- **Error handling**: Graceful handling of file system errors
- **Detailed reporting**: Shows exactly which files will be kept/deleted

## Example Output

```
2025-08-07 15:37:25,860 - INFO - Found 30 .app files in .
2025-08-07 15:37:25,861 - INFO - Found 28 unique app names:
2025-08-07 15:37:25,861 - INFO -   Microsoft_Base Application: 2 versions
2025-08-07 15:37:25,861 - INFO -   Marcus Fabian_EPCIS Migros: 2 versions

Processing duplicates for: Microsoft_Base Application
  Keeping: Microsoft_Base Application_25.0.23364.25858.app (version 25.0.23364.25858)
  Marking for deletion: Microsoft_Base Application_25.0.23364.25649.app (version 25.0.23364.25649)

DRY RUN: Would delete 2 files:
  Would delete: Microsoft_Base Application_25.0.23364.25649.app
  Would delete: Marcus Fabian_EPCIS Migros_24.9.9.0.app
```
