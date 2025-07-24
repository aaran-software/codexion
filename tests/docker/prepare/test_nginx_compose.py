import os
import shutil
import pytest
from prefiq.docker.prepare.nginx_compose import create_nginx_compose
from prefiq import CPATH

@pytest.fixture(autouse=True)
def isolate_docker_dir(tmp_path, monkeypatch):
    """
    Redirect CPATH.DOCKER_DIR to a temporary path for safe testing.
    """
    monkeypatch.setattr(CPATH, "DOCKER_DIR", tmp_path)
    yield tmp_path
    shutil.rmtree(tmp_path, ignore_errors=True)


def test_gen_nginx_compose(tmp_path):
    service_name = "test_service"
    service_port = 8081

    result = create_nginx_compose(service_name, service_port)

    compose_file = result["compose_path"]
    nginx_conf = result["nginx_conf_path"]
    cert_path = result["cert_path"]
    key_path = result["key_path"]

    # Check compose file
    assert os.path.exists(compose_file)
    with open(compose_file) as f:
        content = f.read()
        assert service_name in content or str(service_port) in content

    # Check nginx.conf
    assert os.path.exists(nginx_conf)
    with open(nginx_conf) as f:
        content = f.read()
        assert service_name in content or str(service_port) in content

    # Check SSL certs
    assert os.path.exists(cert_path)
    assert os.path.exists(key_path)
