import os
import subprocess
from pathlib import Path

from prefiq.docker.common.generate_from_template import generate_from_template
from prefiq.utils.cprint import cprint_success, cprint_warning
from prefiq import CPATH

TEMPLATE_NAME = "nginx.j2"

def generate_self_signed_cert(certs_dir: Path):
    """
    Generates self-signed SSL certificates if they don't exist.
    """
    cert_path = certs_dir / 'fullchain.pem'
    key_path = certs_dir / 'privkey.pem'

    if cert_path.exists() and key_path.exists():
        cprint_warning("Certificates already exist, skipping generation.")
        return

    certs_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run([
        "openssl", "req", "-x509", "-nodes", "-days", "365",
        "-newkey", "rsa:2048",
        "-keyout", str(key_path),
        "-out", str(cert_path),
        "-subj", "/CN=localhost"
    ], check=True)

    cprint_success("Self-signed certificates generated.")

def create_nginx_compose(service_name: str, service_port: int, output_dir: Path = None):
    """
    Generates Docker Compose and nginx.conf for a given service behind Nginx.
    """
    if output_dir is None:
        output_dir = CPATH.DOCKER_DIR

    nginx_dir = output_dir / 'nginx'
    certs_dir = output_dir / 'certs'

    nginx_dir.mkdir(parents=True, exist_ok=True)
    certs_dir.mkdir(parents=True, exist_ok=True)

    context = {
        "service_name": service_name,
        "service_port": service_port,
    }

    # Generate docker-compose-nginx.yml
    generate_from_template(
        template_name=TEMPLATE_NAME,
        output_filename='docker-compose-nginx.yml',
        context=context,
        output_dir=str(output_dir)
    )

    # Generate nginx.conf
    generate_from_template(
        template_name='nginx.conf.j2',
        output_filename='nginx.conf',
        context=context,
        output_dir=str(nginx_dir)
    )

    # Generate SSL certificates
    generate_self_signed_cert(certs_dir)

    cprint_success("Nginx setup complete with nginx.conf and self-signed SSL.")

    return {
        "compose_path": output_dir / 'docker-compose-nginx.yml',
        "nginx_conf_path": nginx_dir / 'nginx.conf',
        "cert_path": certs_dir / 'fullchain.pem',
        "key_path": certs_dir / 'privkey.pem',
    }
