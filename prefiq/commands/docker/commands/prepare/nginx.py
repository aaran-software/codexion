import os
import subprocess

from prefiq.commands.docker.commands.prepare.gen_docker_json import gen_docker_json
from prefiq.commands.docker.commands.prepare.generate_from_template import generate_from_template
from prefiq.commands.utils.ui import print_success, print_warning

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
OUTPUT_DIR = os.path.join(os.getcwd(), 'docker')
NGINX_DIR = os.path.join(OUTPUT_DIR, 'nginx')
CERTS_DIR = os.path.join(NGINX_DIR, 'certs')
os.makedirs(CERTS_DIR, exist_ok=True)


def generate_self_signed_cert():
    cert_path = os.path.join(CERTS_DIR, 'fullchain.pem')
    key_path = os.path.join(CERTS_DIR, 'privkey.pem')

    if os.path.exists(cert_path) and os.path.exists(key_path):
        print_warning("Certificates already exist, skipping generation.")
        return

    subprocess.run([
        "openssl", "req", "-x509", "-nodes", "-days", "365",
        "-newkey", "rsa:2048",
        "-keyout", key_path,
        "-out", cert_path,
        "-subj", "/CN=localhost"
    ], check=True)

    print_success("Self-signed certificates generated.")


def gen_nginx_compose(service_name: str, service_port: int):
    context = {
        "service_name": service_name,
        "service_port": service_port,
    }

    # 1. Docker Compose
    generate_from_template(
        template_name='nginx.j2',
        output_filename='docker-compose-nginx.yml',
        context=context,
        output_dir=OUTPUT_DIR
    )

    # 2. nginx.conf
    generate_from_template(
        template_name='nginx.conf.j2',
        output_filename='nginx.conf',
        context=context,
        output_dir=NGINX_DIR
    )

    # 3. SSL Certs
    generate_self_signed_cert()

    gen_docker_json("NGINX_COMPOSE", {os.path.join(OUTPUT_DIR, "docker-compose-traefik.yml")})
    gen_docker_json("NGINX_CONF", {os.path.join(OUTPUT_DIR, "nginx.conf")})

    print_success("Nginx setup complete with nginx.conf and self-signed SSL.")
