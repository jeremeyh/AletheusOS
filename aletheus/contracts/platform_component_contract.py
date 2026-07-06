from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class PlatformComponentContract(ABC):
    """
    AletheusOS Platform Component Contract™

    Every first-class operating system component
    should satisfy this contract.
    """

    VERSION = "0.1.0"
    GENESIS = "13.4"

    @abstractmethod
    def boot(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def health(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def statistics(self) -> dict[str, Any]:
        raise NotImplementedError

    def status(self) -> dict[str, Any]:
        return self.health()

    def snapshot(self) -> dict[str, Any]:
        return {
            "health": self.health(),
            "statistics": self.statistics(),
        }

    def verify(self) -> dict[str, Any]:
        return {
            "verified": True,
            "component": self.__class__.__name__,
        }

    def shutdown(self) -> dict[str, Any]:
        return {
            "status": "offline",
            "component": self.__class__.__name__,
        }
