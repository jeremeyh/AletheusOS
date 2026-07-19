"""
AletheusOS Runtime Command Registry

Genesis 7 Compatibility Layer
"""

from __future__ import annotations

from typing import Any, Callable

from .models import CommandRecord, CommandResult


class RuntimeCommandRegistry:
    """
    Owns payload command registration and dispatch.

    During the Genesis 7 migration, duplicate registrations are treated
    as idempotent so multiple bootstrap modules may coexist.
    """

    def __init__(self) -> None:
        self.commands: dict[str, CommandRecord] = {}

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

        #
        # Genesis 7 compatibility
        #
        if normalized_name in self.commands:

            if replace:
                self.unregister(normalized_name)

            else:
                #
                # Existing registration wins.
                #
                return self.commands[normalized_name]

        record = CommandRecord(
            name=normalized_name,
            handler=handler,
            category=category,
            description=description,
            metadata=metadata or {},
        )

        self.commands[normalized_name] = record
        return record

    def unregister(self, name: str) -> bool:
        return self.commands.pop(name, None) is not None

    def has(self, name: str) -> bool:
        return name in self.commands

    def get(self, name: str):
        return self.commands.get(name)

    def dispatch(self, name: str, payload=None):

        payload = payload or {}

        record = self.commands.get(name)

        if record is None:
            return CommandResult(
                command=name,
                status="missing",
                response={
                    "error": f"Command '{name}' is not registered."
                },
            )

        try:

            response = record.handler(payload)

            return CommandResult(
                command=name,
                status="completed",
                response=(
                    response
                    if isinstance(response, dict)
                    else {"result": response}
                ),
            )

        except Exception as exc:

            return CommandResult(
                command=name,
                status="failed",
                response={
                    "error": str(exc),
                    "error_type": type(exc).__name__,
                },
            )

    def count(self):
        return len(self.commands)

    def list(self):
        return sorted(self.commands)

    def categories(self):
        return sorted(
            {
                record.category
                for record in self.commands.values()
            }
        )

    def health(self):
        return {
            "status": "online",
            "commands": self.count(),
            "categories": self.categories(),
            "command_names": self.list(),
        }


__all__ = [
    "RuntimeCommandRegistry",
]
