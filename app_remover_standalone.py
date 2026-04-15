#!/usr/bin/env python3
"""
Standalone App Duplicate Remover - Executable Version

This is a standalone executable script that can be run directly without VS Code.
It contains all the necessary code in a single file.
"""

import os
import re
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app_cleanup.log'),
            logging.StreamHandler()
        ]
    )


def parse_version(version_str: str) -> Tuple[int, ...]:
    """
    Parse version string into tuple of integers for comparison.
    
    Args:
        version_str: Version string like "25.0.11.0"
        
    Returns:
        Tuple of integers representing version components
    """
    try:
        return tuple(map(int, version_str.split('.')))
    except ValueError as e:
        logging.warning(f"Could not parse version '{version_str}': {e}")
        return (0,)


def extract_name_and_version(filename: str) -> Optional[Tuple[str, str]]:
    """
    Extract name part and version from .app filename.
    
    Args:
        filename: The .app filename
        
    Returns:
        Tuple of (name_part, version) or None if pattern doesn't match
    """
    if not filename.endswith('.app'):
        return None
    
    base_name = filename[:-4]
    pattern = r'^(.+)_(\d+(?:\.\d+)*)$'
    match = re.match(pattern, base_name)
    
    if match:
        name_part = match.group(1)
        version = match.group(2)
        return name_part, version
    
    logging.warning(f"Could not parse filename: {filename}")
    return None


def find_app_files(directory: str) -> List[str]:
    """Find all .app files in the given directory."""
    directory_path = Path(directory)
    app_files = [f.name for f in directory_path.glob('*.app')]
    logging.info(f"Found {len(app_files)} .app files in {directory}")
    return app_files


def group_files_by_name(app_files: List[str]) -> Dict[str, List[Tuple[str, str]]]:
    """Group .app files by their name parts."""
    grouped_files = defaultdict(list)
    
    for filename in app_files:
        parsed = extract_name_and_version(filename)
        if parsed:
            name_part, version = parsed
            grouped_files[name_part].append((filename, version))
    
    return dict(grouped_files)


def identify_files_to_delete(grouped_files: Dict[str, List[Tuple[str, str]]]) -> List[str]:
    """Identify which files should be deleted (keeping only the highest version)."""
    files_to_delete = []
    
    for name_part, file_versions in grouped_files.items():
        if len(file_versions) <= 1:
            continue
        
        logging.info(f"\nProcessing duplicates for: {name_part}")
        
        sorted_files = sorted(
            file_versions,
            key=lambda x: parse_version(x[1]),
            reverse=True
        )
        
        keep_file = sorted_files[0]
        delete_files = sorted_files[1:]
        
        logging.info(f"  Keeping: {keep_file[0]} (version {keep_file[1]})")
        
        for filename, version in delete_files:
            logging.info(f"  Marking for deletion: {filename} (version {version})")
            files_to_delete.append(filename)
    
    return files_to_delete


def delete_files(files_to_delete: List[str], directory: str, dry_run: bool = False) -> None:
    """Delete the specified files."""
    directory_path = Path(directory)
    
    if not files_to_delete:
        logging.info("No duplicate files found to delete.")
        return
    
    logging.info(f"\n{'DRY RUN: Would delete' if dry_run else 'Deleting'} {len(files_to_delete)} files:")
    
    for filename in files_to_delete:
        file_path = directory_path / filename
        
        if file_path.exists():
            if dry_run:
                logging.info(f"  Would delete: {filename}")
            else:
                try:
                    file_path.unlink()
                    logging.info(f"  Deleted: {filename}")
                except OSError as e:
                    logging.error(f"  Failed to delete {filename}: {e}")
        else:
            logging.warning(f"  File not found: {filename}")


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(
        description="Remove duplicate .app files, keeping highest versions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Execute deletion in current directory
  %(prog)s --dry-run          # Preview what would be deleted
  %(prog)s -d /path/to/apps   # Execute in specific directory
  %(prog)s -d /path --dry-run # Preview in specific directory
        """
    )
    
    parser.add_argument(
        "--directory", "-d",
        default=".",
        help="Directory to process (default: current directory)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only show what would be deleted without actually deleting"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="App Duplicate Remover 1.0"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Welcome message
    print("=" * 60)
    print("🗂️  APP DUPLICATE REMOVER v1.0")
    print("=" * 60)
    
    logger.info(f"Starting app file duplicate removal in: {os.path.abspath(args.directory)}")
    logger.info(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE DELETION'}")
    
    # Find all .app files
    app_files = find_app_files(args.directory)
    
    if not app_files:
        logger.info("No .app files found.")
        print("\n✅ No .app files found to process.")
        return
    
    # Group files by name part
    grouped_files = group_files_by_name(app_files)
    
    # Show summary
    logger.info(f"\nFound {len(grouped_files)} unique app names:")
    duplicate_count = 0
    for name_part, file_versions in grouped_files.items():
        if len(file_versions) > 1:
            logger.info(f"  {name_part}: {len(file_versions)} versions")
            duplicate_count += 1
        else:
            logger.info(f"  {name_part}: 1 version (no duplicates)")
    
    if duplicate_count == 0:
        print("\n✅ No duplicate files found!")
        return
    
    # Identify files to delete
    files_to_delete = identify_files_to_delete(grouped_files)
    
    # Delete files (or dry run)
    delete_files(files_to_delete, args.directory, args.dry_run)
    
    # Final message
    if args.dry_run:
        print(f"\n🔍 DRY RUN COMPLETE")
        print(f"📋 Would delete {len(files_to_delete)} duplicate files")
        print(f"🚀 To actually delete files, run without --dry-run flag")
    else:
        print(f"\n✅ DELETION COMPLETE")
        print(f"🗑️  Removed {len(files_to_delete)} duplicate files")
        print(f"📝 Check app_cleanup.log for detailed information")


if __name__ == "__main__":
    main()
