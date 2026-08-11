"""
CardHawk OS™
Universal Engine Base
"""

from abc import ABC, abstractmethod


class EngineBase(ABC):
    name = "Unnamed Engine"
    version = "1.0"

    # Events this engine subscribes to
    events = []

    def initialize(self):
        """Called during platform bootstrap."""
        return True

    def subscribe(self, event_bus):
        """
        Automatically subscribe this engine to every event
        declared in self.events.
        """
        for event in self.events:
            event_bus.subscribe(event, self.handle_event)

    def handle_event(self, payload):
        """
        Override in concrete engines if they react to events.
        """

    @abstractmethod
    def execute(self, payload):
        """
        Primary execution entry point.
        """
        raise NotImplementedError

    def shutdown(self):
        """Cleanup resources."""
        return True
