# tools/clean_pycache.py
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil

SKIP_DIRS = {".git", ".hg", ".svn", ".venv", "venv", "node_modules", ".mypy_cache", ".pytest_cache"}

def should_skip(path: Path) -> bool:
    parts = set(part.lower() for part in path.parts)
    return any(skip in parts for skip in SKIP_DIRS)

def clean(root: Path, dry_run: bool = False) -> tuple[int, int]:
    removed_dirs = 0
    removed_files = 0

    for p in root.rglob("*"):
        if p.is_dir():
            if p.name == "__pycache__" and not should_skip(p):
                if dry_run:
                    print(f"[dry] remove dir: {p}")
                else:
                    shutil.rmtree(p, ignore_errors=True)
                removed_dirs += 1
        elif p.is_file():
            if p.suffix in {".pyc", ".pyo"} and not should_skip(p):
                if dry_run:
                    print(f"[dry] remove file: {p}")
                else:
                    try:
                        p.unlink()
                    except OSError:
                        pass
                removed_files += 1
    return removed_dirs, removed_files

def main():
    parser = argparse.ArgumentParser(description="Clean all Python cache files/dirs.")
    parser.add_argument("--root", default=".", help="Root directory (default: current)")
    parser.add_argument("--dry-run", action="store_true", help="Preview deletions without removing")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Root not found: {root}")
        raise SystemExit(2)

    d, f = clean(root, dry_run=args.dry_run)
    if args.dry_run:
        print(f"[dry] Would remove: {d} __pycache__/ dirs, {f} .pyc/.pyo files")
    else:
        print(f"Removed: {d} __pycache__/ dirs, {f} .pyc/.pyo files")

if __name__ == "__main__":
    main()
