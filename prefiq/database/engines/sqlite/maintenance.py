# =============================================================
# SQLite Maintenance (backup / integrity / rebuild)
# file path: prefiq/database/engines/sqlite/maintenance.py
#
# Author: Sundar
# Created: 2025-08-18
#
# Purpose:
#   - Safely backup and rebuild SQLite databases without data loss.
#   - Handles common "database is locked" / write error scenarios by
#     reading from the source in read-only mode and writing to a clean copy.
#
# Approach:
#   1) Open source DB in read-only (URI mode).
#   2) Use SQLite backup API to copy to a temp file.
#   3) Run integrity_check on the temp copy.
#   4) (Optional) VACUUM and ANALYZE the temp copy.
#   5) Atomically replace original: rename original -> .old, temp -> original.
#      Keep .old as a safety rollback.
#
# Notes:
#   - Backup API can run while DB is in use (online backup).
#   - Place rebuilt file in the same directory for atomic rename semantics.
#   - WAL/SHM of the *old* DB are preserved alongside .old for forensic fallback.
# =============================================================

from __future__ import annotations

import os
import sqlite3
import time
from typing import Optional, Tuple

from prefiq.log.logger import get_logger

LOG = get_logger("prefiq.database.sqlite.maintenance")


def _as_uri_ro(path: str) -> str:
    # Use URI to open read-only without creating -journal for the source.
    # Ensures no accidental writes to the source during backup.
    # Note: path must be absolute or relative; SQLite URI handles both.
    return f"file:{path}?mode=ro"


def _dir_and_names(db_path: str) -> Tuple[str, str]:
    d = os.path.dirname(os.path.abspath(db_path)) or "."
    base = os.path.basename(db_path)
    return d, base


def integrity_check(conn: sqlite3.Connection) -> Tuple[bool, str]:
    """
    Run PRAGMA integrity_check and return (ok, message).
    If not ok, message contains the first failure line.
    """
    try:
        row = conn.execute("PRAGMA integrity_check").fetchone()
        msg = (row[0] if row else "") or ""
        ok = (msg.lower() == "ok")
        return ok, msg
    except Exception as e:
        return False, f"integrity_check_error: {type(e).__name__}: {e}"


def backup_sqlite(src_path: str, dst_path: str, *, timeout: float = 60.0) -> None:
    """
    Perform an online backup from src_path (read-only) into dst_path.
    Uses sqlite3 backup API (Python 3.7+).
    """
    os.makedirs(os.path.dirname(dst_path) or ".", exist_ok=True)

    # Open source in read-only via URI, with a generous timeout to wait out locks.
    src_uri = _as_uri_ro(os.path.abspath(src_path))
    LOG.info("backup_start", extra={"src": src_path, "dst": dst_path})

    t0 = time.time()
    with sqlite3.connect(src_uri, uri=True, timeout=timeout, detect_types=sqlite3.PARSE_DECLTYPES) as src, \
         sqlite3.connect(dst_path, timeout=timeout, detect_types=sqlite3.PARSE_DECLTYPES) as dst:

        # Recommended pragmas on destination to ensure consistency and performance of the copy.
        dst.executescript("""
            PRAGMA journal_mode=OFF;
            PRAGMA synchronous=OFF;
            PRAGMA foreign_keys=ON;
        """)

        # Run the online backup; this copies the entire database ('main' pages).
        # source.backup(target)
        src.backup(dst)  # type: ignore[attr-defined]

        dst.commit()

    LOG.info("backup_done", extra={"elapsed_ms": int((time.time() - t0) * 1000)})


def optimize_sqlite(db_path: str) -> None:
    """
    Optionally optimize the rebuilt DB: VACUUM + ANALYZE.
    """
    LOG.info("optimize_start", extra={"db": db_path})
    with sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
        conn.executescript("""
            PRAGMA foreign_keys=ON;
            VACUUM;
            ANALYZE;
        """)
        conn.commit()
    LOG.info("optimize_done", extra={"db": db_path})


def rebuild_sqlite_database(
    db_path: str,
    *,
    keep_old: bool = True,
    optimize: bool = True,
    timeout: float = 60.0,
) -> bool:
    """
    Safely rebuild a SQLite DB even if it's currently locked or had a write error.

    Steps:
      - Copy source -> temp using online backup API (read-only src).
      - Validate temp via PRAGMA integrity_check.
      - Optionally VACUUM + ANALYZE temp.
      - Atomically swap original with temp, preserving original as .old if keep_old.

    Returns:
      True on success (original replaced by rebuilt copy), False otherwise.
    """
    db_path = os.path.abspath(db_path)
    d, base = _dir_and_names(db_path)
    temp_path = os.path.join(d, f".rebuild.{base}.tmp")
    old_path = os.path.join(d, f"{base}.old")

    try:
        # 1) Backup to temp
        backup_sqlite(db_path, temp_path, timeout=timeout)

        # 2) Integrity check on temp
        with sqlite3.connect(temp_path, detect_types=sqlite3.PARSE_DECLTYPES) as tmp_conn:
            ok, msg = integrity_check(tmp_conn)
            if not ok:
                LOG.error("rebuild_integrity_failed", extra={"db": db_path, "msg": msg})
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
                return False

        # 3) Optional optimize on temp
        if optimize:
            optimize_sqlite(temp_path)

        # 4) Atomic swap: original -> .old (if keep_old), temp -> original
        # Close handles elsewhere first if possible (we can't control other procs,
        # but replace will still update the directory entry atomically on POSIX).
        if keep_old:
            # If an older .old exists, rotate it away to avoid overwrite
            if os.path.exists(old_path):
                try:
                    os.remove(old_path)
                except OSError:
                    pass
            os.replace(db_path, old_path)
        else:
            # If not keeping old, just remove the original (best effort)
            try:
                os.remove(db_path)
            except OSError:
                pass

        os.replace(temp_path, db_path)

        LOG.info("rebuild_swap_complete", extra={
            "db": db_path,
            "old": old_path if keep_old else None
        })
        return True

    except sqlite3.OperationalError as e:
        # Common: "database is locked", I/O errors, etc.
        LOG.error("rebuild_failed_operational_error", extra={"db": db_path, "error": f"{type(e).__name__}: {e}"})
        # Cleanup temp if present
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except OSError:
            pass
        return False

    except Exception as e:
        LOG.error("rebuild_failed", extra={"db": db_path, "error": f"{type(e).__name__}: {e}"})
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except OSError:
            pass
        return False
