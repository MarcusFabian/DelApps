#!/usr/bin/env python3
"""
Example usage of the app_duplicate_remover module.

This script demonstrates how to use the app duplicate remover programmatically.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from _app_duplicate_remover import main


def example_usage():
    """Example of how to use the app duplicate remover."""
    
    print("=== App Duplicate Remover Example ===\n")
    
    # Current directory path
    current_dir = os.getcwd()
    print(f"Working directory: {current_dir}\n")
    
    # Run in dry run mode first (safe)
    print("1. Running in DRY RUN mode (safe - no files will be deleted):")
    print("-" * 60)
    main(directory=current_dir, dry_run=True)
    
    print("\n" + "=" * 60)
    print("2. To actually delete duplicate files, you would run:")
    print("   main(directory=current_dir, dry_run=False)  # Default behavior")
    print("   Or use: python src/app_duplicate_remover.py")
    print("   For dry run: python src/app_duplicate_remover.py --dry-run")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()
