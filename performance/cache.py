from time import time


class ResultCache:
    _cache = {}

    @classmethod
    def set(cls, key, value, ttl_seconds=300):
        cls._cache[key] = {"value": value, "expires": time() + ttl_seconds}
        return value

    @classmethod
    def get(cls, key, default=None):
        item = cls._cache.get(key)
        if not item or time() > item["expires"]:
            cls._cache.pop(key, None)
            return default
        return item["value"]

    @classmethod
    def clear(cls):
        cls._cache.clear()
