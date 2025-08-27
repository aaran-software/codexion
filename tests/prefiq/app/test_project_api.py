# # tests/test_project_api.py
#
# from __future__ import annotations
#
# import uuid
# from typing import Dict
#
# import pytest
# from fastapi import FastAPI
# from fastapi.testclient import TestClient
#
# # Mount ONLY the project router for focused tests
# from apps.devmeta.devmeta.project.api import router as project_router
#
#
# def make_app() -> FastAPI:
#     app = FastAPI(title="Prefiq Test API")
#     app.include_router(project_router, prefix="/api")
#     return app
#
#
# def headers(tenant="t1", user="u1", roles="editor") -> Dict[str, str]:
#     return {
#         "X-Tenant-ID": tenant,
#         "X-User-ID": user,
#         "X-Roles": roles,
#         "Content-Type": "application/json",
#     }
#
#
# @pytest.fixture(scope="function")
# def client() -> TestClient:
#     app = make_app()
#     return TestClient(app)
#
#
# def _new_name(prefix: str = "Proj") -> str:
#     return f"{prefix}-{uuid.uuid4()}"
#
#
# # --- Happy path: editor creates, reads, lists, updates own, transitions, deletes (admin) --- #
#
# def test_create_project_as_editor(client: TestClient):
#     name = _new_name("Create")
#     payload = {
#         "name": name,
#         "status": "new",
#         "priority": "high",
#         "start_date": "2025-08-01",
#         "due_date": "2025-08-20",
#         "tags": ["e2e", "api"]
#     }
#     r = client.post("/api/projects", json=payload, headers=headers(roles="editor"))
#     assert r.status_code == 200, r.text
#     data = r.json()
#     assert data["name"] == name
#     assert data["tenant_id"] == "t1"
#     assert data["owner_id"] == "u1"
#     assert data["status"] == "new"
#     assert data["priority"] == "high"
#     assert "created_at" in data and "updated_at" in data
#
#
# def test_get_and_list_projects(client: TestClient):
#     # create two records in same tenant
#     id_list = []
#     for _ in range(2):
#         r = client.post("/api/projects", json={"name": _new_name("List")}, headers=headers())
#         assert r.status_code == 200
#         id_list.append(r.json()["id"])
#
#     # GET one
#     rid = id_list[0]
#     r = client.get(f"/api/projects/{rid}", headers=headers())
#     assert r.status_code == 200
#     one = r.json()
#     assert one["id"] == rid
#
#     # LIST with pagination + sort
#     r = client.get("/api/projects?page=1&size=10&sort=-updated_at", headers=headers())
#     assert r.status_code == 200
#     lst = r.json()
#     assert "items" in lst and "total" in lst
#     assert any(item["id"] == rid for item in lst["items"])
#
#     # LIST with filter
#     r = client.get('/api/projects?filters={"status":"new"}', headers=headers())
#     assert r.status_code == 200
#     flt = r.json()
#     assert all(item["status"] == "new" for item in flt["items"])
#
#
# def test_update_project_row_guard_and_fields(client: TestClient):
#     # create as editor u1
#     r = client.post("/api/projects", json={"name": _new_name("Upd"), "status": "new"}, headers=headers(user="u1", roles="editor"))
#     assert r.status_code == 200
#     proj = r.json()
#     pid = proj["id"]
#
#     # try update by DIFFERENT editor u2 (should be 403 by row guard)
#     r = client.patch(f"/api/projects/{pid}", json={"description": "not mine"}, headers=headers(user="u2", roles="editor"))
#     assert r.status_code == 403
#
#     # update by owner u1 (ok)
#     r = client.patch(f"/api/projects/{pid}", json={"description": "mine"}, headers=headers(user="u1", roles="editor"))
#     assert r.status_code == 200
#     assert r.json()["description"] == "mine"
#
#     # editor cannot change owner_id
#     r = client.patch(f"/api/projects/{pid}", json={"owner_id": "uX"}, headers=headers(user="u1", roles="editor"))
#     assert r.status_code in (403, 422)
#
#
# def test_status_transition_rules(client: TestClient):
#     # new -> in_progress (editor allowed)
#     r = client.post("/api/projects", json={"name": _new_name("Trans"), "status": "new"}, headers=headers(roles="editor"))
#     assert r.status_code == 200
#     pid = r.json()["id"]
#
#     # Start
#     r = client.post(f"/api/projects/{pid}/transition", json={"to": "in_progress"}, headers=headers(roles="editor"))
#     assert r.status_code == 200
#     assert r.json()["status"] == "in_progress"
#
#     # Complete
#     r = client.post(f"/api/projects/{pid}/transition", json={"to": "done"}, headers=headers(roles="editor"))
#     assert r.status_code == 200
#     assert r.json()["status"] == "done"
#
#     # done -> archived (editor allowed)
#     r = client.post(f"/api/projects/{pid}/transition", json={"to": "archived"}, headers=headers(roles="editor"))
#     assert r.status_code == 200
#     assert r.json()["status"] == "archived"
#
#     # archived -> any (disallowed)
#     r = client.post(f"/api/projects/{pid}/transition", json={"to": "in_progress"}, headers=headers(roles="editor"))
#     assert r.status_code == 422
#
#
# def test_delete_policy(client: TestClient):
#     # create one
#     r = client.post("/api/projects", json={"name": _new_name("Del")}, headers=headers(roles="editor"))
#     assert r.status_code == 200
#     pid = r.json()["id"]
#
#     # editor cannot delete
#     r = client.delete(f"/api/projects/{pid}", headers=headers(roles="editor"))
#     assert r.status_code == 403
#
#     # admin can delete
#     r = client.delete(f"/api/projects/{pid}", headers=headers(roles="admin"))
#     assert r.status_code == 200
#     assert r.json()["ok"] is True
#
#     # subsequent get -> 404
#     r = client.get(f"/api/projects/{pid}", headers=headers(roles="admin"))
#     assert r.status_code == 404
#
#
# # --- Validation & query guardrails --- #
#
# def test_invalid_filters_and_sort(client: TestClient):
#     # invalid JSON in filters -> 400
#     r = client.get('/api/projects?filters={not_json}', headers=headers())
#     assert r.status_code == 400
#
#     # invalid transition target -> 422
#     r = client.post("/api/projects/does-not-exist/transition", json={"to": "waka"}, headers=headers())
#     # make a real project to assert 422 strictly
#     r2 = client.post("/api/projects", json={"name": _new_name("V")}, headers=headers())
#     pid = r2.json()["id"]
#     r3 = client.post(f"/api/projects/{pid}/transition", json={"to": "waka"}, headers=headers())
#     assert r3.status_code == 422
#
#     # due_date < start_date -> 422 on create
#     bad = {
#         "name": _new_name("BadDate"),
#         "start_date": "2025-09-10",
#         "due_date": "2025-09-01"
#     }
#     rb = client.post("/api/projects", json=bad, headers=headers())
#     assert rb.status_code == 422
#
#
# def test_multitenancy_isolation(client: TestClient):
#     # Create in tenant t1
#     r1 = client.post("/api/projects", json={"name": _new_name("Iso")}, headers=headers(tenant="t1", user="u1", roles="editor"))
#     assert r1.status_code == 200
#     pid = r1.json()["id"]
#
#     # Cannot read from another tenant t2
#     r2 = client.get(f"/api/projects/{pid}", headers=headers(tenant="t2", user="u2", roles="admin"))
#     assert r2.status_code == 404
#
#     # List in t2 should not include t1 record
#     r3 = client.get("/api/projects", headers=headers(tenant="t2", user="u2", roles="admin"))
#     assert r3.status_code == 200
#     lst = r3.json()
#     assert not any(item["id"] == pid for item in lst["items"])
