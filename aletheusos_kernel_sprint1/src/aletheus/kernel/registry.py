from threading import RLock
class Registry:
    def __init__(self): self._items={}; self._lock=RLock()
    def register(self,key,item):
        key=key.strip()
        if not key: raise ValueError("Registry key cannot be empty.")
        with self._lock:
            if key in self._items: raise KeyError(f"Registry key already exists: {key}")
            self._items[key]=item
    def get(self,key):
        with self._lock:
            if key not in self._items: raise KeyError(f"Registry key not found: {key}")
            return self._items[key]
    def count(self):
        with self._lock: return len(self._items)
