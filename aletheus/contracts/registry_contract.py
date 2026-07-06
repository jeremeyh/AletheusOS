from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RegistryContract(ABC):
    """
    AletheusOS Registry Contract™

    Common interface for all platform registries.
    """

    VERSION = "0.1.0"
    GENESIS = "13.3"

    @abstractmethod
    def register(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    def unregister(self, key: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Any]:
        raise NotImplementedError

    def exists(self, key: str) -> bool:
        return self.get(key) is not None

    @abstractmethod
    def health(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def statistics(self) -> dict[str, Any]:
        raise NotImplementedError

    def snapshot(self) -> dict[str, Any]:
        return {
            "health": self.health(),
            "statistics": self.statistics(),
        }
