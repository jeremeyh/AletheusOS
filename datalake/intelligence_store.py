from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class LakeRecord:
    record_type: str
    payload: dict
    source: str = "CardHawk OS™"
    record_id: str = field(default_factory=lambda: f"DL-{uuid.uuid4().hex[:10].upper()}")
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

class IntelligenceStore:
    """Data Lake Intelligence™ in-memory store for Alpha 1.0."""
    _records = []

    @classmethod
    def add(cls, record_type, payload, source="CardHawk OS™"):
        rec = LakeRecord(record_type, payload, source)
        cls._records.append(rec)
        return rec

    @classmethod
    def by_type(cls, record_type):
        return [r for r in cls._records if r.record_type == record_type]

    @classmethod
    def latest(cls, limit=50):
        return cls._records[-limit:]

    @classmethod
    def features(cls):
        counts = {}
        for rec in cls._records:
            counts[rec.record_type] = counts.get(rec.record_type, 0) + 1
        return counts
