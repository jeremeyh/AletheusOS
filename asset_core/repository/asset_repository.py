import sqlite3
import uuid
from datetime import datetime

DB = "data/cardhawk.db"


class AssetRepository:

    @staticmethod
    def save(card):

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO assets (
                player,
                year,
                brand,
                set_name,
                grade,
                created_at,
                uuid
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                card.get("player"),
                card.get("year"),
                card.get("brand"),
                card.get("set"),
                card.get("grade"),
                datetime.utcnow().isoformat(),
                str(uuid.uuid4()),
            ),
        )

        conn.commit()
        asset_id = cur.lastrowid
        conn.close()

        return asset_id

    @staticmethod
    def update_thorx(asset_id: int, score: float):

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE assets
            SET thorx_score = ?
            WHERE id = ?
            """,
            (score, asset_id),
        )

        conn.commit()
        conn.close()

    @staticmethod
    def update_market(asset_id: int, value: dict):

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE assets
            SET
                current_value = ?,
                floor = ?,
                ceiling = ?
            WHERE id = ?
            """,
            (
                value["current_value"],
                value["floor"],
                value["ceiling"],
                asset_id,
            ),
        )

        conn.commit()
        conn.close()
