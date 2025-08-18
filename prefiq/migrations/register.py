from __future__ import annotations
from prefiq.migrations.migrator import MigrationRegistry
from prefiq.migrations import m001_bootstrap as m001  # noqa: E402,E999 (pseudo-import; use valid name)

registry = MigrationRegistry()

# Register with different IDs for clarity
# IMPORTANT: use valid Python module names; actual file should be `m001_bootstrap.py`
# Below shows intent—adjust names to your filename.
try:
    registry.register_async("001_bootstrap", m001.up_async)
except AttributeError:
    pass

try:
    registry.register("001_bootstrap_sync", m001.up_sync)
except AttributeError:
    pass
