import os

def get_root_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def get_apps_dir():
    return os.path.join(get_root_dir(), "apps")

def get_config_path():
    return os.path.join(get_apps_dir(), "config.json")
