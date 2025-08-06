from cortex.database.migrations.loader import get_registered_apps


def test_read_apps_cfg():
    apps = get_registered_apps()
    assert isinstance(apps, list)
    assert "crm" in apps  # Replace with known app
