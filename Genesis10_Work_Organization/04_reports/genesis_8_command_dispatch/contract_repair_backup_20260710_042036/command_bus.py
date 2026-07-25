"""
AletheusOS Runtime Command Bus

Genesis 7 compatibility and composition façade.

CommandBus preserves the stable runtime command interface while delegating:

- registration and low-level routing to RuntimeCommandRegistry
- built-in runtime command implementations to RuntimeCommands
- lifecycle/bootstrap ownership to CommandManager
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from aletheus.runtime.commands_v2.registry import (
    RuntimeCommandRegistry,
)
from aletheus.runtime.context import RuntimeContext

from .runtime_commands import RuntimeCommands


class CommandBus:
    """
    Stable public runtime command surface.

    CommandBus is intentionally a thin façade. It coordinates command
    families without absorbing their implementation responsibilities.
    """

    def __init__(
        self,
        runtime: Any,
        registry: RuntimeCommandRegistry | None = None,
    ) -> None:
        self.runtime = runtime
        self.registry = registry or RuntimeCommandRegistry()
        self.runtime_commands = RuntimeCommands(runtime)

        self._context_handlers: dict[
            str,
            Callable[[RuntimeContext], RuntimeContext],
        ] = {}

        self._register_builtin_runtime_commands()

    # ---------------------------------------------------------
    # Built-in contextual command registration
    # ---------------------------------------------------------

    def _register_builtin_runtime_commands(self) -> None:
        builtins = {
            "runtime.health": self.runtime_commands.health,
            "runtime.diagnostics": self.runtime_commands.diagnostics,
            "runtime.metrics": self.runtime_commands.metrics,
            "runtime.events": self.runtime_commands.events,
            "runtime.queue": self.runtime_commands.queue,
            "runtime.run_next_job": (
                self.runtime_commands.run_next_job
            ),
        }

        for name, handler in builtins.items():
            self.register_context_handler(
                name,
                handler,
                replace=True,
            )

    def register_context_handler(
        self,
        name: str,
        handler: Callable[
            [RuntimeContext],
            RuntimeContext,
        ],
        *,
        replace: bool = False,
    ) -> Callable[[RuntimeContext], RuntimeContext]:
        """
        Register a handler that receives a RuntimeContext.
        """

        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("Command name cannot be empty.")

        if (
            normalized_name in self._context_handlers
            and not replace
        ):
            raise ValueError(
                f"Context command already registered: "
                f"{normalized_name}"
            )

        self._context_handlers[normalized_name] = handler
        return handler

    # ---------------------------------------------------------
    # Payload-handler registration
    # ---------------------------------------------------------

    def register(
        self,
        name: str,
        handler: Callable[..., Any],
        category: str = "general",
        description: str = "",
        metadata: dict[str, Any] | None = None,
        *,
        replace: bool = False,
    ):
        """
        Register a payload-based command with the registry.
        """

        return self.registry.register(
            name=name,
            handler=handler,
            category=category,
            description=description,
            metadata=metadata,
            replace=replace,
        )

    def unregister(self, name: str) -> bool:
        """
        Unregister a command from either command surface.
        """

        removed_context = (
            self._context_handlers.pop(name, None) is not None
        )
        removed_registry = self.registry.unregister(name)

        return removed_context or removed_registry

    # ---------------------------------------------------------
    # Dispatch
    # ---------------------------------------------------------

    def dispatch(
        self,
        command: str,
        payload: dict[str, Any] | None = None,
        application: str = "system",
    ) -> RuntimeContext:
        """
        Dispatch a command and always return RuntimeContext.

        Context-aware runtime handlers are executed directly. Registered
        payload handlers are dispatched through RuntimeCommandRegistry and
        adapted into the common RuntimeContext contract.
        """

        normalized_payload = payload or {}

        context = RuntimeContext(
            command=command,
            application=application,
        )

        if hasattr(context, "add_trace"):
            context.add_trace(
                "command.dispatch.start",
                command,
            )

        context_handler = self._context_handlers.get(command)

        if context_handler is not None:
            try:
                result = context_handler(context)

                if hasattr(result, "add_trace"):
                    result.add_trace(
                        "command.dispatch.finish",
                        command,
                    )

                return result

            except Exception as exc:
                context.add_error(
                    f"{type(exc).__name__}: {exc}"
                )

                if hasattr(context, "add_trace"):
                    context.add_trace(
                        "command.dispatch.failed",
                        command,
                    )

                return context

        result = self.registry.dispatch(
            command,
            normalized_payload,
        )

        status = getattr(result, "status", "unknown")
        response = getattr(result, "response", None)

        if status == "completed":
            context.add_result(
                command,
                response,
            )

        elif status == "missing":
            error = self._extract_error(
                response,
                fallback=(
                    f"Command is not registered: {command}"
                ),
            )
            context.add_error(error)

        else:
            error = self._extract_error(
                response,
                fallback=(
                    f"Command failed: {command}"
                ),
            )
            context.add_error(error)

        if hasattr(context, "add_trace"):
            context.add_trace(
                "command.dispatch.finish",
                {
                    "command": command,
                    "status": status,
                },
            )

        return context

    def execute(
        self,
        command: str,
        payload: dict[str, Any] | None = None,
        application: str = "system",
    ) -> RuntimeContext:
        """
        Compatibility alias for dispatch.
        """

        return self.dispatch(
            command,
            payload,
            application=application,
        )

    @staticmethod
    def _extract_error(
        response: Any,
        *,
        fallback: str,
    ) -> str:
        if isinstance(response, dict):
            error = response.get("error")

            if error:
                return str(error)

        if response:
            return str(response)

        return fallback

    # ---------------------------------------------------------
    # Discovery
    # ---------------------------------------------------------

    def has(self, command: str) -> bool:
        return (
            command in self._context_handlers
            or self.registry.has(command)
        )

    def count(self) -> int:
        return len(
            set(self._context_handlers)
            | set(self.registry.commands)
        )

    def list(self) -> list[str]:
        return sorted(
            set(self._context_handlers)
            | set(self.registry.commands)
        )

    def categories(self) -> list[str]:
        categories = set(self.registry.categories())

        if self._context_handlers:
            categories.add("runtime")

        return sorted(categories)

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(self) -> dict[str, Any]:
        return {
            "status": "online",
            "commands": self.count(),
            "context_commands": len(
                self._context_handlers
            ),
            "registry_commands": self.registry.count(),
            "categories": self.categories(),
            "command_names": self.list(),
            "registry": self.registry.health(),
        }


__all__ = [
    "CommandBus",
]
