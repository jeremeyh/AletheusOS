from __future__ import annotations

import time
from typing import Any, Dict, Optional


class RuntimeCache:
    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        expires_at = None if ttl_seconds is None else time.time() + ttl_seconds
        self._store[key] = {"value": value, "expires_at": expires_at}

    def get(self, key: str, default: Any = None) -> Any:
        item = self._store.get(key)
        if not item:
            return default
        expires_at = item.get("expires_at")
        if expires_at is not None and time.time() > expires_at:
            self._store.pop(key, None)
            return default
        return item.get("value")

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()

    def stats(self) -> Dict[str, Any]:
        return {"keys": len(self._store), "key_names": sorted(self._store.keys())}
