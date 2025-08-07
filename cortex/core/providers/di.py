import inspect


class Container:
    def __init__(self):
        self._bindings = {}
        self._singletons = {}

    def bind(self, key, value):
        self._bindings[key] = value

    def singleton(self, key, factory):
        self._bindings[key] = factory
        self._singletons[key] = None

    def make(self, key):
        if key in self._singletons and self._singletons[key] is not None:
            return self._singletons[key]
        if key not in self._bindings:
            raise KeyError(f"Service '{key}' not bound")
        value = self._bindings[key]
        if callable(value):
            instance = value()
        else:
            instance = value
        if key in self._singletons:
            self._singletons[key] = instance
        return instance

    def resolve(self, func):
        sig = inspect.signature(func)
        kwargs = {k: self.make(k) for k in sig.parameters}
        return func(**kwargs)
