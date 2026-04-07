import hashlib


class CacheService:

    def __init__(self, cache):
        if cache is None:
            self.cache = {}
        else:
            self.cache = cache

    def _hash(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def get(self, query):
        key = self._hash(query)
        if hasattr(self.cache,"get"):
            return self.cache.get(self._hash(key))
        return None

    def set(self, query, value):
        key = self._hash(query)
        if hasattr(self.cache, "set"):
            self.cache.set(key, value)
        else:
            self.cache[key] = value