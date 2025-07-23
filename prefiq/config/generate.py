import configparser
from prefiq import CPATH

CONFIG_DIR = CPATH.CONFIG_DIR


def get_app_config_path():
    return CONFIG_DIR / "app.cfg"


DEFAULT_CONFIGS = {
    "app.cfg": {
        "cxsun": {"version": "1.2.0"},
        "crm": {"version": "0.9.5"},
        "inventory": {"version": "2.0.1"},
    },
    "api.cfg": {
        "api": {"host": "localhost", "port": "8000"}
    },
    "docker.cfg": {
        "docker": {"image": "myapp:latest", "ports": "8000"}
    },
}


def ensure_config_file(filename: str, content: dict):
    file_path = CONFIG_DIR / filename
    if not file_path.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        config = configparser.ConfigParser()
        for section, values in content.items():
            config[section] = values
        with open(file_path, "w") as f:
            config.write(f)


def generate_all_configs():
    for name, default in DEFAULT_CONFIGS.items():
        ensure_config_file(name, default)


def add_app_to_config(app_name: str, version: str):
    path = get_app_config_path()
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    config = configparser.ConfigParser()
    if not path.exists():
        path.touch()

    config.read(path)
    config[app_name] = {"version": version}

    with open(path, "w") as f:
        config.write(f)


def list_apps() -> dict:
    path = get_app_config_path()
    config = configparser.ConfigParser()
    config.read(path)
    return {section: dict(config[section]) for section in config.sections()}


def update_app_version(app: str, version: str):
    path = get_app_config_path()
    config = configparser.ConfigParser()
    config.read(path)
    if app not in config:
        raise KeyError(f"App '{app}' not found in config.")
    config[app]["version"] = version
    with open(path, "w") as f:
        config.write(f)


def delete_app(app: str):
    path = get_app_config_path()
    config = configparser.ConfigParser()
    config.read(path)
    if app in config:
        config.remove_section(app)
        with open(path, "w") as f:
            config.write(f)
    else:
        raise KeyError(f"App '{app}' does not exist.")
