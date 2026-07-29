from __future__ import annotations

from typing import Protocol

from .component import RuntimeComponent


class ComponentRegistry(Protocol):
    """
    Canonical contract for runtime component registries.
    """

    async def register(self, component: RuntimeComponent) -> None:
        """Register a runtime component."""
        ...

    async def unregister(self, component_id: str) -> None:
        """Remove a registered component."""
        ...

    def get(self, component_id: str) -> RuntimeComponent:
        """Return a registered component."""
        ...

    def contains(self, component_id: str) -> bool:
        """Determine whether a component is registered."""
        ...

    def all(self) -> tuple[RuntimeComponent, ...]:
        """Return all registered components."""
        ...


