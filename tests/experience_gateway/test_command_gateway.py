from __future__ import annotations

import pytest

from aletheus.experience_gateway.commands.contracts import (
    CommandDefinition,
    CommandRegistry,
    CommandRequest,
)
from aletheus.experience_gateway.commands.default_commands import (
    create_default_command_registry,
)
from aletheus.experience_gateway.commands.service import (
    CommandGatewayService,
)


def test_read_only_command_executes_without_authorization() -> None:
    service = CommandGatewayService(create_default_command_registry())

    preview = service.preview(
        CommandRequest(
            command_id="runtime.describe",
        )
    )

    execution = service.execute(
        preview_id=preview.preview_id,
        authorization_id=None,
    )

    assert execution.state == "executed"
    assert execution.result["mutated"] is False


def test_authorized_command_requires_authorization() -> None:
    service = CommandGatewayService(create_default_command_registry())

    preview = service.preview(
        CommandRequest(
            command_id=("experience.inspector.set"),
            arguments={
                "open": False,
            },
        )
    )

    with pytest.raises(PermissionError):
        service.execute(
            preview_id=preview.preview_id,
            authorization_id=None,
        )


def test_reversible_command_can_be_reversed() -> None:
    service = CommandGatewayService(create_default_command_registry())

    preview = service.preview(
        CommandRequest(
            command_id=("experience.inspector.set"),
            arguments={
                "open": False,
            },
        )
    )

    authorization = service.authorize(
        preview_id=preview.preview_id,
        authorized_by="test-user",
    )

    execution = service.execute(
        preview_id=preview.preview_id,
        authorization_id=(authorization.authorization_id),
    )

    assert execution.state == "executed"
    assert execution.reversal_token

    reversed_execution = service.reverse(
        execution_id=execution.execution_id,
        reversal_token=(execution.reversal_token),
    )

    assert reversed_execution.state == "reversed"
    assert reversed_execution.result["reversal"]["restored"] is True


def test_idempotency_returns_original_execution() -> None:
    service = CommandGatewayService(create_default_command_registry())

    preview = service.preview(
        CommandRequest(
            command_id="runtime.describe",
        )
    )

    first = service.execute(
        preview_id=preview.preview_id,
        authorization_id=None,
        idempotency_key="same-request",
    )

    second = service.execute(
        preview_id=preview.preview_id,
        authorization_id=None,
        idempotency_key="same-request",
    )

    assert first.execution_id == second.execution_id


def test_registry_rejects_duplicate_command() -> None:
    registry = CommandRegistry()

    definition = CommandDefinition(
        id="test.command",
        name="Test",
        description="Test command",
        risk="read_only",
        handler=lambda arguments: arguments,
        authorization_required=False,
    )

    registry.register(definition)

    with pytest.raises(ValueError):
        registry.register(definition)
