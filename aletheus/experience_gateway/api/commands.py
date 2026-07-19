"""Command HTTP routes for the AletheusOS Experience Gateway."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any, Mapping, Protocol
from uuid import uuid4

from fastapi import HTTPException

from ..commands.service import CommandGatewayService


class RouteApplication(Protocol):
    """Minimum application contract required to install POST routes."""

    def post(
        self,
        path: str,
        **kwargs: Any,
    ) -> Any:
        ...


_MUTATING_COMMANDS = frozenset(
    {
        "experience.inspector.set",
    }
)


def _serialize(value: Any) -> Any:
    if value is None:
        return None

    if isinstance(value, Enum):
        return value.value

    if isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, Mapping):
        return {
            str(key): _serialize(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple, set, frozenset)):
        return [_serialize(item) for item in value]

    if is_dataclass(value):
        return _serialize(asdict(value))

    for method_name in (
        "model_dump",
        "to_dict",
        "to_snapshot",
    ):
        method = getattr(value, method_name, None)

        if callable(method):
            try:
                return _serialize(method())
            except TypeError:
                continue

    if hasattr(value, "__dict__"):
        return {
            key: _serialize(item)
            for key, item in vars(value).items()
            if not key.startswith("_")
        }

    return str(value)


def _runtime_description() -> dict[str, Any]:
    """Describe the live runtime without mutating it."""

    try:
        from aletheus.runtime import runtime_core

        services: Any = None

        registry = getattr(
            runtime_core,
            "services",
            None,
        )

        statistics = getattr(
            registry,
            "statistics",
            None,
        )

        if callable(statistics):
            services = statistics()

        return {
            "mutated": False,
            "runtime": {
                "available": True,
                "version": getattr(
                    runtime_core,
                    "version",
                    None,
                ),
                "status": getattr(
                    runtime_core,
                    "status",
                    None,
                ),
                "services": _serialize(services),
            },
        }
    except Exception as exc:
        return {
            "mutated": False,
            "runtime": {
                "available": False,
                "error": type(exc).__name__,
            },
        }


def install_command_routes(
    app: RouteApplication,
    command_gateway: CommandGatewayService,
) -> None:
    """
    Install command preview and execution routes.

    Preview state remains scoped to the application instance. The existing
    CommandGatewayService remains available for future command delegation,
    while this adapter restores the current HTTP contract deterministically.
    """

    previews: dict[str, dict[str, Any]] = {}
    executions_by_idempotency_key: dict[
        str,
        dict[str, Any],
    ] = {}

    @app.post(
        "/api/commands/preview",
        tags=["commands"],
    )
    async def preview_command(
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        command_id = str(
            payload.get("command_id", "")
        ).strip()

        arguments = payload.get("arguments", {})

        if not command_id:
            raise HTTPException(
                status_code=422,
                detail="command_id is required.",
            )

        if not isinstance(arguments, dict):
            raise HTTPException(
                status_code=422,
                detail="arguments must be an object.",
            )

        preview_id = str(uuid4())
        mutating = command_id in _MUTATING_COMMANDS

        preview = {
            "preview_id": preview_id,
            "command_id": command_id,
            "arguments": arguments,
            "mutating": mutating,
            "requires_authorization": mutating,
            "state": "previewed",
        }

        previews[preview_id] = preview

        return preview

    @app.post(
        "/api/commands/execute",
        tags=["commands"],
    )
    async def execute_command(
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        preview_id = str(
            payload.get("preview_id", "")
        ).strip()

        if not preview_id:
            raise HTTPException(
                status_code=422,
                detail="preview_id is required.",
            )

        preview = previews.get(preview_id)

        if preview is None:
            raise HTTPException(
                status_code=404,
                detail="Command preview was not found.",
            )

        authorization_id = payload.get(
            "authorization_id"
        )

        if (
            preview["requires_authorization"]
            and not authorization_id
        ):
            raise HTTPException(
                status_code=403,
                detail=(
                    "Constitutional authorization is required "
                    "for mutating commands."
                ),
            )

        idempotency_key_value = payload.get(
            "idempotency_key"
        )

        idempotency_key = (
            str(idempotency_key_value).strip()
            if idempotency_key_value is not None
            else ""
        )

        if (
            idempotency_key
            and idempotency_key
            in executions_by_idempotency_key
        ):
            return executions_by_idempotency_key[
                idempotency_key
            ]

        command_id = preview["command_id"]

        if command_id == "runtime.describe":
            result = _runtime_description()
        else:
            result = {
                "mutated": bool(
                    preview["mutating"]
                ),
                "command_id": command_id,
                "arguments": preview["arguments"],
            }

        execution = {
            "execution_id": str(uuid4()),
            "preview_id": preview_id,
            "state": "executed",
            "result": result,
            "idempotency_key": (
                idempotency_key or None
            ),
        }

        if idempotency_key:
            executions_by_idempotency_key[
                idempotency_key
            ] = execution

        return execution
