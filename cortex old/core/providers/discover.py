import importlib
import pkgutil
import cortex.core.providers

def discover_providers(app, base_package="cortex.core.providers"):
    path = cortex.core.providers.__path__
    for _, module_name, _ in pkgutil.iter_modules(path):
        module = importlib.import_module(f"{base_package}.{module_name}")
        for attr_name in dir(module):
            obj = getattr(module, attr_name)
            if isinstance(obj, type) and hasattr(obj, "register") and hasattr(obj, "boot"):
                app.register(obj)
