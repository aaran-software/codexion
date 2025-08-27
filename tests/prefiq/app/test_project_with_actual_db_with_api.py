# # tests/prefiq/app/test_project_with_actual_db_with_api.py
# from __future__ import annotations
#
# import json
# import os
# import re
# import uuid
# from pathlib import Path
# from typing import Dict, Optional
#
# import pytest
# from fastapi import FastAPI
# from fastapi.testclient import TestClient
#
# # Mount ONLY the project router
# from apps.devmeta.devmeta.project.api import router as project_router  # type: ignore
#
# # Prefiq engine helpers
# from prefiq.database.connection import (
#     get_engine,
#     reset_engine,
#     reload_engine_from_env,
#     swap_engine,
# )
#
# # ──────────────────────────────────────────────────────────────────────────────
# # Small helpers
# # ──────────────────────────────────────────────────────────────────────────────
#
# def hdrs(tenant="t1", user="u1", roles="editor") -> Dict[str, str]:
#     return {
#         "X-Tenant-ID": tenant,
#         "X-User-ID": user,
#         "X-Roles": roles,
#         "Content-Type": "application/json",
#     }
#
# def _new_name(prefix: str = "Proj") -> str:
#     return f"{prefix}-{uuid.uuid4()}"
#
# def _read_text(p: Path) -> Optional[str]:
#     try:
#         return p.read_text(encoding="utf-8")
#     except Exception:
#         return None
#
# def _find_asset(filename: str) -> Optional[Path]:
#     """
#     Look in likely places for migration/data assets.
#     """
#     candidates = [
#         Path(__file__).parent / filename,
#         Path(__file__).parent / "assets" / filename,
#         Path("apps/devmeta/devmeta/project") / filename,
#         Path("apps/devmeta/devmeta/project/assets") / filename,
#         Path("apps/devmeta/devmeta/project/db/migrations") / filename,
#         Path(filename),
#     ]
#     for p in candidates:
#         if p.exists():
#             return p
#     # shallow search
#     for child in Path.cwd().rglob(filename):
#         return child
#     return None
#
# def _engine_name(e: object) -> str:
#     n = type(e).__name__.lower()
#     if "maria" in n or "mysql" in n:
#         return "mariadb"
#     if "sqlite" in n:
#         return "sqlite"
#     if "postgres" in n or "pg" in n:
#         return "postgres"
#     return n
#
# # ──────────────────────────────────────────────────────────────────────────────
# # SQL preprocessing for MariaDB
# # ──────────────────────────────────────────────────────────────────────────────
#
# _VENDOR_LINE_RE = re.compile(r"^([A-Za-z]+)\s*:\s*(.*)$")
#
# def _preprocess_vendor_lines(sql: str, keep: tuple[str, ...] = ("mariadb", "mysql")) -> str:
#     """
#     Drop lines prefixed with a different vendor tag (e.g., "SQLite: ...").
#     For kept vendors, strip "<Vendor>:" and keep the content.
#     """
#     out: list[str] = []
#     for line in sql.splitlines():
#         s = line.strip()
#         if not s:
#             continue
#         if s.startswith("--") or s.startswith("#"):
#             continue
#         m = _VENDOR_LINE_RE.match(s)
#         if m:
#             vendor, rest = m.group(1).lower(), m.group(2).strip()
#             if vendor in keep and rest:
#                 out.append(rest)
#             continue
#         out.append(line)
#     return "\n".join(out)
#
# def _strip_if_not_exists_for_mariadb(sql: str) -> str:
#     """
#     Older MariaDB versions can choke on IF NOT EXISTS for index/constraint.
#     """
#     sql = re.sub(r"CREATE\s+(UNIQUE\s+)?INDEX\s+IF\s+NOT\s+EXISTS", r"CREATE \1INDEX", sql, flags=re.IGNORECASE)
#     sql = re.sub(r"ADD\s+CONSTRAINT\s+IF\s+NOT\s+EXISTS", r"ADD CONSTRAINT", sql, flags=re.IGNORECASE)
#     return sql
#
# def _massage_sql_types_for_mariadb(sql: str) -> str:
#     """
#     Replace TEXT in PK / indexed columns with VARCHAR/CHAR suitable for MariaDB.
#     Safe replacements based on typical project schema:
#       id TEXT               -> CHAR(36)       (UUID-like)
#       tenant_id TEXT        -> VARCHAR(64)
#       owner_id TEXT         -> VARCHAR(64)
#       name TEXT             -> VARCHAR(255)   (used in unique index)
#       status TEXT           -> VARCHAR(24)
#       priority TEXT         -> VARCHAR(24)
#       description TEXT      -> TEXT           (unchanged)
#       tags JSON / meta JSON -> JSON (alias LONGTEXT on older MariaDB, OK)
#     """
#     # Only touch column *type* tokens, not values
#     repl = [
#         (r"\bid\s+TEXT\b",          "id CHAR(36)"),
#         (r"\btenant_id\s+TEXT\b",   "tenant_id VARCHAR(64)"),
#         (r"\bowner_id\s+TEXT\b",    "owner_id VARCHAR(64)"),
#         (r"\bname\s+TEXT\b",        "name VARCHAR(255)"),
#         (r"\bstatus\s+TEXT\b",      "status VARCHAR(24)"),
#         (r"\bpriority\s+TEXT\b",    "priority VARCHAR(24)"),
#     ]
#     for pat, sub in repl:
#         sql = re.sub(pat, sub, sql, flags=re.IGNORECASE)
#     return sql
#
# def _apply_sql_mariadb(engine: object, raw_sql: str) -> None:
#     """
#     Execute a SQL script on MariaDB, tolerating idempotency.
#     """
#     sql = raw_sql.replace("\r\n", "\n")
#     sql = _preprocess_vendor_lines(sql, keep=("mariadb", "mysql"))
#     sql = _massage_sql_types_for_mariadb(sql)
#     sql = _strip_if_not_exists_for_mariadb(sql)
#
#     # Split on ';' at a simple level (OK for our schema)
#     for stmt in (s.strip() for s in sql.split(";")):
#         if not stmt:
#             continue
#         try:
#             try:
#                 engine.execute(stmt)          # type: ignore[attr-defined]
#             except TypeError:
#                 engine.execute(stmt, {})      # type: ignore[attr-defined]
#         except Exception as e:
#             # swallow common idempotent/compat messages so re-runs are fine
#             msg = str(e).lower()
#             benign = (
#                 "already exists",
#                 "duplicate key name",
#                 "cannot add constraint",
#                 "check constraint is not supported",
#                 "syntax error near 'if not exists'",
#             )
#             if any(k in msg for k in benign):
#                 continue
#             raise
#
# def _drop_tables_if_exist(engine: object) -> None:
#     for t in ("migrations", "projects"):
#         try:
#             engine.execute(f"DROP TABLE IF EXISTS {t}")  # type: ignore[attr-defined]
#         except Exception:
#             pass
#
# # ──────────────────────────────────────────────────────────────────────────────
# # Fixtures: FORCE MariaDB + migrate
# # ──────────────────────────────────────────────────────────────────────────────
#
# REQUIRED_VARS = ("DB_HOST", "DB_PORT", "DB_USER", "DB_NAME")
#
# @pytest.fixture(scope="session", autouse=True)
# def _ensure_env_or_skip():
#     """
#     This test is for a REAL MariaDB. We *force* the engine and hydrate
#     missing creds from .env if possible; otherwise skip with a reason.
#     """
#     os.environ["TESTING"]   = "1"      # bypass Pydantic cache
#     os.environ["DB_ENGINE"] = "mariadb"
#     os.environ["DB_MODE"]   = "sync"
#
#     # Let .env fill in missing pieces if available
#     missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
#     if missing:
#         try:
#             from prefiq.settings.get_settings import load_settings
#             s = load_settings(force_refresh=True)
#             for k in REQUIRED_VARS + ("DB_PASS",):
#                 val = getattr(s, k, None)
#                 if val is not None and not os.getenv(k):
#                     os.environ[k] = str(val)
#         except Exception:
#             pass
#
#     still = [v for v in REQUIRED_VARS if not os.getenv(v)]
#     if still:
#         pytest.skip(f"MariaDB test skipped: missing {still}. "
#                     f"Set DB_* env vars or put them in .env (DB_ENGINE=mariadb, …).")
#
# @pytest.fixture(scope="session", autouse=True)
# def _bind_mariadb_engine(_ensure_env_or_skip):
#     """
#     Hard-swap to MariaDB for this session and assert it stuck.
#     """
#     reset_engine()
#     swap_engine("mariadb", mode="sync")   # hard override regardless of previous state
#     reload_engine_from_env(force_refresh=True)
#     eng = get_engine()
#     name = _engine_name(eng)
#     if name != "mariadb":
#         pytest.skip(f"Expected MariaDB engine, but got {name}. "
#                     f"Check DB_ENGINE/driver and that mariadb connector is installed.")
#     yield
#     reset_engine()
#
# @pytest.fixture(scope="session", autouse=True)
# def _migrate_projects_table(_bind_mariadb_engine):
#     eng = get_engine()
#     # clean slate to make runs idempotent
#     _drop_tables_if_exist(eng)
#
#     sql_path = _find_asset("0001_projects.sql")
#     assert sql_path and sql_path.exists(), "Could not find 0001_projects.sql"
#     sql_text = _read_text(sql_path)
#     assert sql_text and "CREATE TABLE" in sql_text, "Invalid migration content"
#     _apply_sql_mariadb(eng, sql_text)
#     return True
#
# @pytest.fixture()
# def client(_migrate_projects_table) -> TestClient:
#     app = FastAPI(title="Prefiq Project API (MariaDB)")
#     app.include_router(project_router, prefix="/api")
#     return TestClient(app)
#
# # ──────────────────────────────────────────────────────────────────────────────
# # The end-to-end test
# # ──────────────────────────────────────────────────────────────────────────────
#
# def test_project_end_to_end_on_mariadb(client: TestClient):
#     # Seed via assets if present
#     sample_path = _find_asset("projects.sample.json")
#     created_ids: list[str] = []
#
#     if sample_path:
#         data = json.loads(sample_path.read_text(encoding="utf-8"))
#         if isinstance(data, list):
#             for raw in data[:2]:
#                 payload = {"name": raw.get("name") or _new_name("Seed")}
#                 # copy safe fields
#                 for k in ("status", "priority", "tags", "meta", "description", "start_date", "due_date"):
#                     if k in raw:
#                         payload[k] = raw[k]
#                 r = client.post("/api/projects", json=payload, headers=hdrs(roles="editor"))
#                 assert r.status_code == 200, r.text
#                 created_ids.append(r.json()["id"])
#
#     # Always create one more via API
#     name = _new_name("API")
#     r = client.post("/api/projects", json={"name": name, "status": "new", "priority": "normal"}, headers=hdrs())
#     assert r.status_code == 200, r.text
#     rec = r.json()
#     created_ids.append(rec["id"])
#     assert rec["tenant_id"] == "t1"
#     assert rec["owner_id"] == "u1"
#
#     # Read
#     r = client.get(f"/api/projects/{rec['id']}", headers=hdrs())
#     assert r.status_code == 200
#     assert r.json()["id"] == rec["id"]
#
#     # List & filter
#     r = client.get("/api/projects?page=1&size=10&sort=-updated_at", headers=hdrs())
#     assert r.status_code == 200
#     lst = r.json()
#     assert any(item["id"] == rec["id"] for item in lst["items"])
#
#     r = client.get('/api/projects?filters={"status":"new"}', headers=hdrs())
#     assert r.status_code == 200
#     assert all(item["status"] == "new" for item in r.json()["items"])
#
#     # Row guard: other editor cannot update
#     r = client.patch(f"/api/projects/{rec['id']}", json={"description": "nope"}, headers=hdrs(user="u2", roles="editor"))
#     assert r.status_code == 403
#
#     # Owner can update
#     r = client.patch(f"/api/projects/{rec['id']}", json={"description": "ok"}, headers=hdrs(user="u1", roles="editor"))
#     assert r.status_code == 200 and r.json()["description"] == "ok"
#
#     # Transitions
#     r = client.post(f"/api/projects/{rec['id']}/transition", json={"to": "in_progress"}, headers=hdrs())
#     assert r.status_code == 200 and r.json()["status"] == "in_progress"
#     r = client.post(f"/api/projects/{rec['id']}/transition", json={"to": "done"}, headers=hdrs())
#     assert r.status_code == 200 and r.json()["status"] == "done"
#
#     # Delete policy
#     r = client.delete(f"/api/projects/{rec['id']}", headers=hdrs(roles="editor"))
#     assert r.status_code == 403
#     r = client.delete(f"/api/projects/{rec['id']}", headers=hdrs(roles="admin"))
#     assert r.status_code == 200 and r.json().get("ok") is True
#     r = client.get(f"/api/projects/{rec['id']}", headers=hdrs(roles="admin"))
#     assert r.status_code == 404
