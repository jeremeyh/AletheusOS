from __future__ import annotations

from dataclasses import dataclass, field
from threading import RLock

from .contracts import (
    CommandAuthorization,
    CommandExecution,
    CommandPreview,
)


@dataclass(slots=True)
class CommandAuditStore:
    _previews: dict[
        str,
        CommandPreview,
    ] = field(default_factory=dict)

    _authorizations: dict[
        str,
        CommandAuthorization,
    ] = field(default_factory=dict)

    _executions: dict[
        str,
        CommandExecution,
    ] = field(default_factory=dict)

    _idempotency_index: dict[
        str,
        str,
    ] = field(default_factory=dict)

    _lock: RLock = field(default_factory=RLock)

    def save_preview(
        self,
        preview: CommandPreview,
    ) -> None:
        with self._lock:
            self._previews[preview.preview_id] = preview

    def preview(
        self,
        preview_id: str,
    ) -> CommandPreview:
        with self._lock:
            try:
                return self._previews[preview_id]
            except KeyError as error:
                raise KeyError(f"Unknown command preview: {preview_id}") from error

    def save_authorization(
        self,
        authorization: CommandAuthorization,
    ) -> None:
        with self._lock:
            self._authorizations[authorization.authorization_id] = authorization

    def authorization(
        self,
        authorization_id: str,
    ) -> CommandAuthorization:
        with self._lock:
            try:
                return self._authorizations[authorization_id]
            except KeyError as error:
                raise KeyError(
                    f"Unknown command authorization: {authorization_id}"
                ) from error

    def save_execution(
        self,
        execution: CommandExecution,
        *,
        idempotency_key: str | None = None,
    ) -> None:
        with self._lock:
            self._executions[execution.execution_id] = execution

            if idempotency_key:
                self._idempotency_index[idempotency_key] = execution.execution_id

    def execution(
        self,
        execution_id: str,
    ) -> CommandExecution:
        with self._lock:
            try:
                return self._executions[execution_id]
            except KeyError as error:
                raise KeyError(f"Unknown command execution: {execution_id}") from error

    def execution_for_idempotency_key(
        self,
        idempotency_key: str,
    ) -> CommandExecution | None:
        with self._lock:
            execution_id = self._idempotency_index.get(idempotency_key)

            if execution_id is None:
                return None

            return self._executions[execution_id]

    def executions(
        self,
    ) -> tuple[CommandExecution, ...]:
        with self._lock:
            return tuple(self._executions.values())
