from datetime import datetime, timedelta


class RuntimeCache:
    """
    CardHawkOS Runtime Cache™

    Lightweight in-memory cache for expensive runtime snapshots.
    """

    _cache = {}

    @classmethod
    def set(cls, key, value, ttl_seconds=300):
        cls._cache[key] = {
            "value": value,
            "expires_at": datetime.utcnow() + timedelta(seconds=ttl_seconds),
            "created_at": datetime.utcnow(),
        }

    @classmethod
    def get(cls, key):
        item = cls._cache.get(key)

        if not item:
            return None

        if datetime.utcnow() > item["expires_at"]:
            cls._cache.pop(key, None)
            return None

        return item["value"]

    @classmethod
    def remember(cls, key, callback, ttl_seconds=300):
        cached = cls.get(key)

        if cached is not None:
            return cached

        value = callback()

        cls.set(
            key,
            value,
            ttl_seconds=ttl_seconds,
        )

        return value

    @classmethod
    def clear(cls):
        cls._cache.clear()

    @classmethod
    def status(cls):
        return {
            "items": len(cls._cache),
            "keys": list(cls._cache.keys()),
        }
