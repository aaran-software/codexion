import types
from typing import List

import pytest

# Module under test
import prefiq.cli.checkup.boot_doctor as boot_doctor


def test_boot_doctor_happy_path(monkeypatch):
    """Settings load -> providers discovered -> application booted."""
    # 1) load_settings -> dummy
    from tests.conftest import DummySettings
    monkeypatch.setattr(
        boot_doctor, "load_settings", lambda *a, **k: DummySettings(), raising=True
    )

    # 2) PROVIDERS -> two fake providers
    class P1: __name__ = "SettingsProvider"
    class P2: __name__ = "ProfilesProvider"
    monkeypatch.setattr(boot_doctor, "PROVIDERS", [P1, P2], raising=True)

    # 3) Application.get_app() -> fake app that records registrations + boot
    class FakeApp:
        def __init__(self):
            self.registered: List[type] = []
            self.boot_called = False
        def register(self, p): self.registered.append(p)
        def boot(self): self.boot_called = True

    monkeypatch.setattr(
        boot_doctor.Application,
        "get_app",
        classmethod(lambda cls: FakeApp()),
        raising=True,
    )

    ok, results = boot_doctor.run_boot_diagnostics()
    assert ok is True

    # Names + success flags in order
    assert [(r.name, r.ok) for r in results] == [
        ("Settings loaded", True),
        ("Providers discovered", True),
        ("Application booted", True),
    ]


def test_boot_doctor_settings_failure(monkeypatch):
    """If settings fail to load, doctor exits early with a single failing check."""
    def _raise(*a, **k):
        raise RuntimeError("boom")
    monkeypatch.setattr(boot_doctor, "load_settings", _raise, raising=True)

    ok, results = boot_doctor.run_boot_diagnostics()
    assert ok is False
    assert len(results) == 1
    assert results[0].name == "Settings loaded"
    assert results[0].ok is False
    assert "boom" in results[0].detail
