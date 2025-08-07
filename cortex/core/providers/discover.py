import importlib
import pkgutil


def discover_providers(app, base_package="cortex.services"):
    providers = []
    for _, module_name, _ in pkgutil.iter_modules([base_package.replace(".", "/")]):
        module = importlib.import_module(f"{base_package}.{module_name}")
        for attr in dir(module):
            obj = getattr(module, attr)
            if isinstance(obj, type) and hasattr(obj, "register") and hasattr(obj, "boot"):
                app.register(obj)
                providers.append(obj)
    return providers
