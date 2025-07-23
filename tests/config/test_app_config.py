import configparser
from pathlib import Path
from prefiq.config import generate
from prefiq import CPATH

REQUIRED_FILES = {
    "app.cfg",
    "api.cfg",
    "docker.cfg",
}

def read_cfg_file(path: Path) -> dict:
    config = configparser.ConfigParser()
    config.read(path)
    return {section: dict(config[section]) for section in config.sections()}


def test_generate_app_cfg(tmp_path, monkeypatch):
    monkeypatch.setattr(generate, "CONFIG_DIR", tmp_path)

    app_cfg = tmp_path / "app.cfg"
    assert not app_cfg.exists()

    generate.ensure_config_file("app.cfg", generate.DEFAULT_CONFIGS["app.cfg"])
    assert app_cfg.exists()

    data = read_cfg_file(app_cfg)
    expected = {
        section: {k: str(v) for k, v in values.items()}
        for section, values in generate.DEFAULT_CONFIGS["app.cfg"].items()
    }
    assert data == expected


def test_generate_all_configs(tmp_path, monkeypatch):
    monkeypatch.setattr(generate, "CONFIG_DIR", tmp_path)

    generate.generate_all_configs()

    for name, default in generate.DEFAULT_CONFIGS.items():
        cfg_path = tmp_path / name
        assert cfg_path.exists()
        data = read_cfg_file(cfg_path)
        expected = {
            section: {k: str(v) for k, v in values.items()}
            for section, values in default.items()
        }
        assert data == expected


def test_required_config_files_exist(tmp_path, monkeypatch):
    monkeypatch.setattr(generate, "CONFIG_DIR", tmp_path)
    generate.generate_all_configs()

    for file in REQUIRED_FILES:
        full_path = tmp_path / file
        assert full_path.exists(), f"Missing config: {file}"


def test_all_configs_are_valid_ini(tmp_path, monkeypatch):
    monkeypatch.setattr(generate, "CONFIG_DIR", tmp_path)
    generate.generate_all_configs()

    for file in REQUIRED_FILES:
        full_path = tmp_path / file
        try:
            config = configparser.ConfigParser()
            config.read(full_path)
            assert config.sections(), f"{file} has no sections or is not valid INI"
        except Exception as e:
            raise AssertionError(f"{file} is not valid INI: {e}")


def test_add_new_app_to_config(tmp_path, monkeypatch):
    monkeypatch.setattr(generate, "CONFIG_DIR", tmp_path)

    app_cfg = tmp_path / "app.cfg"
    assert not app_cfg.exists()

    generate.ensure_config_file("app.cfg", generate.DEFAULT_CONFIGS["app.cfg"])
    generate.add_app_to_config("billing", "1.0.0")

    config = configparser.ConfigParser()
    config.read(app_cfg)

    assert "billing" in config
    assert config["billing"]["version"] == "1.0.0"
