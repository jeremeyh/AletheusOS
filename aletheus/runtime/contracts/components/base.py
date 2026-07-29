from __future__ import annotations

import asyncio
from abc import abstractmethod

from aletheus.runtime.contracts.component import RuntimeComponent
from aletheus.runtime.contracts.health import (
    HealthReport,
    HealthStatus,
)
from aletheus.runtime.contracts.lifecycle import LifecycleState
from aletheus.runtime.contracts.manifest import ComponentManifest


class BaseRuntimeComponent(RuntimeComponent):
    """
    Shared lifecycle implementation for runtime-managed components.

    Concrete components inherit from this class and only implement
    component-specific startup and shutdown logic.
    """

    def __init__(self, manifest: ComponentManifest) -> None:
        self._manifest = manifest
        self._state = LifecycleState.CREATED
        self._lock = asyncio.Lock()
        self._last_error: Exception | None = None

    @property
    def manifest(self) -> ComponentManifest:
        return self._manifest

    @property
    def state(self) -> LifecycleState:
        return self._state

    async def start(self) -> None:
        async with self._lock:
            if self._state is LifecycleState.RUNNING:
                return

            self._state = LifecycleState.STARTING

            try:
                await self._on_start()
            except Exception as exc:
                self._last_error = exc
                self._state = LifecycleState.FAILED
                raise

            self._state = LifecycleState.RUNNING

    async def stop(self) -> None:
        async with self._lock:
            if self._state is LifecycleState.STOPPED:
                return

            self._state = LifecycleState.STOPPING

            try:
                await self._on_stop()
            except Exception as exc:
                self._last_error = exc
                self._state = LifecycleState.FAILED
                raise

            self._state = LifecycleState.STOPPED

    async def health(self) -> HealthReport:
        if self._state is LifecycleState.RUNNING:
            return HealthReport(
                component_id=self.manifest.component_id,
                status=HealthStatus.HEALTHY,
                summary="Component is running.",
                details={"state": self._state.value},
            )

        if self._state is LifecycleState.FAILED:
            return HealthReport(
                component_id=self.manifest.component_id,
                status=HealthStatus.UNHEALTHY,
                summary="Component failed.",
                details={
                    "state": self._state.value,
                    "error": repr(self._last_error),
                },
            )

        return HealthReport(
            component_id=self.manifest.component_id,
            status=HealthStatus.UNKNOWN,
            summary="Component is not running.",
            details={"state": self._state.value},
        )

    @abstractmethod
    async def _on_start(self) -> None:
        """Component-specific startup."""

    @abstractmethod
    async def _on_stop(self) -> None:
        """Component-specific shutdown."""
