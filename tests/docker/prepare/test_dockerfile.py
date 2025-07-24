import subprocess
import pytest
from pathlib import Path

from prefiq import CPATH
from prefiq.docker.prepare import dockerfile_named


@pytest.fixture(autouse=True)
def cleanup_dockerfiles():
    # Clean Docker output dir before and after each test
    for f in Path(CPATH.DOCKER_DIR).glob("Dockerfile_test_*"):
        f.unlink()
    yield
    for f in Path(CPATH.DOCKER_DIR).glob("Dockerfile_test_*"):
        f.unlink()


def test_create_docker():
    name = "test_app"
    dockerfile_named.create_docker(name)
    expected = CPATH.DOCKER_DIR / f"Dockerfile_{name}"
    assert expected.exists()
    content = expected.read_text()
    assert "ubuntu:24.04" in content
    assert "python3" in content


def test_update_docker():
    name = "test_update"
    file = CPATH.DOCKER_DIR / f"Dockerfile_{name}"
    file.write_text("dummy content")
    assert file.exists()

    dockerfile_named.update_docker(name)
    assert file.exists()
    assert "ubuntu:24.04" in file.read_text()


def test_remove_docker():
    name = "test_remove"
    file = CPATH.DOCKER_DIR / f"Dockerfile_{name}"
    file.write_text("to be removed")

    assert file.exists()
    dockerfile_named.remove_docker(name)
    assert not file.exists()


def test_remove_nonexistent_docker(capfd):
    name = "test_nonexistent"
    file = CPATH.DOCKER_DIR / f"Dockerfile_{name}"
    if file.exists():
        file.unlink()

    dockerfile_named.remove_docker(name)
    out = capfd.readouterr().out
    assert "not found" in out.lower()


def test_list_dockers(capfd):
    names = ["test_list1", "test_list2"]
    for n in names:
        (CPATH.DOCKER_DIR / f"Dockerfile_{n}").write_text("# Dummy")

    dockerfile_named.list_dockers()
    out = capfd.readouterr().out
    for n in names:
        assert f"Dockerfile_{n}" in out