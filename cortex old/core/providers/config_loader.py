import os
import importlib.util

def load_env(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath) as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, _, value = line.strip().partition("=")
                    os.environ[key] = value

def load_config_modules(config_folder="config"):
    config = {}
    for filename in os.listdir(config_folder):
        if filename.endswith(".py"):
            name = filename[:-3]
            spec = importlib.util.spec_from_file_location(name, os.path.join(config_folder, filename))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            config[name] = getattr(mod, "CONFIG", {})
    return config
