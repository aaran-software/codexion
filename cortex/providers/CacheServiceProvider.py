# providers/cache_provider.py

from cortex.services import ServiceProvider
from cortex.container import container

# Simple in-memory cache as default
class InMemoryCache:
    def __init__(self):
        self.store = {}

    def get(self, key):
        return self.store.get(key)

    def set(self, key, value):
        self.store[key] = value

    def has(self, key):
        return key in self.store

    def clear(self):
        self.store.clear()


class CacheServiceProvider(ServiceProvider):
    def register(self):
        # Could be extended to Redis, Memcached, etc. in future
        cache = InMemoryCache()
        container.instance("cache", cache)

    def boot(self):
        print("✅ Cache system initialized.")
