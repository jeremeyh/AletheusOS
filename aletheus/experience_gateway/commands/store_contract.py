from __future__ import annotations

from typing import Protocol

from .contracts import (
    CommandAuthorization,
    CommandExecution,
    CommandPreview,
)


class CommandStore(Protocol):
    def save_preview(
        self,
        preview: CommandPreview,
    ) -> None:
        ...

    def preview(
        self,
        preview_id: str,
    ) -> CommandPreview:
        ...

    def save_authorization(
        self,
        authorization: CommandAuthorization,
    ) -> None:
        ...

    def authorization(
        self,
        authorization_id: str,
    ) -> CommandAuthorization:
        ...

    def save_execution(
        self,
        execution: CommandExecution,
        *,
        idempotency_key: str | None = None,
    ) -> None:
        ...

    def execution(
        self,
        execution_id: str,
    ) -> CommandExecution:
        ...

    def execution_for_idempotency_key(
        self,
        idempotency_key: str,
    ) -> CommandExecution | None:
        ...

    def executions(
        self,
    ) -> tuple[CommandExecution, ...]:
        ...
