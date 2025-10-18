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
from typing import Dict, List


def organize_files(directory: str) -> int:
    """Organize files in the given directory into subfolders by extension.

    Returns the number of files moved.
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

    # Ensure category folders exist
    for category in categories:
        os.makedirs(os.path.join(directory, category), exist_ok=True)

    moved_count = 0
    for entry in os.listdir(directory):
        src_path = os.path.join(directory, entry)

        # Skip directories (including our category folders)
        if os.path.isdir(src_path):
            continue

        # Determine category by extension
        _, ext = os.path.splitext(entry)
        ext = ext.lower()

        dest_category = None
        for category, exts in categories.items():
            if ext and ext in exts:
                dest_category = category
                break

        if dest_category is None:
            # If file has an extension but no matching category, place in Misc.
            # Files without any extension are left in place by default to avoid
            # surprising moves of executables or dotfiles; change logic if desired.
            if ext:
                dest_category = "Misc"
            else:
                continue

        dest_path = os.path.join(directory, dest_category, entry)

        # If a file with the same name exists in the destination, generate a unique name
        if os.path.exists(dest_path):
            name, extension = os.path.splitext(entry)
            suffix = 1
            while True:
                candidate = f"{name} ({suffix}){extension}"
                candidate_path = os.path.join(directory, dest_category, candidate)
                if not os.path.exists(candidate_path):
                    dest_path = candidate_path
                    break
                suffix += 1

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
    args = parser.parse_args()

    moved = organize_files(args.directory)
    print(f"Organized {moved} files in {os.path.abspath(os.path.expanduser(args.directory))}.")


if __name__ == "__main__":
    main()
