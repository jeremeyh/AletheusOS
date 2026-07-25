"""
AletheusOS Compiled Runtime Command Dispatcher

Genesis 8

The dispatcher receives an immutable command-table snapshot from
RuntimeCommandRegistry. It owns payload-command lookup, invocation,
normalization, and failure isolation.

Reflection and registration never occur in the hot dispatch path.
"""

from __future__ import annotations

from collections.abc import Mapping
from hashlib import sha256
from types import MappingProxyType
from typing import Any

from .models import CommandRecord, CommandResult


class CompiledRuntimeCommandDispatcher:
    """
    Immutable payload-command execution index.

    A new dispatcher is compiled only when the registry changes.
    Normal command dispatch performs one mapping lookup.
    """

    __slots__ = (
        "_commands",
        "_fingerprint",
        "_generation",
    )

    def __init__(
        self,
        commands: Mapping[str, CommandRecord],
        *,
        generation: int = 0,
    ) -> None:
        snapshot = dict(commands)

        self._commands: Mapping[str, CommandRecord] = (
            MappingProxyType(snapshot)
        )
        self._generation = generation
        self._fingerprint = self._build_fingerprint(snapshot)

    @staticmethod
    def _handler_identity(handler: Any) -> str:
        """
        Build a deterministic implementation identity.

        Module and qualified name identify the handler symbol. Bytecode,
        constants, names, defaults, and closure values distinguish replaced
        functions that share the same symbol name, including local lambdas.
        """

        code = getattr(handler, "__code__", None)

        if code is None:
            return "|".join(
                (
                    getattr(handler, "__module__", ""),
                    getattr(handler, "__qualname__", repr(handler)),
                    type(handler).__module__,
                    type(handler).__qualname__,
                )
            )

        closure = getattr(handler, "__closure__", None) or ()

        closure_values = tuple(
            repr(cell.cell_contents)
            for cell in closure
        )

        return repr(
            (
                getattr(handler, "__module__", ""),
                getattr(handler, "__qualname__", ""),
                code.co_code,
                code.co_consts,
                code.co_names,
                code.co_varnames,
                getattr(handler, "__defaults__", None),
                getattr(handler, "__kwdefaults__", None),
                closure_values,
            )
        )

    @classmethod
    def _build_fingerprint(
        cls,
        commands: Mapping[str, CommandRecord],
    ) -> str:
        rows: list[str] = []

        for name in sorted(commands):
            record = commands[name]

            rows.append(
                "|".join(
                    (
                        name,
                        str(record.category),
                        str(record.description),
                        repr(record.metadata),
                        cls._handler_identity(record.handler),
                    )
                )
            )

        payload = "\n".join(rows).encode("utf-8")
        return sha256(payload).hexdigest()

    @property
    def fingerprint(self) -> str:
        return self._fingerprint

    @property
    def generation(self) -> int:
        return self._generation

    @property
    def count(self) -> int:
        return len(self._commands)

    def has(self, name: str) -> bool:
        return name in self._commands

    def get(self, name: str) -> CommandRecord | None:
        return self._commands.get(name)

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._commands))

    def dispatch(
        self,
        name: str,
        payload: dict[str, Any] | None = None,
    ) -> CommandResult:
        normalized_payload = payload or {}
        record = self._commands.get(name)

        if record is None:
            return CommandResult(
                command=name,
                status="missing",
                response={
                    "error": (
                        f"Command '{name}' is not registered."
                    )
                },
            )

        try:
            response = record.handler(normalized_payload)

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

    def health(self) -> dict[str, Any]:
        return {
            "status": "online",
            "mode": "compiled",
            "commands": self.count,
            "generation": self.generation,
            "fingerprint": self.fingerprint,
            "command_names": list(self.names()),
        }


__all__ = [
    "CompiledRuntimeCommandDispatcher",
]
