from __future__ import annotations

from pathlib import Path

from aletheus.experience_gateway.commands.contracts import (
    CommandRequest,
)
from aletheus.experience_gateway.commands.default_commands import (
    create_default_command_registry,
)
from aletheus.experience_gateway.commands.service import (
    CommandGatewayService,
)
from aletheus.experience_gateway.commands.sqlite_store import (
    SQLiteCommandAuditStore,
)


def create_service(
    database_path: Path,
) -> CommandGatewayService:
    return CommandGatewayService(
        create_default_command_registry(),
        store=SQLiteCommandAuditStore(
            database_path
        ),
    )


def test_execution_survives_service_restart(
    tmp_path: Path,
) -> None:
    database_path = (
        tmp_path / "commands.sqlite3"
    )

    first_service = create_service(
        database_path
    )

    preview = first_service.preview(
        CommandRequest(
            command_id="runtime.describe",
        )
    )

    execution = first_service.execute(
        preview_id=preview.preview_id,
        authorization_id=None,
        idempotency_key="restart-test",
    )

    second_service = create_service(
        database_path
    )

    restored = second_service.history()

    assert len(restored) == 1
    assert (
        restored[0].execution_id
        == execution.execution_id
    )


def test_idempotency_survives_restart(
    tmp_path: Path,
) -> None:
    database_path = (
        tmp_path / "commands.sqlite3"
    )

    first_service = create_service(
        database_path
    )

    preview = first_service.preview(
        CommandRequest(
            command_id="runtime.describe",
        )
    )

    first_execution = first_service.execute(
        preview_id=preview.preview_id,
        authorization_id=None,
        idempotency_key="durable-key",
    )

    second_service = create_service(
        database_path
    )

    second_execution = second_service.execute(
        preview_id=preview.preview_id,
        authorization_id=None,
        idempotency_key="durable-key",
    )

    assert (
        first_execution.execution_id
        == second_execution.execution_id
    )


def test_reversal_survives_restart(
    tmp_path: Path,
) -> None:
    database_path = (
        tmp_path / "commands.sqlite3"
    )

    first_service = create_service(
        database_path
    )

    preview = first_service.preview(
        CommandRequest(
            command_id=(
                "experience.inspector.set"
            ),
            arguments={
                "open": False,
            },
        )
    )

    authorization = first_service.authorize(
        preview_id=preview.preview_id,
        authorized_by="test-user",
    )

    execution = first_service.execute(
        preview_id=preview.preview_id,
        authorization_id=(
            authorization.authorization_id
        ),
    )

    assert execution.reversal_token

    second_service = create_service(
        database_path
    )

    reversed_execution = (
        second_service.reverse(
            execution_id=(
                execution.execution_id
            ),
            reversal_token=(
                execution.reversal_token
            ),
        )
    )

    assert (
        reversed_execution.state
        == "reversed"
    )

    third_service = create_service(
        database_path
    )

    persisted = third_service.history()

    assert persisted[0].state == "reversed"


def test_store_reports_durable_counts(
    tmp_path: Path,
) -> None:
    store = SQLiteCommandAuditStore(
        tmp_path / "commands.sqlite3"
    )

    service = CommandGatewayService(
        create_default_command_registry(),
        store=store,
    )

    preview = service.preview(
        CommandRequest(
            command_id="runtime.describe",
        )
    )

    service.execute(
        preview_id=preview.preview_id,
        authorization_id=None,
        idempotency_key="count-test",
    )

    counts = store.counts()

    assert counts == {
        "previews": 1,
        "authorizations": 0,
        "executions": 1,
        "idempotencyKeys": 1,
    }
