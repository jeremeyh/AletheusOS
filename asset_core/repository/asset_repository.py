import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

DB = "data/cardhawk.db"


class AssetRepository:
    """
    CardHawkOS Asset Repository

    Central persistent CRUD layer for Asset Vault records.
    """

    @staticmethod
    def connect():
        Path("data").mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row

        return conn

    @staticmethod
    def ensure_schema():
        conn = AssetRepository.connect()
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT NOT NULL,
                sport TEXT,
                team TEXT,
                year INTEGER,
                brand TEXT,
                set_name TEXT,
                card_number TEXT,
                parallel TEXT,
                rookie INTEGER DEFAULT 0,
                first_bowman INTEGER DEFAULT 0,
                autograph INTEGER DEFAULT 0,
                patch INTEGER DEFAULT 0,
                serial_number TEXT,
                print_run INTEGER,
                grading_company TEXT,
                grade TEXT,
                condition TEXT DEFAULT 'Raw',
                purchase_price REAL DEFAULT 0,
                current_value REAL DEFAULT 0,
                market_value REAL DEFAULT 0,
                floor REAL DEFAULT 0,
                ceiling REAL DEFAULT 0,
                average_sale REAL DEFAULT 0,
                highest_sale REAL DEFAULT 0,
                lowest_sale REAL DEFAULT 0,
                active_listings INTEGER DEFAULT 0,
                sold_comps INTEGER DEFAULT 0,
                market_velocity TEXT,
                thorx_score REAL DEFAULT 0,
                q_def REAL DEFAULT 0,
                d_def REAL DEFAULT 0,
                hawk_rating REAL DEFAULT 0,
                hawk_tier TEXT,
                founder_rating TEXT,
                recommendation TEXT,
                image_path TEXT,
                front_image TEXT,
                back_image TEXT,
                notes TEXT,
                status TEXT DEFAULT 'Active',
                created_at TEXT,
                updated_at TEXT,
                uuid TEXT
            )
            """
        )

        required_columns = {
            "player": "TEXT",
            "sport": "TEXT",
            "team": "TEXT",
            "year": "INTEGER",
            "brand": "TEXT",
            "set_name": "TEXT",
            "card_number": "TEXT",
            "parallel": "TEXT",
            "rookie": "INTEGER DEFAULT 0",
            "first_bowman": "INTEGER DEFAULT 0",
            "autograph": "INTEGER DEFAULT 0",
            "patch": "INTEGER DEFAULT 0",
            "serial_number": "TEXT",
            "print_run": "INTEGER",
            "grading_company": "TEXT",
            "grade": "TEXT",
            "condition": "TEXT DEFAULT 'Raw'",
            "purchase_price": "REAL DEFAULT 0",
            "current_value": "REAL DEFAULT 0",
            "market_value": "REAL DEFAULT 0",
            "floor": "REAL DEFAULT 0",
            "ceiling": "REAL DEFAULT 0",
            "average_sale": "REAL DEFAULT 0",
            "highest_sale": "REAL DEFAULT 0",
            "lowest_sale": "REAL DEFAULT 0",
            "active_listings": "INTEGER DEFAULT 0",
            "sold_comps": "INTEGER DEFAULT 0",
            "market_velocity": "TEXT",
            "thorx_score": "REAL DEFAULT 0",
            "q_def": "REAL DEFAULT 0",
            "d_def": "REAL DEFAULT 0",
            "hawk_rating": "REAL DEFAULT 0",
            "hawk_tier": "TEXT",
            "founder_rating": "TEXT",
            "recommendation": "TEXT",
            "image_path": "TEXT",
            "front_image": "TEXT",
            "back_image": "TEXT",
            "notes": "TEXT",
            "status": "TEXT DEFAULT 'Active'",
            "created_at": "TEXT",
            "updated_at": "TEXT",
            "uuid": "TEXT",
        }

        cur.execute("PRAGMA table_info(assets)")
        existing_columns = {row["name"] for row in cur.fetchall()}

        for column, definition in required_columns.items():
            if column not in existing_columns:
                cur.execute(f"ALTER TABLE assets ADD COLUMN {column} {definition}")

        conn.commit()
        conn.close()

    @staticmethod
    def save(card):
        AssetRepository.ensure_schema()

        now = datetime.utcnow().isoformat()

        player = (
            card.get("player")
            or card.get("name")
            or card.get("asset_name")
            or "Unknown"
        )

        values = {
            "player": player,
            "sport": card.get("sport"),
            "team": card.get("team"),
            "year": card.get("year"),
            "brand": card.get("brand"),
            "set_name": card.get("set_name") or card.get("set"),
            "card_number": card.get("card_number"),
            "parallel": card.get("parallel"),
            "rookie": int(bool(card.get("rookie"))),
            "first_bowman": int(bool(card.get("first_bowman"))),
            "autograph": int(bool(card.get("autograph"))),
            "patch": int(bool(card.get("patch"))),
            "serial_number": card.get("serial_number") or card.get("serial"),
            "print_run": card.get("print_run"),
            "grading_company": card.get("grading_company") or card.get("grade_company"),
            "grade": card.get("grade"),
            "condition": card.get("condition") or "Raw",
            "purchase_price": float(card.get("purchase_price") or 0),
            "current_value": float(
                card.get("current_value") or card.get("market_value") or 0
            ),
            "market_value": float(
                card.get("market_value") or card.get("current_value") or 0
            ),
            "floor": float(card.get("floor") or 0),
            "ceiling": float(card.get("ceiling") or 0),
            "thorx_score": float(card.get("thorx_score") or 0),
            "hawk_rating": float(card.get("hawk_rating") or 0),
            "hawk_tier": card.get("hawk_tier"),
            "founder_rating": card.get("founder_rating"),
            "recommendation": card.get("recommendation"),
            "image_path": card.get("image_path"),
            "front_image": card.get("front_image"),
            "back_image": card.get("back_image"),
            "notes": card.get("notes"),
            "status": card.get("status") or "Active",
            "created_at": now,
            "updated_at": now,
            "uuid": str(uuid.uuid4()),
        }

        columns = list(values.keys())
        placeholders = ", ".join(["?"] * len(columns))

        conn = AssetRepository.connect()
        cur = conn.cursor()

        cur.execute(
            f"""
            INSERT INTO assets (
                {", ".join(columns)}
            )
            VALUES (
                {placeholders}
            )
            """,
            [values[column] for column in columns],
        )

        conn.commit()
        asset_id = cur.lastrowid
        conn.close()

        return asset_id

    @staticmethod
    def all(include_archived=False):
        AssetRepository.ensure_schema()

        conn = AssetRepository.connect()
        cur = conn.cursor()

        if include_archived:
            cur.execute(
                """
                SELECT *
                FROM assets
                ORDER BY id DESC
                """
            )
        else:
            cur.execute(
                """
                SELECT *
                FROM assets
                WHERE COALESCE(status, 'Active') != 'Archived'
                ORDER BY id DESC
                """
            )

        rows = cur.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    @staticmethod
    def get(asset_id):
        AssetRepository.ensure_schema()

        conn = AssetRepository.connect()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT *
            FROM assets
            WHERE id = ?
            """,
            (asset_id,),
        )

        row = cur.fetchone()
        conn.close()

        return dict(row) if row else None

    @staticmethod
    def update(asset_id, updates):
        AssetRepository.ensure_schema()

        if not updates:
            return False

        allowed_columns = {
            "player",
            "sport",
            "team",
            "year",
            "brand",
            "set_name",
            "card_number",
            "parallel",
            "rookie",
            "first_bowman",
            "autograph",
            "patch",
            "serial_number",
            "print_run",
            "grading_company",
            "grade",
            "condition",
            "purchase_price",
            "current_value",
            "market_value",
            "floor",
            "ceiling",
            "average_sale",
            "highest_sale",
            "lowest_sale",
            "active_listings",
            "sold_comps",
            "market_velocity",
            "thorx_score",
            "q_def",
            "d_def",
            "hawk_rating",
            "hawk_tier",
            "founder_rating",
            "recommendation",
            "image_path",
            "front_image",
            "back_image",
            "notes",
            "status",
        }

        fields = []
        values = []

        for key, value in updates.items():
            if key in allowed_columns:
                fields.append(f"{key} = ?")
                values.append(value)

        if not fields:
            return False

        fields.append("updated_at = ?")
        values.append(datetime.utcnow().isoformat())
        values.append(asset_id)

        conn = AssetRepository.connect()
        cur = conn.cursor()

        cur.execute(
            f"""
            UPDATE assets
            SET {", ".join(fields)}
            WHERE id = ?
            """,
            values,
        )

        conn.commit()
        conn.close()

        return True

    @staticmethod
    def update_thorx(asset_id, score):
        if isinstance(score, dict):
            score = score.get("score", 0)

        return AssetRepository.update(
            asset_id,
            {
                "thorx_score": float(score or 0),
            },
        )

    @staticmethod
    def update_market(asset_id, market):
        return AssetRepository.update(
            asset_id,
            {
                "current_value": float(market.get("current_value") or 0),
                "market_value": float(market.get("current_value") or 0),
                "floor": float(market.get("floor") or 0),
                "ceiling": float(market.get("ceiling") or 0),
                "average_sale": float(market.get("average_sale") or 0),
                "highest_sale": float(market.get("highest_sale") or 0),
                "lowest_sale": float(market.get("lowest_sale") or 0),
                "active_listings": int(market.get("comp_count") or 0),
                "sold_comps": int(market.get("comp_count") or 0),
                "market_velocity": market.get("market_velocity") or "Unknown",
            },
        )

    @staticmethod
    def archive(asset_id):
        return AssetRepository.update(
            asset_id,
            {
                "status": "Archived",
            },
        )

    @staticmethod
    def restore(asset_id):
        return AssetRepository.update(
            asset_id,
            {
                "status": "Active",
            },
        )

    @staticmethod
    def delete(asset_id):
        AssetRepository.ensure_schema()

        conn = AssetRepository.connect()
        cur = conn.cursor()

        cur.execute(
            """
            DELETE FROM assets
            WHERE id = ?
            """,
            (asset_id,),
        )

        conn.commit()
        conn.close()

        return True

    @staticmethod
    def count(include_archived=False):
        return len(
            AssetRepository.all(
                include_archived=include_archived,
            )
        )
