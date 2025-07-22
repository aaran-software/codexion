from typer.testing import CliRunner
import configparser
from pathlib import Path

from prefiq.cli.config.app.app_cli import app_cmd
from prefiq import CPATH

runner = CliRunner()


def setup_app_cfg(tmp_path: Path):
    config = configparser.ConfigParser()
    config["crm"] = {"version": "1.0.0"}
    (tmp_path / "app.cfg").write_text("")
    with open(tmp_path / "app.cfg", "w") as f:
        config.write(f)


def test_update_app_with_version(monkeypatch, tmp_path):
    monkeypatch.setattr("prefiq.config.generate.CONFIG_DIR", tmp_path)
    monkeypatch.setattr(CPATH, "CONFIG_DIR", tmp_path)
    setup_app_cfg(tmp_path)

    result = runner.invoke(app_cmd, ["update", "crm", "2.1.0"])
    assert result.exit_code == 0
    assert "app 'crm' updated to version 2.1.0" in result.output.lower()

    config = configparser.ConfigParser()
    config.read(tmp_path / "app.cfg")
    assert config["crm"]["version"] == "2.1.0"


def test_update_app_to_latest(monkeypatch, tmp_path):
    monkeypatch.setattr("prefiq.config.generate.CONFIG_DIR", tmp_path)
    monkeypatch.setattr(CPATH, "CONFIG_DIR", tmp_path)
    setup_app_cfg(tmp_path)

    result = runner.invoke(app_cmd, ["update", "crm", "--latest"])
    assert result.exit_code == 0
    assert "app 'crm' updated to version latest" in result.output.lower()

    config = configparser.ConfigParser()
    config.read(tmp_path / "app.cfg")
    assert config["crm"]["version"] == "latest"


def test_update_app_missing_args(monkeypatch, tmp_path):
    monkeypatch.setattr("prefiq.config.generate.CONFIG_DIR", tmp_path)
    monkeypatch.setattr(CPATH, "CONFIG_DIR", tmp_path)
    setup_app_cfg(tmp_path)

    result = runner.invoke(app_cmd, ["update", "crm"])
    assert result.exit_code != 0
    assert "provide a version or use --latest" in result.output.lower()

