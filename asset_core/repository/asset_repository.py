import sqlite3
import uuid
from datetime import datetime

DB = "data/cardhawk.db"


class AssetRepository:
    """
    CardHawk OS™ Asset Repository

    Responsible for persistence of Asset Vault records.
    """

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
            SET
                thorx_score = ?
            WHERE id = ?
            """,
            (
                score,
                asset_id,
            ),
        )

        conn.commit()
        conn.close()

    @staticmethod
    def update_market(asset_id: int, market: dict):

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE assets
            SET
                current_value=?,
                floor=?,
                ceiling=?,
                average_sale=?,
                highest_sale=?,
                lowest_sale=?,
                market_velocity=?,
                active_listings=?,
                hawk_aeye_confidence=?
            WHERE id=?
            """,
            (
                market.get("current_value", 0),
                market.get("floor", 0),
                market.get("ceiling", 0),
                market.get("average_sale", 0),
                market.get("highest_sale", 0),
                market.get("lowest_sale", 0),
                market.get("market_velocity", "Unknown"),
                market.get("comp_count", 0),
                market.get("confidence", 0),
                asset_id,
            ),
        )

        conn.commit()
        conn.close()

    @staticmethod
    def get(asset_id):

        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()

        cur.execute(
            """
            SELECT *
            FROM assets
            WHERE id=?
            """,
            (asset_id,),
        )

        row = cur.fetchone()

        conn.close()

        return dict(row) if row else None

    @staticmethod
    def all():

        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()

        cur.execute(
            """
            SELECT *
            FROM assets
            ORDER BY id DESC
            """
        )

        rows = [dict(r) for r in cur.fetchall()]

        conn.close()

        return rows
