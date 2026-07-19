from collections import defaultdict
from threading import RLock
class EventBus:
    def __init__(self):
        self._handlers=defaultdict(list); self._history=[]; self._lock=RLock()
    def subscribe(self,event_type,handler):
        with self._lock: self._handlers[event_type].append(handler)
    def publish(self,event):
        with self._lock:
            handlers=tuple(self._handlers.get(event.event_type,()))+tuple(self._handlers.get("*",()))
            self._history.append(event)
        for handler in handlers: handler(event)
    @property
    def history(self):
        with self._lock: return tuple(self._history)
