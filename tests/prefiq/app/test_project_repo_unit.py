# from fastapi.testclient import TestClient
# from fastapi import FastAPI
# from apps.devmeta.devmeta.project.api import router as project_router
#
# app = FastAPI()
# app.include_router(project_router, prefix="/api")
# client = TestClient(app)
#
# def hdrs(tenant="t1", user="u1", roles="editor"):
#     return {"X-Tenant-ID": tenant, "X-User-ID": user, "X-Roles": roles, "Content-Type": "application/json"}
#
# def test_admin_delete_smoke():
#     r = client.post("/api/projects", json={"name": "X"}, headers=hdrs())
#     assert r.status_code == 200
#     pid = r.json()["id"]
#
#     # editor cannot delete
#     r = client.delete(f"/api/projects/{pid}", headers=hdrs(roles="editor"))
#     assert r.status_code == 403
#
#     # admin can
#     r = client.delete(f"/api/projects/{pid}", headers=hdrs(roles="admin"))
#     assert r.status_code == 200
#     assert r.json().get("ok") is True
