"""
CardHawk OS™
Projection Base
"""

from abc import ABC, abstractmethod


class Projection(ABC):
    name = "Projection"

    events = []

    @abstractmethod
    def handle(self, event_name, payload):
        pass

    def rebuild(self):
        pass
