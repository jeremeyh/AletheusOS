"""
Runtime Anchor Circuit Base

Genesis 8.3

Capability attachment contract.
"""

from abc import ABC, abstractmethod


class RuntimeAnchorCircuit(ABC):
    version = "1.0.0"

    def __init__(self, runtime):

        self.runtime = runtime
        self.connected = False

    @property
    def name(self):

        return self.__class__.__name__

    @abstractmethod
    def attach(self):

        pass

    def detach(self):

        self.connected = False

        return self.status()

    def health(self):

        return {"healthy": self.connected, "connected": self.connected}

    def capabilities(self):

        return []

    def contract(self):

        return {
            "name": self.name,
            "version": self.version,
            "capabilities": self.capabilities(),
            "lifecycle": ["attach", "detach", "health"],
        }

    def validate_contract(self):

        required = ["attach", "detach", "health", "capabilities"]

        missing = [item for item in required if not hasattr(self, item)]

        return {"valid": len(missing) == 0, "missing": missing}

    def status(self):

        return {
            "name": self.name,
            "version": self.version,
            "connected": self.connected,
            "contract": self.validate_contract(),
        }
