# import types
# import pytest
#
# import prefiq.cli.checkup.database_doctor as db_doctor
#
#
# def _mk_settings(**over):
#     from tests.conftest import DummySettings
#     s = DummySettings()
#     for k, v in over.items():
#         setattr(s, k, v)
#     return s
#
#
# def test_database_doctor_skips_when_provider_missing(monkeypatch):
#     # Settings OK
#     monkeypatch.setattr(
#         db_doctor, "load_settings", lambda *a, **k: _mk_settings(), raising=True
#     )
#     # PROVIDERS lacks DatabaseProvider
#     class P1: __name__ = "SettingsProvider"
#     class P2: __name__ = "ProfilesProvider"
#     monkeypatch.setattr(db_doctor, "PROVIDERS", [P1, P2], raising=True)
#
#     ok, results = db_doctor.run_database_diagnostics(strict=False)
#     # Non-strict: overall OK, but shows provider missing and "skipped"
#     assert ok is True
#     names = [r.name for r in results]
#     assert "Database provider configured" in names
#     assert "Database checks" in names
#     prov_row = next(r for r in results if r.name == "Database provider configured")
#     skip_row = next(r for r in results if r.name == "Database checks")
#     assert prov_row.ok is False
#     assert skip_row.detail.startswith("skipped")
#
#
# def test_database_doctor_strict_fails_when_provider_missing(monkeypatch):
#     monkeypatch.setattr(
#         db_doctor, "load_settings", lambda *a, **k: _mk_settings(), raising=True
#     )
#     class P1: __name__ = "SettingsProvider"
#     class P2: __name__ = "ProfilesProvider"
#     monkeypatch.setattr(db_doctor, "PROVIDERS", [P1, P2], raising=True)
#
#     ok, results = db_doctor.run_database_diagnostics(strict=True)
#     assert ok is False
#     prov_row = next(r for r in results if r.name == "Database provider configured")
#     assert prov_row.ok is False
#
#
# def test_database_doctor_runs_when_provider_present(monkeypatch):
#     """With a DatabaseProvider and a fake engine, doctor should perform probes."""
#     # Settings OK
#     monkeypatch.setattr(
#         db_doctor, "load_settings", lambda *a, **k: _mk_settings(), raising=True
#     )
#
#     # PROVIDERS contains a DatabaseProvider-like class
#     class DatabaseProvider: pass
#     class P1: __name__ = "SettingsProvider"
#     class P2: __name__ = "ProfilesProvider"
#     monkeypatch.setattr(db_doctor, "PROVIDERS", [P1, P2, DatabaseProvider], raising=True)
#
#     # Fake engine that satisfies the probes
#     class FakeEngine:
#         def __init__(self): self.executed = []
#         def test_connection(self): return True
#         def execute(self, sql):
#             self.executed.append(sql)
#             class _C:
#                 def fetchone(self_inner): return (1,)
#             return _C()
#
#     # Patch resolver to return FakeEngine (and simulate import OK)
#     monkeypatch.setattr(
#         db_doctor, "_try_import_engine", lambda: (lambda: FakeEngine(), None), raising=True
#     )
#
#     ok, results = db_doctor.run_database_diagnostics(strict=True)
#     assert ok is True
#
#     names = [r.name for r in results]
#     assert names[:3] == ["Settings loaded", "Database provider configured", "Engine resolved"]
#     assert "DB connectivity" in names
#     # Metadata/DDL may be present depending on environment; assert no failures
#     assert all(r.ok for r in results)
