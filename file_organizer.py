#!/usr/bin/env python3
"""
Automatic File Organizer
------------------------
Tiny CLI utility to sort files into subfolders by extension.

Usage:
    python file_organizer.py [directory]

If no directory is provided, the current working directory is organized.
Only files in the top-level of the target directory are moved; subfolders are ignored.
"""

from __future__ import annotations

import argparse
import os
import shutil
from typing import Dict, List, Iterable


def organize_files(
    directory: str,
    *,
    recursive: bool = False,
    dry_run: bool = False,
    move_noext: bool = False,
) -> int:
    """Organize files in the given directory into subfolders by extension.

    Parameters:
        directory: Target directory to organize.
        recursive: If True, also organize files in subdirectories.
        dry_run: If True, print intended actions but do not move files.
        move_noext: If True, files without extensions go to Misc; otherwise left in place.

    Returns:
        Number of files moved (or that would be moved in dry-run).
    """
    # Define categories and their extensions (lowercase)
    categories: Dict[str, List[str]] = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg"],
        "Documents": [
            ".pdf",
            ".doc",
            ".docx",
            ".txt",
            ".rtf",
            ".odt",
            ".xls",
            ".xlsx",
            ".csv",
            ".ppt",
            ".pptx",
            ".md",
        ],
        "Archives": [".zip", ".rar", ".tar", ".gz", ".bz2", ".xz", ".7z"],
        "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".webm"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
        "Code": [
            ".py",
            ".js",
            ".ts",
            ".jsx",
            ".tsx",
            ".html",
            ".css",
            ".json",
            ".yml",
            ".yaml",
            ".xml",
            ".sh",
        ],
        "Misc": [],  # Catch-all for uncategorized files
    }

    directory = os.path.abspath(os.path.expanduser(directory))
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"Not a directory: {directory}")

    # Ensure category folders exist at the root
    for category in categories:
        os.makedirs(os.path.join(directory, category), exist_ok=True)

    def iter_files(root: str) -> Iterable[str]:
        if not recursive:
            for entry in os.listdir(root):
                p = os.path.join(root, entry)
                if os.path.isfile(p):
                    yield p
            return
        # recursive walk
        for dirpath, dirnames, filenames in os.walk(root):
            # Skip category folders under root to avoid reprocessing destinations
            if os.path.abspath(dirpath) == os.path.abspath(root):
                dirnames[:] = [d for d in dirnames if d not in categories]
            for fname in filenames:
                yield os.path.join(dirpath, fname)

    moved_count = 0
    root_abs = os.path.abspath(directory)
    for src_path in iter_files(root_abs):
        entry = os.path.basename(src_path)

        # Determine category by extension
        _, ext = os.path.splitext(entry)
        ext = ext.lower()

        dest_category = None
        for category, exts in categories.items():
            if ext and ext in exts:
                dest_category = category
                break

        if dest_category is None:
            if ext:
                dest_category = "Misc"
            elif move_noext:
                dest_category = "Misc"
            else:
                continue

        dest_dir = os.path.join(root_abs, dest_category)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, entry)

        # If a file with the same name exists in the destination, generate a unique name
        if os.path.exists(dest_path):
            name, extension = os.path.splitext(entry)
            suffix = 1
            while True:
                candidate = f"{name} ({suffix}){extension}"
                candidate_path = os.path.join(dest_dir, candidate)
                if not os.path.exists(candidate_path):
                    dest_path = candidate_path
                    break
                suffix += 1

        # Avoid moving if source is already the destination
        if os.path.abspath(src_path) == os.path.abspath(dest_path):
            continue

        if dry_run:
            print(f"DRY-RUN: would move '{src_path}' -> '{dest_path}'")
        else:
            shutil.move(src_path, dest_path)
        moved_count += 1

    return moved_count


def main() -> None:
    parser = argparse.ArgumentParser(description="Organize files in a directory by type.")
    parser.add_argument(
        "directory",
        nargs="?",
        default=os.getcwd(),
        help="Path to the directory to organize (default: current directory)",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Also organize files in subdirectories.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without moving any files.",
    )
    parser.add_argument(
        "--move-noext",
        action="store_true",
        help="Move files without extensions to Misc instead of leaving them.",
    )
    args = parser.parse_args()

    moved = organize_files(
        args.directory,
        recursive=args.recursive,
        dry_run=args.dry_run,
        move_noext=args.move_noext,
    )
    prefix = "(dry-run) " if args.dry_run else ""
    print(f"{prefix}Organized {moved} files in {os.path.abspath(os.path.expanduser(args.directory))}.")


if __name__ == "__main__":
    main()
