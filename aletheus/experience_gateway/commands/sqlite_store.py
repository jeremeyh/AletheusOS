from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from pathlib import Path
from threading import RLock
from typing import Any

from .contracts import (
    CommandAuthorization,
    CommandExecution,
    CommandPreview,
)


class SQLiteCommandAuditStore:
    """Durable command audit persistence with SQLite."""

    def __init__(
        self,
        database_path: str | Path,
    ) -> None:
        self._database_path = Path(
            database_path
        ).expanduser().resolve()

        self._database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._lock = RLock()
        self._initialize_schema()

    @property
    def database_path(self) -> Path:
        return self._database_path

    def save_preview(
        self,
        preview: CommandPreview,
    ) -> None:
        payload = _to_json(preview)

        with self._lock, self._connect() as connection:
            connection.execute(
                """
                INSERT INTO command_previews (
                    preview_id,
                    command_id,
                    requested_by,
                    state,
                    created_at,
                    expires_at,
                    payload_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(preview_id) DO UPDATE SET
                    command_id = excluded.command_id,
                    requested_by = excluded.requested_by,
                    state = excluded.state,
                    created_at = excluded.created_at,
                    expires_at = excluded.expires_at,
                    payload_json = excluded.payload_json
                """,
                (
                    preview.preview_id,
                    preview.command_id,
                    preview.requested_by,
                    preview.state,
                    preview.created_at,
                    preview.expires_at,
                    payload,
                ),
            )

    def preview(
        self,
        preview_id: str,
    ) -> CommandPreview:
        row = self._fetch_one(
            """
            SELECT payload_json
            FROM command_previews
            WHERE preview_id = ?
            """,
            (preview_id,),
        )

        if row is None:
            raise KeyError(
                "Unknown command preview: "
                f"{preview_id}"
            )

        return CommandPreview(
            **json.loads(row["payload_json"])
        )

    def save_authorization(
        self,
        authorization: CommandAuthorization,
    ) -> None:
        payload = _to_json(authorization)

        with self._lock, self._connect() as connection:
            connection.execute(
                """
                INSERT INTO command_authorizations (
                    authorization_id,
                    preview_id,
                    authorized_by,
                    state,
                    authorized_at,
                    expires_at,
                    payload_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(authorization_id) DO UPDATE SET
                    preview_id = excluded.preview_id,
                    authorized_by = excluded.authorized_by,
                    state = excluded.state,
                    authorized_at = excluded.authorized_at,
                    expires_at = excluded.expires_at,
                    payload_json = excluded.payload_json
                """,
                (
                    authorization.authorization_id,
                    authorization.preview_id,
                    authorization.authorized_by,
                    authorization.state,
                    authorization.authorized_at,
                    authorization.expires_at,
                    payload,
                ),
            )

    def authorization(
        self,
        authorization_id: str,
    ) -> CommandAuthorization:
        row = self._fetch_one(
            """
            SELECT payload_json
            FROM command_authorizations
            WHERE authorization_id = ?
            """,
            (authorization_id,),
        )

        if row is None:
            raise KeyError(
                "Unknown command authorization: "
                f"{authorization_id}"
            )

        return CommandAuthorization(
            **json.loads(row["payload_json"])
        )

    def save_execution(
        self,
        execution: CommandExecution,
        *,
        idempotency_key: str | None = None,
    ) -> None:
        payload = _to_json(execution)

        with self._lock, self._connect() as connection:
            connection.execute(
                """
                INSERT INTO command_executions (
                    execution_id,
                    preview_id,
                    authorization_id,
                    command_id,
                    requested_by,
                    state,
                    executed_at,
                    reversible,
                    reversal_token,
                    failure,
                    payload_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(execution_id) DO UPDATE SET
                    preview_id = excluded.preview_id,
                    authorization_id = excluded.authorization_id,
                    command_id = excluded.command_id,
                    requested_by = excluded.requested_by,
                    state = excluded.state,
                    executed_at = excluded.executed_at,
                    reversible = excluded.reversible,
                    reversal_token = excluded.reversal_token,
                    failure = excluded.failure,
                    payload_json = excluded.payload_json
                """,
                (
                    execution.execution_id,
                    execution.preview_id,
                    execution.authorization_id,
                    execution.command_id,
                    execution.requested_by,
                    execution.state,
                    execution.executed_at,
                    int(execution.reversible),
                    execution.reversal_token,
                    execution.failure,
                    payload,
                ),
            )

            if idempotency_key:
                connection.execute(
                    """
                    INSERT INTO command_idempotency (
                        idempotency_key,
                        execution_id
                    )
                    VALUES (?, ?)
                    ON CONFLICT(idempotency_key) DO NOTHING
                    """,
                    (
                        idempotency_key,
                        execution.execution_id,
                    ),
                )

    def execution(
        self,
        execution_id: str,
    ) -> CommandExecution:
        row = self._fetch_one(
            """
            SELECT payload_json
            FROM command_executions
            WHERE execution_id = ?
            """,
            (execution_id,),
        )

        if row is None:
            raise KeyError(
                "Unknown command execution: "
                f"{execution_id}"
            )

        return CommandExecution(
            **json.loads(row["payload_json"])
        )

    def execution_for_idempotency_key(
        self,
        idempotency_key: str,
    ) -> CommandExecution | None:
        row = self._fetch_one(
            """
            SELECT execution_id
            FROM command_idempotency
            WHERE idempotency_key = ?
            """,
            (idempotency_key,),
        )

        if row is None:
            return None

        return self.execution(
            row["execution_id"]
        )

    def executions(
        self,
    ) -> tuple[CommandExecution, ...]:
        with self._lock, self._connect() as connection:
            rows = connection.execute(
                """
                SELECT payload_json
                FROM command_executions
                ORDER BY executed_at DESC
                """
            ).fetchall()

        return tuple(
            CommandExecution(
                **json.loads(row["payload_json"])
            )
            for row in rows
        )

    def counts(self) -> dict[str, int]:
        with self._lock, self._connect() as connection:
            return {
                "previews": self._count(
                    connection,
                    "command_previews",
                ),
                "authorizations": self._count(
                    connection,
                    "command_authorizations",
                ),
                "executions": self._count(
                    connection,
                    "command_executions",
                ),
                "idempotencyKeys": self._count(
                    connection,
                    "command_idempotency",
                ),
            }

    def _initialize_schema(self) -> None:
        with self._lock, self._connect() as connection:
            connection.executescript(
                """
                PRAGMA journal_mode = WAL;
                PRAGMA foreign_keys = ON;

                CREATE TABLE IF NOT EXISTS command_previews (
                    preview_id TEXT PRIMARY KEY,
                    command_id TEXT NOT NULL,
                    requested_by TEXT NOT NULL,
                    state TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS command_authorizations (
                    authorization_id TEXT PRIMARY KEY,
                    preview_id TEXT NOT NULL,
                    authorized_by TEXT NOT NULL,
                    state TEXT NOT NULL,
                    authorized_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    FOREIGN KEY(preview_id)
                        REFERENCES command_previews(preview_id)
                );

                CREATE TABLE IF NOT EXISTS command_executions (
                    execution_id TEXT PRIMARY KEY,
                    preview_id TEXT NOT NULL,
                    authorization_id TEXT,
                    command_id TEXT NOT NULL,
                    requested_by TEXT NOT NULL,
                    state TEXT NOT NULL,
                    executed_at TEXT NOT NULL,
                    reversible INTEGER NOT NULL,
                    reversal_token TEXT,
                    failure TEXT,
                    payload_json TEXT NOT NULL,
                    FOREIGN KEY(preview_id)
                        REFERENCES command_previews(preview_id),
                    FOREIGN KEY(authorization_id)
                        REFERENCES command_authorizations(
                            authorization_id
                        )
                );

                CREATE TABLE IF NOT EXISTS command_idempotency (
                    idempotency_key TEXT PRIMARY KEY,
                    execution_id TEXT NOT NULL,
                    FOREIGN KEY(execution_id)
                        REFERENCES command_executions(execution_id)
                );

                CREATE INDEX IF NOT EXISTS
                    idx_command_executions_executed_at
                ON command_executions(executed_at DESC);

                CREATE INDEX IF NOT EXISTS
                    idx_command_executions_command_id
                ON command_executions(command_id);

                CREATE INDEX IF NOT EXISTS
                    idx_command_executions_state
                ON command_executions(state);
                """
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self._database_path,
            timeout=10,
        )

        connection.row_factory = sqlite3.Row
        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        return connection

    def _fetch_one(
        self,
        query: str,
        parameters: tuple[Any, ...],
    ) -> sqlite3.Row | None:
        with self._lock, self._connect() as connection:
            return connection.execute(
                query,
                parameters,
            ).fetchone()

    @staticmethod
    def _count(
        connection: sqlite3.Connection,
        table: str,
    ) -> int:
        allowed_tables = {
            "command_previews",
            "command_authorizations",
            "command_executions",
            "command_idempotency",
        }

        if table not in allowed_tables:
            raise ValueError(
                f"Unsupported audit table: {table}"
            )

        row = connection.execute(
            f"SELECT COUNT(*) AS count FROM {table}"
        ).fetchone()

        return int(row["count"])


def _to_json(
    value: object,
) -> str:
    return json.dumps(
        asdict(value),
        sort_keys=True,
        separators=(",", ":"),
    )
