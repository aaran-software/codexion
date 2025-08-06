# container.py

class Container:
    def __init__(self):
        self._bindings = {}
        self._singletons = {}
        self._instances = {}

    def bind(self, key, value, singleton=False):
        """
        Bind a class, function, or instance to a key.
        If singleton=True, only one instance will be created.
        """
        self._bindings[key] = value
        if singleton:
            self._singletons[key] = True

    def singleton(self, key, value):
        """Shortcut to bind as singleton."""
        self.bind(key, value, singleton=True)

    def instance(self, key, instance):
        """Bind an existing instance directly."""
        self._instances[key] = instance

    def resolve(self, key):
        """
        Resolve a dependency by key.
        Singleton instances are cached.
        """
        if key in self._instances:
            return self._instances[key]

        if key not in self._bindings:
            raise KeyError(f"No binding found for key '{key}'")

        value = self._bindings[key]

        # If value is a class, instantiate it
        if callable(value):
            instance = value()
        else:
            instance = value

        if key in self._singletons:
            self._instances[key] = instance

        return instance

    def has(self, key):
        return key in self._bindings or key in self._instances

    def clear(self):
        """Clear all bindings and instances (used in tests)."""
        self._bindings.clear()
        self._instances.clear()
        self._singletons.clear()


# Global container instance
container = Container()
