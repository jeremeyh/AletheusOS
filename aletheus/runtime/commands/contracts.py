from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable, Mapping, Protocol, TypeVar, runtime_checkable
from uuid import uuid4


@runtime_checkable
class CommandRequest(Protocol):
    """Marker protocol for command request objects."""


@runtime_checkable
class CommandResult(Protocol):
    """Marker protocol for command result objects."""


@dataclass(frozen=True, slots=True)
class CommandContext:
    correlation_id: str = field(default_factory=lambda: str(uuid4()))
    actor_id: str | None = None
    tenant_id: str | None = None
    trace_id: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


RequestT = TypeVar("RequestT")
ResultT = TypeVar("ResultT")

CommandHandler = Callable[
    [CommandContext, RequestT],
    Awaitable[ResultT] | ResultT,
]

NextHandler = Callable[
    [CommandContext, Any],
    Awaitable[Any],
]


class CommandMiddleware(Protocol):
    async def __call__(
        self,
        context: CommandContext,
        request: Any,
        call_next: NextHandler,
    ) -> Any:
        ...
