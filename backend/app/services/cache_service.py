import hashlib


class CacheService:

    def __init__(self, cache):
        if cache is None:
            self.cache = {}
        self.cache = cache

    def _hash(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def get(self, query):
        if hasattr(self.cache,"get"):
            return self.cache.get(self._hash(query))
        return None

    def set(self, query, value):
        if hasattr(self.cache, "set"):
            self.cache.set(self._hash(query), value)
        else:
            self.cache[self._hash(query)] = value