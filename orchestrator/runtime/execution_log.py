import sqlite3
from datetime import datetime
from pathlib import Path

DB = "data/cardhawk.db"


class OrchestratorExecutionLog:
    """
    ORCHESTRATOR™ Execution Log

    Persistent pipeline execution history.
    """

    @staticmethod
    def connect():
        Path("data").mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def ensure_schema():
        conn = OrchestratorExecutionLog.connect()
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS orchestrator_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id INTEGER,
                status TEXT,
                steps INTEGER DEFAULT 0,
                errors INTEGER DEFAULT 0,
                duration REAL DEFAULT 0,
                payload TEXT,
                created_at TEXT
            )
            """
        )

        conn.commit()
        conn.close()

    @staticmethod
    def record(context, status="SUCCESS", duration=0):
        OrchestratorExecutionLog.ensure_schema()

        conn = OrchestratorExecutionLog.connect()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO orchestrator_runs (
                asset_id,
                status,
                steps,
                errors,
                duration,
                payload,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                context.asset_id,
                status,
                len(context.events),
                len(context.errors),
                float(duration or 0),
                str(context.to_dict()),
                datetime.utcnow().isoformat(),
            ),
        )

        conn.commit()
        run_id = cur.lastrowid
        conn.close()

        return run_id

    @staticmethod
    def recent(limit=25):
        OrchestratorExecutionLog.ensure_schema()

        conn = OrchestratorExecutionLog.connect()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT *
            FROM orchestrator_runs
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )

        rows = [dict(row) for row in cur.fetchall()]
        conn.close()

        return rows
