#!/usr/bin/env python3
"""
Batch rename files by removing "- Made with Clipchamp" from filenames.

Usage examples:
  - Rename files in current directory:
      python file_renamer_script.py

  - Specify input directory:
      python file_renamer_script.py --input "path/to/files"

  - Process files with specific pattern:
      python file_renamer_script.py --pattern "*.mp4"

  - Force rename without confirmation:
      python file_renamer_script.py --force
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove '- Made with Clipchamp' text from all filenames in a directory."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path.cwd(),
        help="Directory containing files to rename (default: current directory)",
    )
    parser.add_argument(
        "--pattern",
        type=str,
        default="*",
        help="Glob pattern for input files (default: * for all files)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompt and rename files immediately",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be renamed without actually doing it",
    )
    return parser.parse_args()


def remove_clipchamp_text(filename: str) -> str:
    """Remove the specific Clipchamp text from a filename."""
    target_text = "- Made with Clipchamp"
    return filename.replace(target_text, "")


def rename_file(file_path: Path, dry_run: bool = False) -> bool:
    """Rename a single file by removing Clipchamp text. Returns True on success."""
    original_name = file_path.name
    target_text = "- Made with Clipchamp"
    
    # Skip if target text not in filename
    if target_text not in original_name:
        return True  # Not an error, just nothing to do
    
    new_name = remove_clipchamp_text(original_name)
    
    # Handle edge case where removal results in empty filename
    if not new_name.strip():
        sys.stderr.write(f"Error: '{original_name}' would result in empty filename\n")
        return False
    
    new_path = file_path.parent / new_name
    
    # Check if target filename already exists
    if new_path.exists() and new_path != file_path:
        sys.stderr.write(f"Error: Cannot rename '{original_name}' -> '{new_name}' (target exists)\n")
        return False
    
    if dry_run:
        return True
    
    # Perform the rename
    try:
        file_path.rename(new_path)
        return True
    except OSError as e:
        sys.stderr.write(f"Error: Failed to rename '{original_name}': {e}\n")
        return False


def main() -> None:
    args = parse_args()
    
    input_dir: Path = args.input.resolve()
    
    if not input_dir.exists() or not input_dir.is_dir():
        sys.stderr.write(f"Input directory does not exist or is not a directory: {input_dir}\n")
        sys.exit(1)
    
    # Get all files matching the pattern
    all_files = sorted(input_dir.glob(args.pattern))
    all_files = [p for p in all_files if p.is_file()]
    
    if not all_files:
        print(f"No files matched pattern '{args.pattern}' in {input_dir}")
        return
    
    # Filter files that actually contain the target text
    target_text = "- Made with Clipchamp"
    files_to_rename = [f for f in all_files if target_text in f.name]
    
    if not files_to_rename:
        print(f"No files contain '{target_text}' in their names")
        return
    
    print(f"Found {len(files_to_rename)} file(s) containing '{target_text}':")
    
    # Show preview of what will be renamed
    for file_path in files_to_rename:
        original_name = file_path.name
        new_name = remove_clipchamp_text(original_name)
        action = "WOULD RENAME" if args.dry_run else "WILL RENAME"
        print(f"  {action}: '{original_name}' -> '{new_name}'")
    
    if args.dry_run:
        print(f"\nDry run complete. {len(files_to_rename)} files would be renamed.")
        return
    
    # Confirm with user unless --force is specified
    if not args.force:
        try:
            response = input(f"\nProceed with renaming {len(files_to_rename)} files? (y/N): ").lower().strip()
            if response not in ['y', 'yes']:
                print("Operation cancelled.")
                return
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return
    
    print()
    
    # Perform the renames
    total = len(files_to_rename)
    successes = 0
    
    for idx, file_path in enumerate(files_to_rename, start=1):
        original_name = file_path.name
        new_name = remove_clipchamp_text(original_name)
        print(f"[{idx}/{total}] Renaming: {original_name} -> {new_name}")
        
        ok = rename_file(file_path, dry_run=False)
        if ok:
            successes += 1
    
    print(f"Done. {successes}/{total} files renamed.")


if __name__ == "__main__":
    main()