"""
AletheusOS Compiled Runtime Command Dispatcher

Genesis 8

Handler signatures are classified once when the immutable dispatcher is
compiled. Runtime dispatch performs no reflection.
"""

from __future__ import annotations

import inspect
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from types import MappingProxyType
from typing import Any, Literal

from aletheus.runtime.context import RuntimeContext

from .models import CommandRecord, CommandResult

InvocationMode = Literal[
    "context",
    "payload",
    "no_arguments",
]


@dataclass(frozen=True, slots=True)
class CompiledCommandEntry:
    record: CommandRecord
    invocation_mode: InvocationMode


class CompiledRuntimeCommandDispatcher:
    """
    Immutable payload-command execution index.

    Handler invocation modes are resolved during compilation rather than
    during normal dispatch.
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
        compiled = {
            name: CompiledCommandEntry(
                record=record,
                invocation_mode=self._classify_handler(record.handler),
            )
            for name, record in commands.items()
        }

        self._commands: Mapping[
            str,
            CompiledCommandEntry,
        ] = MappingProxyType(compiled)

        self._generation = generation
        self._fingerprint = self._build_fingerprint(compiled)

    @staticmethod
    def _classify_handler(
        handler: Any,
    ) -> InvocationMode:
        """
        Classify a handler once at registry compilation.

        Context classification uses both the first parameter name and its
        annotation so older unannotated handlers remain compatible.
        """

        try:
            signature = inspect.signature(handler)
        except (TypeError, ValueError):
            return "payload"

        parameters = list(signature.parameters.values())

        positional = [
            parameter
            for parameter in parameters
            if parameter.kind
            in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
        ]

        if not positional:
            return "no_arguments"

        first = positional[0]
        annotation = first.annotation

        annotation_name = ""

        if annotation is not inspect.Signature.empty:
            annotation_name = getattr(
                annotation,
                "__name__",
                str(annotation),
            )

        normalized_name = first.name.lower()

        if (
            normalized_name
            in {
                "context",
                "ctx",
                "runtime_context",
                "command_context",
            }
            or "RuntimeContext" in annotation_name
        ):
            return "context"

        return "payload"

    @staticmethod
    def _handler_identity(handler: Any) -> str:
        code = getattr(handler, "__code__", None)

        if code is None:
            return "|".join(
                (
                    getattr(handler, "__module__", ""),
                    getattr(
                        handler,
                        "__qualname__",
                        repr(handler),
                    ),
                    type(handler).__module__,
                    type(handler).__qualname__,
                )
            )

        closure = getattr(handler, "__closure__", None) or ()

        closure_values = tuple(repr(cell.cell_contents) for cell in closure)

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
        commands: Mapping[str, CompiledCommandEntry],
    ) -> str:
        rows: list[str] = []

        for name in sorted(commands):
            entry = commands[name]
            record = entry.record

            rows.append(
                "|".join(
                    (
                        name,
                        str(record.category),
                        str(record.description),
                        repr(record.metadata),
                        entry.invocation_mode,
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
        entry = self._commands.get(name)

        if entry is None:
            return None

        return entry.record

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._commands))

    def invocation_mode(
        self,
        name: str,
    ) -> InvocationMode | None:
        entry = self._commands.get(name)

        if entry is None:
            return None

        return entry.invocation_mode

    @staticmethod
    def _invoke(
        entry: CompiledCommandEntry,
        *,
        name: str,
        payload: dict[str, Any],
        application: str,
    ) -> Any:
        handler = entry.record.handler

        if entry.invocation_mode == "no_arguments":
            return handler()

        if entry.invocation_mode == "context":
            context = RuntimeContext(
                command=name,
                payload=payload,
                application=application,
            )

            result = handler(context)

            # A mutating context handler may return None.
            return context if result is None else result

        return handler(payload)

    def dispatch(
        self,
        name: str,
        payload: dict[str, Any] | None = None,
        *,
        application: str = "system",
    ) -> CommandResult:
        normalized_payload = payload or {}
        entry = self._commands.get(name)

        if entry is None:
            return CommandResult(
                command=name,
                status="missing",
                response={"error": (f"Command '{name}' is not registered.")},
            )

        try:
            response = self._invoke(
                entry,
                name=name,
                payload=normalized_payload,
                application=application,
            )

            return CommandResult(
                command=name,
                status="completed",
                response=response,
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
        mode_counts = {
            "context": 0,
            "payload": 0,
            "no_arguments": 0,
        }

        for entry in self._commands.values():
            mode_counts[entry.invocation_mode] += 1

        return {
            "status": "online",
            "mode": "compiled",
            "commands": self.count,
            "generation": self.generation,
            "fingerprint": self.fingerprint,
            "command_names": list(self.names()),
            "invocation_modes": mode_counts,
        }


__all__ = [
    "CompiledCommandEntry",
    "CompiledRuntimeCommandDispatcher",
    "InvocationMode",
]
