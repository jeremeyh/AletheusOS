from __future__ import annotations

from aletheus.runtime.contracts.component import RuntimeComponent
from aletheus.runtime.contracts.errors import (
    ComponentAlreadyRegisteredError,
    ComponentNotFoundError,
)
from aletheus.runtime.contracts.registration import ComponentRegistry


class RegistrationManager(ComponentRegistry):
    """
    In-memory runtime component registry.

    The Constitutional Runtime Kernel interacts with this class
    instead of managing component registration directly.
    """

    def __init__(self) -> None:
        self._components: dict[str, RuntimeComponent] = {}

    async def register(self, component: RuntimeComponent) -> None:
        component_id = component.manifest.component_id

        if component_id in self._components:
            raise ComponentAlreadyRegisteredError(
                f"Component '{component_id}' is already registered."
            )

        self._components[component_id] = component

    async def unregister(self, component_id: str) -> None:
        if component_id not in self._components:
            raise ComponentNotFoundError(
                f"Component '{component_id}' is not registered."
            )

        del self._components[component_id]

    def get(self, component_id: str) -> RuntimeComponent:
        try:
            return self._components[component_id]
        except KeyError as exc:
            raise ComponentNotFoundError(
                f"Component '{component_id}' not found."
            ) from exc

    def contains(self, component_id: str) -> bool:
        return component_id in self._components

    def all(self) -> tuple[RuntimeComponent, ...]:
        return tuple(self._components.values())

    def count(self) -> int:
        return len(self._components)
