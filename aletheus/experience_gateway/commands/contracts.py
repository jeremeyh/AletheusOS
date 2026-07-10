from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from threading import RLock
from typing import Any, Literal


CommandRisk = Literal[
    "read_only",
    "low",
    "moderate",
    "high",
]

CommandState = Literal[
    "previewed",
    "authorized",
    "executed",
    "rejected",
    "failed",
    "reversed",
]

CommandHandler = Callable[
    [dict[str, Any]],
    dict[str, Any],
]

CommandReversalHandler = Callable[
    [dict[str, Any]],
    dict[str, Any],
]


@dataclass(frozen=True, slots=True)
class CommandRequest:
    command_id: str
    arguments: dict[str, Any] = field(
        default_factory=dict
    )
    requested_by: str = "local-user"
    idempotency_key: str | None = None


@dataclass(frozen=True, slots=True)
class CommandDefinition:
    id: str
    name: str
    description: str
    risk: CommandRisk
    handler: CommandHandler
    reversible: bool = False
    reversal_handler: CommandReversalHandler | None = None
    required_arguments: tuple[str, ...] = ()
    effects: tuple[str, ...] = ()
    authorization_required: bool = True
    required_entitlements: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError(
                "Command id cannot be empty."
            )

        if not self.name.strip():
            raise ValueError(
                "Command name cannot be empty."
            )

        if (
            self.reversible
            and self.reversal_handler is None
        ):
            raise ValueError(
                "Reversible commands require a "
                "reversal handler."
            )


@dataclass(frozen=True, slots=True)
class CommandPreview:
    preview_id: str
    command_id: str
    name: str
    description: str
    risk: CommandRisk
    arguments: dict[str, Any]
    effects: tuple[str, ...]
    required_entitlements: tuple[str, ...]
    reversible: bool
    authorization_required: bool
    requested_by: str
    created_at: str
    expires_at: str
    state: CommandState = "previewed"


@dataclass(frozen=True, slots=True)
class CommandAuthorization:
    authorization_id: str
    preview_id: str
    authorized_by: str
    authorized_at: str
    expires_at: str
    state: CommandState = "authorized"


@dataclass(frozen=True, slots=True)
class CommandExecution:
    execution_id: str
    preview_id: str
    authorization_id: str | None
    command_id: str
    state: CommandState
    result: dict[str, Any]
    requested_by: str
    executed_at: str
    reversible: bool
    reversal_token: str | None = None
    failure: str | None = None


class CommandRegistry:
    def __init__(self) -> None:
        self._definitions: dict[
            str,
            CommandDefinition,
        ] = {}

        self._lock = RLock()

    def register(
        self,
        definition: CommandDefinition,
        *,
        replace: bool = False,
    ) -> None:
        with self._lock:
            if (
                definition.id in self._definitions
                and not replace
            ):
                raise ValueError(
                    "Command already registered: "
                    f"{definition.id}"
                )

            self._definitions[
                definition.id
            ] = definition

    def get(
        self,
        command_id: str,
    ) -> CommandDefinition:
        with self._lock:
            try:
                return self._definitions[
                    command_id
                ]
            except KeyError as error:
                raise KeyError(
                    "Unknown command: "
                    f"{command_id}"
                ) from error

    def list_definitions(
        self,
    ) -> tuple[CommandDefinition, ...]:
        with self._lock:
            return tuple(
                self._definitions.values()
            )
