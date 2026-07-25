from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


@dataclass(slots=True)
class RuntimeDispatchRequest:
    """
    Executive-layer dispatch request.

    The Executive Kernel should submit requests through this stable
    contract rather than reaching directly into runtime/core.py.
    """

    command: str
    payload: dict[str, Any] = field(default_factory=dict)
    requester: str = "executive_kernel"
    intent_id: str | None = None


@dataclass(slots=True)
class RuntimeDispatchResult:
    """
    Stable dispatch result returned by a Runtime Adapter.
    """

    command: str
    success: bool
    result: Any = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class RuntimeAdapterProtocol(Protocol):
    """
    Constitutional boundary between the Executive Kernel and Runtime Kernel.

    Implementations may wrap today's runtime/core.py, a future distributed
    runtime, or a test runtime.
    """

    def name(self) -> str:
        ...

    def version(self) -> str:
        ...

    def status(self) -> dict:
        ...

    def health(self) -> dict:
        ...

    def boot_summary(self) -> dict:
        ...

    def list_services(self) -> list[Any]:
        ...

    def list_managers(self) -> list[Any]:
        ...

    def list_engines(self) -> list[Any]:
        ...

    def list_capabilities(self) -> list[Any]:
        ...

    def dispatch(
        self,
        request: RuntimeDispatchRequest,
    ) -> RuntimeDispatchResult:
        ...


class DefaultRuntimeAdapter:
    """
    Default Runtime Adapter for the current Aletheus runtime.

    This adapter exposes a curated, stable interface for the Executive
    Kernel. It intentionally avoids exposing runtime internals directly.
    """

    def __init__(
        self,
        runtime: Any,
    ) -> None:
        self.runtime = runtime

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    def name(self) -> str:
        return getattr(
            self.runtime,
            "name",
            "Aletheus Runtime Kernel",
        )

    def version(self) -> str:
        return str(
            getattr(
                self.runtime,
                "version",
                "unknown",
            )
        )

    # ---------------------------------------------------------
    # Status / Health
    # ---------------------------------------------------------

    def status(self) -> dict:
        if hasattr(self.runtime, "status"):
            status = self.runtime.status

            if callable(status):
                return status()

            return {
                "status": status,
            }

        return {
            "status": "unknown",
            "runtime": self.name(),
        }

    def health(self) -> dict:
        if hasattr(self.runtime, "health_report"):
            return self.runtime.health_report()

        if hasattr(self.runtime, "health"):
            health = self.runtime.health

            if callable(health):
                return health()

            return {
                "health": health,
            }

        return {
            "status": "unknown",
            "message": "Runtime health interface not available.",
        }

    def boot_summary(self) -> dict:
        if hasattr(self.runtime, "boot_summary"):
            summary = self.runtime.boot_summary

            if callable(summary):
                return summary()

        return {
            "runtime": self.name(),
            "version": self.version(),
            "status": self.status(),
        }

    # ---------------------------------------------------------
    # Discovery
    # ---------------------------------------------------------

    def list_services(self) -> list[Any]:
        if hasattr(self.runtime, "services"):
            services = self.runtime.services

            if hasattr(services, "all"):
                return list(services.all())

            if isinstance(services, list):
                return services

        if hasattr(self.runtime, "list_services"):
            return list(self.runtime.list_services())

        return []

    def list_managers(self) -> list[Any]:
        if hasattr(self.runtime, "managers"):
            managers = self.runtime.managers

            if isinstance(managers, dict):
                return list(managers.values())

            if isinstance(managers, list):
                return managers

        if hasattr(self.runtime, "list_managers"):
            return list(self.runtime.list_managers())

        return []

    def list_engines(self) -> list[Any]:
        if hasattr(self.runtime, "engines"):
            engines = self.runtime.engines

            if isinstance(engines, dict):
                return list(engines.values())

            if isinstance(engines, list):
                return engines

        if hasattr(self.runtime, "list_engines"):
            return list(self.runtime.list_engines())

        return []

    def list_capabilities(self) -> list[Any]:
        if hasattr(self.runtime, "capabilities"):
            capabilities = self.runtime.capabilities

            if isinstance(capabilities, dict):
                return list(capabilities.values())

            if isinstance(capabilities, list):
                return capabilities

        if hasattr(self.runtime, "list_capabilities"):
            return list(self.runtime.list_capabilities())

        return []

    # ---------------------------------------------------------
    # Dispatch
    # ---------------------------------------------------------

    def dispatch(
        self,
        request: RuntimeDispatchRequest,
    ) -> RuntimeDispatchResult:
        """
        Dispatch a command through the runtime without exposing the
        Executive Kernel to runtime internals.
        """

        try:
            if hasattr(self.runtime, "commands"):
                commands = self.runtime.commands

                if hasattr(commands, "execute"):
                    result = commands.execute(
                        request.command,
                        request.payload,
                    )
                    return RuntimeDispatchResult(
                        command=request.command,
                        success=True,
                        result=result,
                        metadata={
                            "path": "commands.execute",
                        },
                    )

                if hasattr(commands, "dispatch"):
                    result = commands.dispatch(
                        request.command,
                        request.payload,
                    )
                    return RuntimeDispatchResult(
                        command=request.command,
                        success=True,
                        result=result,
                        metadata={
                            "path": "commands.dispatch",
                        },
                    )

            for method_name in (
                "execute",
                "dispatch",
                "run",
            ):
                if hasattr(self.runtime, method_name):
                    method = getattr(self.runtime, method_name)
                    result = method(
                        request.command,
                        request.payload,
                    )
                    return RuntimeDispatchResult(
                        command=request.command,
                        success=True,
                        result=result,
                        metadata={
                            "path": method_name,
                        },
                    )

            return RuntimeDispatchResult(
                command=request.command,
                success=False,
                error="Runtime does not expose a supported dispatch interface.",
            )

        except Exception as exc:
            return RuntimeDispatchResult(
                command=request.command,
                success=False,
                error=str(exc),
            )
