#!/usr/bin/env python3
"""
App File Duplicate Remover

This script identifies and removes duplicate .app files based on their name parts,
keeping only the files with the highest version numbers.

File format expected: [name_part]_[version].app
Example: EOS Solutions_Common Data Layer_25.0.11.0.app
"""

import os
import re
import logging
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
        
    Example:
        parse_version("25.0.11.0") -> (25, 0, 11, 0)
    """
    try:
        return tuple(map(int, version_str.split('.')))
    except ValueError as e:
        logging.warning(f"Could not parse version '{version_str}': {e}")
        return (0,)  # Default to lowest version


def extract_name_and_version(filename: str) -> Optional[Tuple[str, str]]:
    """
    Extract name part and version from .app filename.
    
    Args:
        filename: The .app filename
        
    Returns:
        Tuple of (name_part, version) or None if pattern doesn't match
        
    Example:
        extract_name_and_version("EOS Solutions_Common Data Layer_25.0.11.0.app")
        -> ("EOS Solutions_Common Data Layer", "25.0.11.0")
    """
    if not filename.endswith('.app'):
        return None
    
    # Remove .app extension
    base_name = filename[:-4]
    
    # Pattern to match: name_version where version is like X.Y.Z.W
    # The version part should be at the end after the last underscore
    pattern = r'^(.+)_(\d+(?:\.\d+)*)$'
    match = re.match(pattern, base_name)
    
    if match:
        name_part = match.group(1)
        version = match.group(2)
        return name_part, version
    
    logging.warning(f"Could not parse filename: {filename}")
    return None


def find_app_files(directory: str) -> List[str]:
    """
    Find all .app files in the given directory.
    
    Args:
        directory: Path to search for .app files
        
    Returns:
        List of .app filenames
    """
    directory_path = Path(directory)
    app_files = [f.name for f in directory_path.glob('*.app')]
    logging.info(f"Found {len(app_files)} .app files in {directory}")
    return app_files


def group_files_by_name(app_files: List[str]) -> Dict[str, List[Tuple[str, str]]]:
    """
    Group .app files by their name parts.
    
    Args:
        app_files: List of .app filenames
        
    Returns:
        Dictionary mapping name_part to list of (filename, version) tuples
    """
    grouped_files = defaultdict(list)
    
    for filename in app_files:
        parsed = extract_name_and_version(filename)
        if parsed:
            name_part, version = parsed
            grouped_files[name_part].append((filename, version))
    
    return dict(grouped_files)


def identify_files_to_delete(grouped_files: Dict[str, List[Tuple[str, str]]]) -> List[str]:
    """
    Identify which files should be deleted (keeping only the highest version).
    
    Args:
        grouped_files: Dictionary mapping name_part to list of (filename, version) tuples
        
    Returns:
        List of filenames to delete
    """
    files_to_delete = []
    
    for name_part, file_versions in grouped_files.items():
        if len(file_versions) <= 1:
            # No duplicates, skip
            continue
        
        logging.info(f"\nProcessing duplicates for: {name_part}")
        
        # Sort by version (highest first)
        sorted_files = sorted(
            file_versions,
            key=lambda x: parse_version(x[1]),
            reverse=True
        )
        
        # Keep the first (highest version), mark rest for deletion
        keep_file = sorted_files[0]
        delete_files = sorted_files[1:]
        
        logging.info(f"  Keeping: {keep_file[0]} (version {keep_file[1]})")
        
        for filename, version in delete_files:
            logging.info(f"  Marking for deletion: {filename} (version {version})")
            files_to_delete.append(filename)
    
    return files_to_delete


def delete_files(files_to_delete: List[str], directory: str, dry_run: bool = False) -> None:
    """
    Delete the specified files.
    
    Args:
        files_to_delete: List of filenames to delete
        directory: Directory containing the files
        dry_run: If True, only log what would be deleted without actually deleting
    """
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


def main(directory: str = ".", dry_run: bool = False) -> None:
    """
    Main function to remove duplicate .app files.
    
    Args:
        directory: Directory to process (default: current directory)
        dry_run: If True, only show what would be deleted without actually deleting
    """
    setup_logging()
    
    logger = logging.getLogger(__name__)
    logger.info(f"Starting app file duplicate removal in: {os.path.abspath(directory)}")
    logger.info(f"Mode: {'DRY RUN' if dry_run else 'LIVE DELETION'}")
    
    # Find all .app files
    app_files = find_app_files(directory)
    
    if not app_files:
        logger.info("No .app files found.")
        return
    
    # Group files by name part
    grouped_files = group_files_by_name(app_files)
    
    # Show summary of found files
    logger.info(f"\nFound {len(grouped_files)} unique app names:")
    for name_part, file_versions in grouped_files.items():
        if len(file_versions) > 1:
            logger.info(f"  {name_part}: {len(file_versions)} versions")
        else:
            logger.info(f"  {name_part}: 1 version (no duplicates)")
    
    # Identify files to delete
    files_to_delete = identify_files_to_delete(grouped_files)
    
    # Delete files (or dry run)
    delete_files(files_to_delete, directory, dry_run)
    
    if dry_run:
        logger.info(f"\nDRY RUN COMPLETE. To actually delete files, run with dry_run=False")
    else:
        logger.info(f"\nDeletion complete. {len(files_to_delete)} files removed.")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Remove duplicate .app files, keeping highest versions")
    parser.add_argument(
        "--directory", "-d", 
        default=".", 
        help="Directory to process (default: current directory)"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Only show what would be deleted without actually deleting (default: execute deletion)"
    )
    
    args = parser.parse_args()
    
    main(directory=args.directory, dry_run=args.dry_run)
