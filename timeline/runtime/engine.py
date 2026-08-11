import sqlite3
from datetime import datetime

DB = "data/cardhawk.db"


class TimelineEngine:
    @staticmethod
    def initialize():

        conn = sqlite3.connect(DB)

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS timeline (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                asset_id INTEGER,

                event_type TEXT,

                description TEXT,

                created_at TEXT

            )
            """
        )

        conn.commit()
        conn.close()

    @staticmethod
    def add_event(
        asset_id,
        event_type,
        description,
    ):

        conn = sqlite3.connect(DB)

        conn.execute(
            """
            INSERT INTO timeline (

                asset_id,
                event_type,
                description,
                created_at

            )
            VALUES (?, ?, ?, ?)
            """,
            (
                asset_id,
                event_type,
                description,
                datetime.utcnow().isoformat(),
            ),
        )

        conn.commit()
        conn.close()

    @staticmethod
    def get_events(asset_id):

        conn = sqlite3.connect(DB)

        conn.row_factory = sqlite3.Row

        rows = conn.execute(
            """
            SELECT *

            FROM timeline

            WHERE asset_id = ?

            ORDER BY created_at DESC
            """,
            (asset_id,),
        ).fetchall()

        conn.close()

        return [dict(row) for row in rows]
