import os
import configparser
from cortex.config.apps.apps_cfg import (
    create_apps_cfg,
    # delete_apps_cfg,
    get_registered_apps,
    add_app,
    remove_app,
    update_app_version,
)
from cortex.core.settings import get_settings
from pathlib import Path

settings = get_settings()
CFG_PATH = Path(settings.project_root) / "config" / "apps.cfg"


def setup_module(module):
    # delete_apps_cfg()
    create_apps_cfg()


# def teardown_module(module):
#     delete_apps_cfg()


def test_create_apps_cfg():
    assert os.path.exists(CFG_PATH), "❌ apps.cfg was not created"
    print("✅ apps.cfg created successfully.")


def test_add_app():
    add_app("crm", "0.9.5")
    apps = get_registered_apps()
    assert "crm" in apps
    print("✅ App 'crm' added to apps.cfg")


def test_get_registered_apps():
    add_app("cxsun", "1.2.0")
    add_app("ecart", "2.0.1")
    apps = get_registered_apps()
    assert "cxsun" in apps
    assert "ecart" in apps
    print("✅ Retrieved registered apps successfully")


def test_update_app_version():
    update_app_version("crm", "1.0.0")
    config = configparser.ConfigParser()
    config.read(CFG_PATH)
    assert config["crm"]["version"] == "1.0.0"
    print("✅ App version updated successfully")


def test_remove_app():
    remove_app("cxsun")
    apps = get_registered_apps()
    assert "cxsun" not in apps
    print("✅ App 'cxsun' removed successfully")
