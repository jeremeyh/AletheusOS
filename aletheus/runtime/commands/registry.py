from __future__ import annotations

from hashlib import sha256
from types import MappingProxyType
from typing import Iterable, Iterator, Mapping

from .errors import CommandNotFoundError, DuplicateCommandError
from .models import CompiledCommand


class CompiledCommandRegistry:
    """
    Immutable runtime command index.

    All aliases are resolved during construction. Runtime lookup is a direct
    mapping access with no reflection, scanning, or mutation.
    """

    __slots__ = ("_commands", "_canonical", "_fingerprint")

    def __init__(self, commands: Iterable[CompiledCommand]) -> None:
        command_map: dict[str, CompiledCommand] = {}
        canonical: dict[str, CompiledCommand] = {}

        for command in commands:
            self._bind(command_map, command.name, command)
            canonical[command.name] = command

            for alias in command.aliases:
                self._bind(command_map, alias, command)

        self._commands: Mapping[str, CompiledCommand] = MappingProxyType(command_map)
        self._canonical: Mapping[str, CompiledCommand] = MappingProxyType(canonical)
        self._fingerprint = self._build_fingerprint(canonical.values())

    @staticmethod
    def _bind(
        target: dict[str, CompiledCommand],
        key: str,
        command: CompiledCommand,
    ) -> None:
        if key in target:
            raise DuplicateCommandError(key)
        target[key] = command

    @staticmethod
    def _build_fingerprint(commands: Iterable[CompiledCommand]) -> str:
        rows = []
        for command in sorted(commands, key=lambda item: item.name):
            rows.append(
                "|".join(
                    (
                        command.name,
                        command.domain,
                        command.version,
                        f"{command.handler.__module__}.{command.handler.__qualname__}",
                        f"{command.request_type.__module__}.{command.request_type.__qualname__}",
                        f"{command.result_type.__module__}.{command.result_type.__qualname__}",
                        ",".join(command.permissions),
                        ",".join(command.aliases),
                        str(command.idempotent),
                    )
                )
            )
        return sha256("\n".join(rows).encode("utf-8")).hexdigest()

    @property
    def fingerprint(self) -> str:
        return self._fingerprint

    @property
    def command_count(self) -> int:
        return len(self._canonical)

    def require(self, command_name: str) -> CompiledCommand:
        try:
            return self._commands[command_name]
        except KeyError as exc:
            raise CommandNotFoundError(command_name) from exc

    def contains(self, command_name: str) -> bool:
        return command_name in self._commands

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._canonical))

    def as_mapping(self) -> Mapping[str, CompiledCommand]:
        return self._canonical

    def __iter__(self) -> Iterator[CompiledCommand]:
        return iter(self._canonical.values())

    def __len__(self) -> int:
        return len(self._canonical)
