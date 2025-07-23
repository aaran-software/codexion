import os

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "template")
ENV_TEMPLATE = os.path.join(TEMPLATE_DIR, "env.j2")


def gen_env(key: str, value: str):
    """
    Updates or adds a key-value pair in env.j2 template.
    """
    os.makedirs(TEMPLATE_DIR, exist_ok=True)

    if not os.path.exists(ENV_TEMPLATE):
        with open(ENV_TEMPLATE, "w") as f:
            f.write(f"{key}={value}\n")
        return

    updated = False
    lines = []

    with open(ENV_TEMPLATE, "r") as f:
        for line in f:
            if line.strip().startswith(f"{key}="):
                lines.append(f"{key}={value}\n")
                updated = True
            else:
                lines.append(line)

    if not updated:
        lines.append(f"{key}={value}\n")

    with open(ENV_TEMPLATE, "w") as f:
        f.writelines(lines)
