from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping

from .health import HealthReport
from .manifest import ComponentManifest


class RuntimeComponent(ABC):
    """
    Canonical contract for all runtime-managed components.

    Every component managed by the Constitutional Runtime Kernel
    must implement this interface.
    """

    @property
    @abstractmethod
    def manifest(self) -> ComponentManifest:
        """Return the immutable manifest describing this component."""
        raise NotImplementedError

    @abstractmethod
    async def start(self) -> None:
        """Acquire resources and transition into the running state."""
        raise NotImplementedError

    @abstractmethod
    async def stop(self) -> None:
        """Release resources and stop the component."""
        raise NotImplementedError

    @abstractmethod
    async def health(self) -> HealthReport:
        """Return the current health report."""
        raise NotImplementedError

    def diagnostics(self) -> Mapping[str, Any]:
        """
        Return optional diagnostic information.

        Components may override this to expose
        runtime-specific debugging details.
        """
        return {}
