import subprocess

def is_docker_running():
    try:
        subprocess.check_output(["docker", "info"])
        return True
    except Exception:
        return False

def get_docker_version():
    try:
        out = subprocess.check_output(["docker", "--version"]).decode().strip()
        return out
    except Exception:
        return None

def get_running_containers():
    try:
        out = subprocess.check_output(["docker", "ps", "--format", "{{.Names}}"]).decode().splitlines()
        return out
    except Exception:
        return []
