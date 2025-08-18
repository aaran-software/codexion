# apps/devmeta/sync/ndjson.py
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Iterable, Iterator, List, Optional, Sequence, Tuple, Dict, Any

from prefiq.log.logger import get_logger
from apps.devmeta.core.helper import connect_sqlite, DEFAULT_SQLITE_PATH

LOG = get_logger("prefiq.devmeta.sync.ndjson")

# Default set of tables to sync as DevMeta grows.
DEFAULT_TABLES: Tuple[str, ...] = (
    "todos",
    # future:
    # "notes",
    # "logs",
    # "projects",
    # "roadmap",
    # "reviews",
    # "assignees",
)

# ---------------------------- helpers ---------------------------- #

def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

def _table_columns(conn, table: str) -> List[str]:
    cols = []
    for row in conn.execute(f'PRAGMA table_info("{table}")').fetchall():
        cols.append(row["name"])
    return cols

def _iter_table_rows(conn, table: str) -> Iterator[Dict[str, Any]]:
    # Use row_factory=sqlite3.Row from connect_sqlite
    for r in conn.execute(f'SELECT * FROM "{table}"'):
        yield dict(r)

def _filter_columns(rec: Dict[str, Any], cols: Sequence[str]) -> Dict[str, Any]:
    return {k: rec.get(k) for k in cols if k in rec}

def _has_row_with_id(conn, table: str, row_id: Any) -> bool:
    cur = conn.execute(f'SELECT 1 FROM "{table}" WHERE id = ? LIMIT 1', (row_id,))
    return cur.fetchone() is not None

def _insert_row(conn, table: str, values: Dict[str, Any]) -> None:
    if not values:
        return
    keys = list(values.keys())
    qs = ",".join("?" for _ in keys)
    sql = f'INSERT INTO "{table}" ({",".join(keys)}) VALUES ({qs})'
    conn.execute(sql, tuple(values[k] for k in keys))

def _update_row_by_id(conn, table: str, values: Dict[str, Any]) -> None:
    if "id" not in values:
        return
    row_id = values["id"]
    cols = [k for k in values.keys() if k != "id"]
    if not cols:
        return
    sets = ",".join(f'{k} = ?' for k in cols)
    sql = f'UPDATE "{table}" SET {sets} WHERE id = ?'
    conn.execute(sql, tuple(values[c] for c in cols) + (row_id,))

def _valid_tables(conn, requested: Optional[Iterable[str]]) -> List[str]:
    if requested is None:
        return list(DEFAULT_TABLES)
    req = [t for t in requested if t and isinstance(t, str)]
    # ensure they exist
    existing = {
        r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type IN ('table','view')"
        ).fetchall()
    }
    return [t for t in req if t in existing]

# ----------------------------- export ---------------------------- #

def export_ndjson(
    out_path: str | os.PathLike[str],
    tables: Optional[Iterable[str]] = None,
    db_path: Optional[str] = None,
) -> int:
    """
    Export rows as NDJSON. Each line is a JSON object with a `_table` key.
    Returns number of records written.
    """
    dbp = db_path or DEFAULT_SQLITE_PATH
    out_file = Path(out_path)
    _ensure_parent(out_file)

    total = 0
    with connect_sqlite(dbp) as conn, out_file.open("w", encoding="utf-8") as f:
        tlist = _valid_tables(conn, tables)
        LOG.info("export_start", extra={"db": dbp, "out": str(out_file), "tables": tlist})

        for t in tlist:
            cols = _table_columns(conn, t)
            if not cols:
                continue

            for row in _iter_table_rows(conn, t):
                # Only dump actual columns to avoid hidden Row attrs
                obj = _filter_columns(row, cols)
                obj["_table"] = t
                f.write(json.dumps(obj, ensure_ascii=False) + "\n")
                total += 1

    LOG.info("export_done", extra={"count": total})
    return total

# ----------------------------- import ---------------------------- #

def import_ndjson(
    in_path: str | os.PathLike[str],
    tables: Optional[Iterable[str]] = None,
    mode: str = "insert",  # "insert" | "upsert"
    db_path: Optional[str] = None,
) -> int:
    """
    Import NDJSON into SQLite.

    - mode="insert": INSERT rows as-is (will error on duplicate 'id' unless SQLite autoincrements)
    - mode="upsert": if 'id' exists, UPDATE; otherwise INSERT
    - tables: optional whitelist. If provided, only those `_table` records are applied.
    Returns number of rows applied.
    """
    mode = (mode or "insert").lower()
    if mode not in ("insert", "upsert"):
        raise ValueError("mode must be 'insert' or 'upsert'")

    dbp = db_path or DEFAULT_SQLITE_PATH
    in_file = Path(in_path)
    if not in_file.exists():
        LOG.warning("import_file_missing", extra={"path": str(in_file)})
        return 0

    applied = 0
    with connect_sqlite(dbp) as conn, in_file.open("r", encoding="utf-8") as f:
        whitelist = set(tables) if tables else None
        LOG.info("import_start", extra={"db": dbp, "in": str(in_file), "mode": mode, "tables": list(whitelist) if whitelist else None})

        # Pre-cache schema per table to avoid repetitive PRAGMA calls
        schema_cache: Dict[str, List[str]] = {}
        valid_cache: Dict[str, bool] = {}

        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                LOG.warning("import_skip_bad_json", extra={"line": line[:80]})
                continue

            table = obj.pop("_table", None)
            if not table or not isinstance(table, str):
                LOG.warning("import_skip_no_table", extra={"line": line[:80]})
                continue

            if whitelist and table not in whitelist:
                continue

            # Validate table exists once
            if table not in valid_cache:
                exists = conn.execute(
                    "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
                    (table,),
                ).fetchone() is not None
                valid_cache[table] = exists
                if not exists:
                    LOG.warning("import_skip_unknown_table", extra={"table": table})
                    continue
            if not valid_cache[table]:
                continue

            # Cache columns
            if table not in schema_cache:
                schema_cache[table] = _table_columns(conn, table)
            cols = schema_cache[table]

            # Keep only known columns
            values = _filter_columns(obj, cols)

            if mode == "insert" or "id" not in values:
                _insert_row(conn, table, values)
                applied += 1
                continue

            # upsert logic (by id)
            if _has_row_with_id(conn, table, values["id"]):
                _update_row_by_id(conn, table, values)
            else:
                _insert_row(conn, table, values)
            applied += 1

        conn.commit()

    LOG.info("import_done", extra={"count": applied})
    return applied
