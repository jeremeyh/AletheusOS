"""
CardHawk OS™
Universal Service Base
"""

from abc import ABC


class ServiceBase(ABC):
    name = "Unnamed Service"

    version = "1.0"

    def initialize(self):
        return True

    def shutdown(self):
        return True
