"""
AletheusOS Runtime Command Registry

Genesis 8 compiled-dispatch integration.

The public Genesis 7 registry contract remains stable while runtime
execution is delegated to an immutable compiled dispatcher.
"""

from __future__ import annotations

from typing import Any, Callable

from .dispatcher import CompiledRuntimeCommandDispatcher
from .models import CommandRecord, CommandResult


class RuntimeCommandRegistry:
    """
    Owns payload-command registration and compiled dispatch.

    Registration remains mutable for bootstrap compatibility. Every
    successful mutation recompiles an immutable dispatcher snapshot.
    Runtime command execution does not inspect or mutate the registry.
    """

    def __init__(self) -> None:
        self.commands: dict[str, CommandRecord] = {}
        self._generation = 0
        self._dispatcher = (
            CompiledRuntimeCommandDispatcher(
                self.commands,
                generation=self._generation,
            )
        )

    @property
    def dispatcher(self) -> CompiledRuntimeCommandDispatcher:
        return self._dispatcher

    @property
    def fingerprint(self) -> str:
        return self._dispatcher.fingerprint

    @property
    def generation(self) -> int:
        return self._generation

    def _compile(self) -> None:
        """
        Compile the mutable registration surface into an immutable
        runtime execution index.
        """

        self._generation += 1
        self._dispatcher = (
            CompiledRuntimeCommandDispatcher(
                self.commands,
                generation=self._generation,
            )
        )

    def register(
        self,
        name: str,
        handler: Callable[..., Any],
        category: str = "general",
        description: str = "",
        metadata: dict[str, Any] | None = None,
        *,
        replace: bool = False,
    ) -> CommandRecord:
        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("Command name cannot be empty.")

        if normalized_name in self.commands:
            if not replace:
                # Genesis 7 idempotent-registration compatibility.
                return self.commands[normalized_name]

            self.commands.pop(normalized_name)

        record = CommandRecord(
            name=normalized_name,
            handler=handler,
            category=category,
            description=description,
            metadata=metadata or {},
        )

        self.commands[normalized_name] = record
        self._compile()

        return record

    def unregister(self, name: str) -> bool:
        removed = self.commands.pop(name, None) is not None

        if removed:
            self._compile()

        return removed

    def has(self, name: str) -> bool:
        return self._dispatcher.has(name)

    def get(self, name: str) -> CommandRecord | None:
        return self._dispatcher.get(name)

    def dispatch(
        self,
        name: str,
        payload: dict[str, Any] | None = None,
        *,
        application: str = "system",
    ) -> CommandResult:
        return self._dispatcher.dispatch(
            name,
            payload,
            application=application,
        )

    def count(self) -> int:
        return len(self.commands)

    def list(self) -> list[str]:
        return sorted(self.commands)

    def categories(self) -> list[str]:
        return sorted(
            {
                record.category
                for record in self.commands.values()
            }
        )

    def health(self) -> dict[str, Any]:
        return {
            "status": "online",
            "mode": "compiled",
            "commands": self.count(),
            "categories": self.categories(),
            "command_names": self.list(),
            "generation": self.generation,
            "fingerprint": self.fingerprint,
            "dispatcher": self._dispatcher.health(),
        }


__all__ = [
    "RuntimeCommandRegistry",
]
