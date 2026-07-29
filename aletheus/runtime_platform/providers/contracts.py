from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RuntimeProvider(ABC):
    """
    Canonical provider contract.

    Every runtime capability, subsystem, adapter,
    connector and future plugin should implement this.
    """

    VERSION = "1.0.0"

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    def version(self) -> str:
        return self.VERSION

    @property
    def dependencies(self) -> tuple[str, ...]:
        return ()

    @property
    def capabilities(self) -> tuple[str, ...]:
        return ()

    @abstractmethod
    def initialize(self, runtime: Any) -> None:
        ...

    @abstractmethod
    def activate(self) -> None:
        ...

    @abstractmethod
    def health(self) -> dict[str, Any]:
        ...

    @abstractmethod
    def snapshot(self) -> dict[str, Any]:
        ...

    @abstractmethod
    def shutdown(self) -> None:
        ...
