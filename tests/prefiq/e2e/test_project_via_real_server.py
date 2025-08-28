# tests/prefiq/e2e/test_project_via_real_server.py

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Dict, Optional

import httpx
import pytest

# ---------- Config ----------
BASE_URL = os.environ.get("PREFIQ_BASE_URL", "http://127.0.0.1:5001")
SERVER_START_CMD = os.environ.get("PREFIQ_SERVER_CMD")  # optional override
SERVER_READY_PATH = "/healthz"                          # stronger readiness check
SERVER_START_TIMEOUT = 60.0
SERVER_SHUTDOWN_GRACE = 5.0


def _headers(tenant="t1", user="u1", roles="editor") -> Dict[str, str]:
    return {
        "X-Tenant-ID": tenant,
        "X-User-ID": user,
        "X-Roles": roles,
        "Content-Type": "application/json",
    }


def _new_name(prefix: str = "Proj") -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _start_server() -> subprocess.Popen:
    """
    Start 'prefiq server run dev' (or a user-provided command),
    without reloaders/watchers, so it runs in-foreground as a single process.
    Falls back to 'python -m prefiq.server dev' if the 'prefiq' entrypoint
    isn't available on PATH.
    """
    if SERVER_START_CMD:
        cmd = SERVER_START_CMD.split()
    else:
        cmd = ["prefiq", "server", "run", "dev", "--no-reload"]
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
        )
        return proc
    except FileNotFoundError:
        cmd = [sys.executable, "-m", "prefiq.server", "dev"]
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
        )
        return proc


def _wait_for_server(base_url: str, path: str = "/", timeout: float = 30.0) -> None:
    deadline = time.time() + timeout
    last_exc: Optional[Exception] = None
    with httpx.Client(timeout=2.0) as client:
        while time.time() < deadline:
            try:
                r = client.get(base_url + path)
                if r.status_code < 500:
                    return
            except Exception as e:
                last_exc = e
            time.sleep(0.25)
    if last_exc:
        raise last_exc
    raise RuntimeError("Server did not become ready")


@pytest.fixture(scope="session", autouse=True)
def real_server():
    """
    Boots the Prefiq dev server once for the whole session.
    You can point it at a running server by setting PREFIQ_BASE_URL and skip boot.
    """
    if os.environ.get("PREFIQ_USE_RUNNING", "").lower() in {"1", "true", "yes"}:
        _wait_for_server(BASE_URL, SERVER_READY_PATH, SERVER_START_TIMEOUT)
        yield None
        return

    proc = _start_server()
    try:
        _wait_for_server(BASE_URL, SERVER_READY_PATH, SERVER_START_TIMEOUT)
        yield proc
    finally:
        if proc and proc.poll() is None:
            try:
                if sys.platform.startswith("win"):
                    proc.send_signal(signal.CTRL_BREAK_EVENT)  # type: ignore[attr-defined]
                else:
                    proc.terminate()
            except Exception:
                pass
            t0 = time.time()
            while proc.poll() is None and time.time() - t0 < SERVER_SHUTDOWN_GRACE:
                time.sleep(0.2)
            if proc.poll() is None:
                try:
                    proc.kill()
                except Exception:
                    pass


# -------------------- Debug helpers --------------------

def _debug_ctx(client: httpx.Client, roles="editor", tenant="t1", user="u1") -> str:
    try:
        r = client.get(f"{BASE_URL}/api/projects/_debug/ctx", headers=_headers(tenant=tenant, user=user, roles=roles))
        return f"{r.status_code} {r.text}"
    except Exception as e:
        return f"<ctx fetch error: {e!r}>"

def _debug_openapi(client: httpx.Client) -> str:
    try:
        r = client.get(f"{BASE_URL}/openapi.json")
        if r.status_code != 200:
            return f"openapi status={r.status_code} body={r.text[:500]}"
        # Trim to just our paths for readability
        data = r.json()
        paths = data.get("paths", {})
        interesting = {k: v for k, v in paths.items() if k.startswith("/api/projects")}
        return json.dumps(interesting, indent=2)[:2000]
    except Exception as e:
        return f"<openapi fetch error: {e!r}>"

def _post_with_debug(client: httpx.Client, path: str, payload: dict, roles="editor", tenant="t1", user="u1") -> httpx.Response:
    url = path if path.startswith("http") else (BASE_URL + path)
    r = client.post(url, json=payload, headers=_headers(tenant=tenant, user=user, roles=roles))
    if r.status_code != 200:
        print("\n--- DEBUG: POST failure ---------------------------------")
        print("URL:", url)
        print("Payload:", json.dumps(payload, ensure_ascii=False))
        print("Response:", r.status_code, r.text)
        print("Context:", _debug_ctx(client, roles=roles, tenant=tenant, user=user))
        print("OpenAPI /api/projects*:", _debug_openapi(client))
        print("----------------------------------------------------------\n")
    return r


