import os
import subprocess

from prefiq.docker.prepare.generate_from_template import generate_from_template
from prefiq.utils.cprint import cprint_success, cprint_warning
from prefiq import CPATH

TEMPLATE_NAME = "nginx.j2"
OUTPUT_PATH = CPATH.DOCKER_DIR

NGINX_DIR = os.path.join(OUTPUT_PATH, 'nginx')
CERTS_DIR = os.path.join(OUTPUT_PATH, 'certs')

os.makedirs(NGINX_DIR, exist_ok=True)
os.makedirs(CERTS_DIR, exist_ok=True)

def generate_self_signed_cert():
    """
    Generates self-signed SSL certificates if they don't exist.
    """
    cert_path = os.path.join(CERTS_DIR, 'fullchain.pem')
    key_path = os.path.join(CERTS_DIR, 'privkey.pem')

    if os.path.exists(cert_path) and os.path.exists(key_path):
        cprint_warning("Certificates already exist, skipping generation.")
        return

    subprocess.run([
        "openssl", "req", "-x509", "-nodes", "-days", "365",
        "-newkey", "rsa:2048",
        "-keyout", key_path,
        "-out", cert_path,
        "-subj", "/CN=localhost"
    ], check=True)

    cprint_success("Self-signed certificates generated.")


def create_nginx_compose(service_name: str, service_port: int):
    """
    Generates Docker Compose and nginx.conf for a given service behind Nginx.
    """
    context = {
        "service_name": service_name,
        "service_port": service_port,
    }

    # Generate docker-compose-nginx.yml
    generate_from_template(
        template_name=TEMPLATE_NAME,
        output_filename='docker-compose-nginx.yml',
        context=context,
        output_dir=OUTPUT_PATH
    )

    # Generate nginx.conf
    generate_from_template(
        template_name='nginx.conf.j2',
        output_filename='nginx.conf',
        context=context,
        output_dir=NGINX_DIR
    )

    # Generate SSL certificates
    generate_self_signed_cert()

    cprint_success("Nginx setup complete with nginx.conf and self-signed SSL.")

    return {
        "compose_path": os.path.join(OUTPUT_PATH, 'docker-compose-nginx.yml'),
        "nginx_conf_path": os.path.join(NGINX_DIR, 'nginx.conf'),
        "cert_path": os.path.join(CERTS_DIR, 'fullchain.pem'),
        "key_path": os.path.join(CERTS_DIR, 'privkey.pem'),
    }
