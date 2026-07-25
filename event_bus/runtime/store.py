import sqlite3
from datetime import datetime
from pathlib import Path

DB = "data/cardhawk.db"


class EventStore:
    @staticmethod
    def connect():
        Path("data").mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def ensure_schema():
        conn = EventStore.connect()
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                source TEXT,
                asset_id INTEGER,
                title TEXT,
                message TEXT,
                payload TEXT,
                created_at TEXT
            )
            """
        )

        conn.commit()
        conn.close()

    @staticmethod
    def record(
        event_type,
        source="CardHawkOS",
        asset_id=None,
        title="",
        message="",
        payload="",
    ):
        EventStore.ensure_schema()

        conn = EventStore.connect()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO events (
                event_type,
                source,
                asset_id,
                title,
                message,
                payload,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_type,
                source,
                asset_id,
                title,
                message,
                payload,
                datetime.utcnow().isoformat(),
            ),
        )

        conn.commit()
        event_id = cur.lastrowid
        conn.close()

        return event_id

    @staticmethod
    def recent(limit=25):
        EventStore.ensure_schema()

        conn = EventStore.connect()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT *
            FROM events
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )

        rows = [dict(row) for row in cur.fetchall()]
        conn.close()

        return rows
