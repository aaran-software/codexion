# =============================================================
# Migration File Registry (file.py)
#
# Author: ChatGPT
# Created: 2025-08-06
#
# Purpose:
#   - Manage dynamic or manual registration of migration files.
#   - Can define execution order explicitly if needed.
# =============================================================

import os
import re
from typing import List, Tuple


def _extract_index_from_filename(filename: str) -> int:
    match = re.match(r"(\d+)_", filename)
    return int(match.group(1)) if match else 9999


def _scan_group_folders(base_dir: str) -> List[Tuple[int, int, str]]:
    """
    Return list of (group_index, table_index, full_path) from nested folders.
    """
    ordered = []
    group_folders = sorted([
        f for f in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, f))
    ])

    for group_idx, group in enumerate(group_folders, start=1):
        group_path = os.path.join(base_dir, group)
        files = sorted([
            f for f in os.listdir(group_path)
            if f.endswith(".py") and not f.startswith("__")
        ])

        seen = set()
        for file in files:
            table_index = _extract_index_from_filename(file)
            if table_index in seen:
                raise ValueError(f"🚨 Duplicate table index '{table_index}' in group '{group}'")
            seen.add(table_index)

            full_path = os.path.join(group_path, file)
            ordered.append((group_idx, table_index, full_path))

    return ordered


def list_migration_files(base_dir: str) -> List[str]:
    """
    Auto-generated ordered list of all migration files based on:
    - Folder = group
    - Filename prefix = order (e.g. 01_create_...)
    """
    indexed_files = _scan_group_folders(base_dir)
    sorted_files = sorted(indexed_files, key=lambda x: (x[0], x[1]))
    return [file for _, _, file in sorted_files]
