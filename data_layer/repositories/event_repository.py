import json
from datetime import datetime

from data_layer.database_manager import db


class EventRepository:
    @staticmethod
    def emit(event_type, source, message, payload=None):
        db.execute(
            "INSERT INTO intelligence_events (event_type, source, message, payload, created_at) VALUES (?, ?, ?, ?, ?)",
            (event_type, source, message, json.dumps(payload or {}), datetime.utcnow().isoformat()),
        )

    @staticmethod
    def latest(limit=50):
        return db.query("SELECT * FROM intelligence_events ORDER BY event_id DESC LIMIT ?", (limit,))
