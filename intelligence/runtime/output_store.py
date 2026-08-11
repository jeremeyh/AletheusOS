import sqlite3
from datetime import datetime
from pathlib import Path

DB = "data/cardhawk.db"


class EngineOutputStore:
    @staticmethod
    def connect():
        Path("data").mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def ensure_schema():
        conn = EngineOutputStore.connect()
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS engine_outputs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id INTEGER,
                engine TEXT NOT NULL,
                score REAL DEFAULT 0,
                recommendation TEXT,
                payload TEXT,
                created_at TEXT
            )
            """
        )

        conn.commit()
        conn.close()

    @staticmethod
    def save(
        asset_id,
        engine,
        score=0,
        recommendation="",
        payload="",
    ):
        EngineOutputStore.ensure_schema()

        conn = EngineOutputStore.connect()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO engine_outputs (
                asset_id,
                engine,
                score,
                recommendation,
                payload,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                asset_id,
                engine,
                float(score or 0),
                recommendation,
                str(payload),
                datetime.utcnow().isoformat(),
            ),
        )

        conn.commit()
        output_id = cur.lastrowid
        conn.close()

        return output_id

    @staticmethod
    def latest(asset_id, engine):
        EngineOutputStore.ensure_schema()

        conn = EngineOutputStore.connect()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT *
            FROM engine_outputs
            WHERE asset_id = ?
            AND engine = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (asset_id, engine),
        )

        row = cur.fetchone()
        conn.close()

        return dict(row) if row else None