# -------------------- Seed helper --------------------

def _seed_from_assets(client: httpx.Client):
    """
    If sample data exists in the repo, POST a couple of rows using the real API.
    """
    asset = Path("apps/devmeta/devmeta/project/assets/projects.sample.json")
    if asset.exists():
        try:
            data = json.loads(asset.read_text(encoding="utf-8"))
        except Exception:
            return
        if isinstance(data, list):
            for raw in data[:2]:
                payload = {"name": raw.get("name") or _new_name("Seed")}
                for k in ("status", "priority", "tags", "meta", "description", "start_date", "due_date"):
                    if k in raw:
                        payload[k] = raw[k]
                r = _post_with_debug(client, "/api/projects", payload, roles="editor")
                assert r.status_code == 200, f"asset seed failed: {r.text}"


# -------------------- Main test --------------------

@pytest.mark.mariadb
def test_project_end_to_end_on_mariadb_via_server(real_server):
    """
    Spins up the Prefiq dev server and performs the original project test workflow
    via real HTTP calls (create, get, list/sort/filter, guarded update, transitions, delete).
    """
    with httpx.Client(base_url=BASE_URL, timeout=5.0) as client:
        # Optional: quick sanity on readiness endpoint
        rr = client.get(f"{BASE_URL}{SERVER_READY_PATH}")
        assert rr.status_code in (200, 204), f"Server not ready: {rr.status_code} {rr.text}"

        # Seed (optional)
        _seed_from_assets(client)

        # Create one explicitly
        name = _new_name("API")
        r = _post_with_debug(client, "/api/projects", {"name": name, "status": "new", "priority": "normal"})
        assert r.status_code == 200, r.text
        rec = r.json()
        pid = rec["id"]
        assert rec["tenant_id"] == "t1"
        assert rec["owner_id"] == "u1"

        # Read
        r = client.get(f"/api/projects/{pid}", headers=_headers())
        assert r.status_code == 200
        assert r.json()["id"] == pid

        # List + sort
        r = client.get("/api/projects", params={"page": 1, "size": 10, "sort": "-updated_at"}, headers=_headers())
        assert r.status_code == 200
        lst = r.json()
        assert isinstance(lst.get("items"), list) and "total" in lst
        assert any(it["id"] == pid for it in lst["items"])

        # Filter
        r = client.get("/api/projects", params={"filters": json.dumps({"status": "new"})}, headers=_headers())
        assert r.status_code == 200
        assert all(it["status"] == "new" for it in r.json()["items"])

        # Row guard: another editor cannot update
        r = client.patch(f"/api/projects/{pid}", json={"description": "nope"}, headers=_headers(user="u2", roles="editor"))
        assert r.status_code == 403

        # Owner can update
        r = client.patch(f"/api/projects/{pid}", json={"description": "ok"}, headers=_headers(user="u1", roles="editor"))
        assert r.status_code == 200 and r.json()["description"] == "ok"

        # Transitions
        r = client.post(f"/api/projects/{pid}/transition", json={"to": "in_progress"}, headers=_headers())
        assert r.status_code == 200 and r.json()["status"] == "in_progress"
        r = client.post(f"/api/projects/{pid}/transition", json={"to": "done"}, headers=_headers())
        assert r.status_code == 200 and r.json()["status"] == "done"

        # Delete policy: editor forbidden; admin allowed
        r = client.delete(f"/api/projects/{pid}", headers=_headers(roles="editor"))
        assert r.status_code == 403

        r = client.delete(f"/api/projects/{pid}", headers=_headers(roles="admin"))
        assert r.status_code == 200 and r.json().get("ok") is True

        # After delete -> 404
        r = client.get(f"/api/projects/{pid}", headers=_headers(roles="admin"))
        assert r.status_code == 404

        # Multitenancy isolation quick check
        r = _post_with_debug(client, "/api/projects", {"name": _new_name("Iso"), "status": "new"}, roles="editor", tenant="t1", user="u1")
        assert r.status_code == 200
        pid2 = r.json()["id"]
        r = client.get(f"/api/projects/{pid2}", headers=_headers(tenant="t2", user="u2", roles="admin"))
        assert r.status_code == 404
        r = client.get("/api/projects", headers=_headers(tenant="t2", user="u2", roles="admin"))
        assert r.status_code == 200
        assert not any(it["id"] == pid2 for it in r.json().get("items", []))
