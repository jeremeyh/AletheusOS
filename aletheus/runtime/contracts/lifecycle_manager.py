from __future__ import annotations

from collections.abc import Iterable

from aletheus.runtime.contracts.component import RuntimeComponent


class LifecycleManager:
    """
    Coordinates startup and shutdown of runtime components.
    """

    def __init__(self) -> None:
        self._components: tuple[RuntimeComponent, ...] = ()

    def configure(
        self,
        components: Iterable[RuntimeComponent],
    ) -> None:
        self._components = tuple(components)

    async def start_all(self) -> None:
        for component in self._components:
            await component.start()

    async def stop_all(self) -> None:
        for component in reversed(self._components):
            await component.stop()

    @property
    def components(self) -> tuple[RuntimeComponent, ...]:
        return self._components
