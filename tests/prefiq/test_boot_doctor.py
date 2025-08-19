# ---------------------------------------------------------------------------
# tests/test_boot_doctor.py (lightweight unit test)
from __future__ import annotations

import types
import sys
import builtins

# The test focuses on BootDoctor orchestration; it stubs heavy dependencies

def test_boot_doctor_runs(monkeypatch):
    # Stub Application
    class _App:
        provider_registry = []
        _instance = None
        def __init__(self):
            self._providers = []
        @classmethod
        def get_app(cls):
            cls._instance = cls._instance or _App()
            return cls._instance
        def register(self, p):
            self._providers.append(p if isinstance(p, type) else type(p))
        def boot(self):
            return None

    # Fake module for Application
    m = types.ModuleType("prefiq.core.contracts.base_provider")
    m.Application = _App
    monkeypatch.setitem(sys.modules, "prefiq.core.contracts.base_provider", m)

    # Fake settings
    class _S: ENV = "test"; DB_ENGINE = "sqlite"; DB_MODE = "sync"
    def _ls(): return _S()
    sm = types.ModuleType("prefiq.settings.get_settings")
    sm.load_settings = _ls
    monkeypatch.setitem(sys.modules, "prefiq.settings.get_settings", sm)

    # Fake providers list
    pm = types.ModuleType("cortex.runtime.service_providers")
    pm.PROVIDERS = []
    monkeypatch.setitem(sys.modules, "cortex.runtime.service_providers", pm)

    # Fake engine
    em = types.ModuleType("prefiq.database.connection")
    class _E:
        def test_connection(self):
            return True
    em.get_engine = lambda: _E()
    monkeypatch.setitem(sys.modules, "prefiq.database.connection", em)

    # Import and run
    from prefiq.cli.checkup.boot_doctor import BootDoctor
    r = BootDoctor().run()
    assert r.ok, r.to_text()