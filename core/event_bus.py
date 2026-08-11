"""
CardHawk OS™
Universal Event Bus
"""

from collections import defaultdict


class EventBus:
    def __init__(self):

        self._listeners = defaultdict(list)

    def subscribe(self, event_name, callback):

        self._listeners[event_name].append(callback)

    def publish(self, event_name, payload=None):

        payload = payload or {}

        for listener in self._listeners[event_name]:
            listener(payload)

    def listeners(self):

        return {k: len(v) for k, v in self._listeners.items()}


event_bus = EventBus()
