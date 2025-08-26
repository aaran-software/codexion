from __future__ import annotations
import os
from pathlib import Path

# Force the same absolute DB file you used earlier (adjust if needed)
DB_FILE = Path(r"E:\Workspace\codexion\database\devmeta.sqlite")
os.environ.setdefault("DB_ENGINE", "sqlite")
os.environ.setdefault("DB_MODE", "sync")
os.environ["DB_NAME"] = str(DB_FILE)
os.environ.setdefault("DB_TEST_MYSQL", "0")
os.environ.setdefault("DB_TEST_PG", "0")
os.environ.setdefault("DB_POOL_WARMUP", "0")

from prefiq.core.application import Application
from prefiq.core.service_providers import get_service_providers
from prefiq.database.connection import get_engine

def boot():
    app = Application.get_app()
    for p in get_service_providers():
        app.register(p)
    app.boot()

def fetch_all(cur):
    # Works for sqlite (tuples) or row objects
    rows = cur.fetchall() if hasattr(cur, "fetchall") else []
    cols = [d[0] for d in cur.description] if getattr(cur, "description", None) else []
    return cols, rows

def dump_table(eng, table, limit=10):
    cur = eng.execute(f"SELECT * FROM {table} LIMIT {limit};")
    cols, rows = fetch_all(cur)
    print(f"\n== {table} (up to {limit}) ==")
    if not rows:
        print("(no rows)")
        return
    print(" | ".join(cols))
    for r in rows:
        # r may be tuple or dict-like
        if isinstance(r, (list, tuple)):
            print(" | ".join(str(x) for x in r))
        else:
            print(" | ".join(str(r.get(c)) for c in cols))

def main():
    boot()
    eng = get_engine()

    # Quick counts (fetch while connection is live)
    for t in ["projects", "tasks", "task_assignees", "comments", "activity_logs"]:
        cur = eng.execute(f"SELECT COUNT(*) FROM {t};")
        cnt = cur.fetchone()[0] if hasattr(cur, "fetchone") else 0
        print(f"{t}: {cnt}")

    # Sample dumps
    for t in ["projects", "tasks", "task_assignees", "comments", "activity_logs"]:
        dump_table(eng, t, limit=10)

if __name__ == "__main__":
    print("DB:", DB_FILE)
    main()
