from datetime import datetime
from services.database import db


class GenomeService:
    """
    Asset Genome™ Service

    Records the living history of an asset:
    creation, updates, scans, valuations, THORᵡ changes, offers, sales, etc.
    """

    @staticmethod
    def record_event(
        asset_id: int,
        event_type: str,
        event_note: str = "",
        previous_value: str = "",
        new_value: str = "",
        source: str = "CardHawk OS",
    ):
        db.execute(
            """
            INSERT INTO genome_events (
                asset_id,
                event_type,
                event_note,
                previous_value,
                new_value,
                source,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                asset_id,
                event_type,
                event_note,
                previous_value,
                new_value,
                source,
                datetime.now().isoformat(),
            ),
        )

    @staticmethod
    def get_events(asset_id: int):
        return db.query(
            """
            SELECT *
            FROM genome_events
            WHERE asset_id = ?
            ORDER BY created_at DESC
            """,
            (asset_id,),
        )

    @staticmethod
    def get_recent(limit: int = 20):
        return db.query(
            """
            SELECT *
            FROM genome_events
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        )
