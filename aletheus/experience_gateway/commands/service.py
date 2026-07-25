from __future__ import annotations

from dataclasses import replace
from datetime import timedelta
from typing import Any
from uuid import uuid4

from aletheus.experience_gateway.security.contracts import (
    AuthorizationPolicy,
    Principal,
)
from aletheus.time_utils import (
    utc_now,
    utc_now_iso,
)

from .contracts import (
    CommandAuthorization,
    CommandExecution,
    CommandPreview,
    CommandRegistry,
    CommandRequest,
)
from .store import CommandAuditStore
from .store_contract import CommandStore


class CommandGatewayService:
    PREVIEW_TTL_SECONDS = 300
    AUTHORIZATION_TTL_SECONDS = 300

    def __init__(
        self,
        registry: CommandRegistry,
        store: CommandStore | None = None,
        authorization_policy: AuthorizationPolicy | None = None,
    ) -> None:
        self._registry = registry
        self._store = (
            store or CommandAuditStore()
        )
        self._authorization_policy = (
            authorization_policy
        )

    def list_commands(
        self,
    ) -> list[dict[str, Any]]:
        return [
            {
                "id": definition.id,
                "name": definition.name,
                "description": (
                    definition.description
                ),
                "risk": definition.risk,
                "reversible": (
                    definition.reversible
                ),
                "authorizationRequired": (
                    definition
                    .authorization_required
                ),
                "requiredArguments": list(
                    definition
                    .required_arguments
                ),
                "effects": list(
                    definition.effects
                ),
                "requiredEntitlements": list(
                    definition.required_entitlements
                ),
            }
            for definition in (
                self._registry
                .list_definitions()
            )
        ]

    def preview(
        self,
        request: CommandRequest,
        *,
        principal: Principal | None = None,
    ) -> CommandPreview:
        definition = self._registry.get(
            request.command_id
        )

        if (
            self._authorization_policy is not None
            and principal is not None
        ):
            decision = (
                self._authorization_policy.evaluate(
                    principal=principal,
                    command_id=definition.id,
                    command_risk=definition.risk,
                    required_entitlements=(
                        definition.required_entitlements
                    ),
                )
            )

            if not decision.allowed:
                raise PermissionError(
                    decision.reason
                )

        self._validate_arguments(
            definition.required_arguments,
            request.arguments,
        )

        now = utc_now()

        preview = CommandPreview(
            preview_id=str(uuid4()),
            command_id=definition.id,
            name=definition.name,
            description=definition.description,
            risk=definition.risk,
            arguments=dict(request.arguments),
            effects=definition.effects,
            required_entitlements=(
                definition.required_entitlements
            ),
            reversible=definition.reversible,
            authorization_required=(
                definition
                .authorization_required
            ),
            requested_by=request.requested_by,
            created_at=now.isoformat(),
            expires_at=(
                now
                + timedelta(
                    seconds=(
                        self.PREVIEW_TTL_SECONDS
                    )
                )
            ).isoformat(),
        )

        self._store.save_preview(preview)

        return preview

    def authorize(
        self,
        *,
        preview_id: str,
        authorized_by: str,
    ) -> CommandAuthorization:
        preview = self._store.preview(
            preview_id
        )

        self._assert_not_expired(
            preview.expires_at,
            "Command preview",
        )

        now = utc_now()

        authorization = (
            CommandAuthorization(
                authorization_id=str(
                    uuid4()
                ),
                preview_id=preview_id,
                authorized_by=authorized_by,
                authorized_at=now.isoformat(),
                expires_at=(
                    now
                    + timedelta(
                        seconds=(
                            self
                            .AUTHORIZATION_TTL_SECONDS
                        )
                    )
                ).isoformat(),
            )
        )

        self._store.save_authorization(
            authorization
        )

        return authorization

    def execute(
        self,
        *,
        preview_id: str,
        authorization_id: str | None,
        idempotency_key: str | None = None,
    ) -> CommandExecution:
        if idempotency_key:
            previous = (
                self._store
                .execution_for_idempotency_key(
                    idempotency_key
                )
            )

            if previous is not None:
                return previous

        preview = self._store.preview(
            preview_id
        )

        self._assert_not_expired(
            preview.expires_at,
            "Command preview",
        )

        definition = self._registry.get(
            preview.command_id
        )

        if (
            definition.authorization_required
        ):
            if authorization_id is None:
                raise PermissionError(
                    "Command authorization is required."
                )

            authorization = (
                self._store.authorization(
                    authorization_id
                )
            )

            if (
                authorization.preview_id
                != preview_id
            ):
                raise PermissionError(
                    "Authorization does not match "
                    "the command preview."
                )

            self._assert_not_expired(
                authorization.expires_at,
                "Command authorization",
            )
        else:
            authorization = None

        execution_id = str(uuid4())

        try:
            result = definition.handler(
                dict(preview.arguments)
            )

            reversal_token = (
                str(uuid4())
                if definition.reversible
                else None
            )

            execution = CommandExecution(
                execution_id=execution_id,
                preview_id=preview_id,
                authorization_id=(
                    authorization.authorization_id
                    if authorization
                    else None
                ),
                command_id=definition.id,
                state="executed",
                result=result,
                requested_by=preview.requested_by,
                executed_at=utc_now_iso(),
                reversible=definition.reversible,
                reversal_token=reversal_token,
            )
        except Exception as error:
            execution = CommandExecution(
                execution_id=execution_id,
                preview_id=preview_id,
                authorization_id=(
                    authorization.authorization_id
                    if authorization
                    else None
                ),
                command_id=definition.id,
                state="failed",
                result={},
                requested_by=preview.requested_by,
                executed_at=utc_now_iso(),
                reversible=False,
                failure=(
                    f"{type(error).__name__}: "
                    f"{error}"
                ),
            )

        self._store.save_execution(
            execution,
            idempotency_key=idempotency_key,
        )

        return execution

    def reverse(
        self,
        *,
        execution_id: str,
        reversal_token: str,
    ) -> CommandExecution:
        execution = self._store.execution(
            execution_id
        )

        if execution.state != "executed":
            raise ValueError(
                "Only successful executions can "
                "be reversed."
            )

        if not execution.reversible:
            raise ValueError(
                "This command is not reversible."
            )

        if (
            execution.reversal_token
            != reversal_token
        ):
            raise PermissionError(
                "Invalid reversal token."
            )

        preview = self._store.preview(
            execution.preview_id
        )

        definition = self._registry.get(
            execution.command_id
        )

        if definition.reversal_handler is None:
            raise RuntimeError(
                "The command has no reversal handler."
            )

        result = definition.reversal_handler(
            {
                "arguments": (
                    dict(preview.arguments)
                ),
                "executionResult": (
                    dict(execution.result)
                ),
            }
        )

        reversed_execution = replace(
            execution,
            state="reversed",
            result={
                **execution.result,
                "reversal": result,
            },
            executed_at=utc_now_iso(),
            reversal_token=None,
        )

        self._store.save_execution(
            reversed_execution
        )

        return reversed_execution

    def history(
        self,
    ) -> tuple[CommandExecution, ...]:
        return self._store.executions()

    @staticmethod
    def _validate_arguments(
        required_arguments: tuple[
            str,
            ...,
        ],
        arguments: dict[str, Any],
    ) -> None:
        missing = [
            name
            for name in required_arguments
            if (
                name not in arguments
                or arguments[name] is None
            )
        ]

        if missing:
            raise ValueError(
                "Missing required command arguments: "
                + ", ".join(missing)
            )

    @staticmethod
    def _assert_not_expired(
        expires_at: str,
        label: str,
    ) -> None:
        from datetime import datetime

        expires = datetime.fromisoformat(
            expires_at
        )

        if utc_now() >= expires:
            raise TimeoutError(
                f"{label} has expired."
            )
