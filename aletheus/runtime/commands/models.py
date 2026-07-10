from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .contracts import CommandHandler, CommandMiddleware


@dataclass(frozen=True, slots=True)
class CompiledCommand:
    name: str
    domain: str
    version: str
    handler: CommandHandler[Any, Any]
    request_type: type
    result_type: type
    permissions: tuple[str, ...] = ()
    middleware: tuple[CommandMiddleware, ...] = ()
    idempotent: bool = False
    aliases: tuple[str, ...] = ()
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.name or "." not in self.name:
            raise ValueError(
                "Command names must be non-empty and domain-qualified, "
                "for example 'workflow.execute'."
            )
        if not self.domain:
            raise ValueError("Command domain cannot be empty.")
        if not self.version:
            raise ValueError("Command version cannot be empty.")
        if not callable(self.handler):
            raise TypeError("Command handler must be callable.")
        if not isinstance(self.request_type, type):
            raise TypeError("request_type must be a type.")
        if not isinstance(self.result_type, type):
            raise TypeError("result_type must be a type.")
