# prefiq/database/migrations/rollback.py

from prefiq.database.schemas.queries import select_all, delete
from prefiq.database.migrations.loader import resolve_and_load
import traceback

# System/core migrations that should NEVER be rolled back
PROTECTED_MIGRATIONS = {
    "core": ["migrations"],
}

def is_protected(app: str, name: str) -> bool:
    return name in PROTECTED_MIGRATIONS.get(app, [])


def rollback(step: int = 1):
    """
    Rollback the last `step` number of migrations in reverse order.
    """
    applied = select_all("migrations", columns="app, name, order_index")
    if not applied:
        print("ℹ️  No migrations to rollback.")
        return

    # Sort by latest applied first
    applied.sort(key=lambda x: x[2], reverse=True)

    rolled_back = 0

    for row in applied[:step]:
        app, name, index = row

        if is_protected(app, name):
            print(f"🛑 Skipping protected migration: {app}.{name}")
            continue

        try:
            mod, _ = resolve_and_load(app, name)

            if not hasattr(mod, "down"):
                print(f"⚠️  Migration {app}.{name} has no `down()` method.")
                continue

            print(f"⏪ Rolling back {app}.{name} ...")
            mod.down()

            delete("migrations", "app = %s AND name = %s", (app, name))
            rolled_back += 1

        except Exception as e:
            print(f"❌ Failed to rollback {app}.{name}: {e}")
            traceback.print_exc()
            break

    if rolled_back:
        print(f"✅ Rolled back {rolled_back} migration(s).")
