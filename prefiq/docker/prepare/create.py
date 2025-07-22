from prefiq import CPATH
from prefiq.docker.gen_docker_json import gen_docker_json
from prefiq.docker.generate_from_template import generate_from_template
from prefiq.utils.cprint import cprint_success

template_name = 'dockerfile.j2'
output_path = CPATH.DOCKER_DIR


def dockerfile(name: str):
    context = {
        "base_image": "ubuntu:24.04",
        "packages": ["python3", "python3-pip", "curl", "nano"],
        "cmd": "bash"
    }

    output_filename = f"Dockerfile_{name}"

    generate_from_template(
        template_name=template_name,
        output_filename=output_filename,
        context=context,
        output_dir=output_path
    )

    gen_docker_json("DOCKERFILE_NAME", output_filename)
    gen_docker_json("DOCKERFILE_PATH", str(output_path))

    cprint_success(f"Dockerfile written to: {output_path}")
