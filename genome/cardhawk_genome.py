import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class GenomeRecord:
    subject_id: str
    event_type: str
    description: str
    payload: dict = field(default_factory=dict)
    genome_id: str = field(
        default_factory=lambda: f"GEN-{uuid.uuid4().hex[:10].upper()}"
    )
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class CardHawkGenome:
    """CardHawk Genome™ lifecycle memory."""

    _records = []

    @classmethod
    def record(cls, subject_id, event_type, description, payload=None):
        rec = GenomeRecord(subject_id, event_type, description, payload or {})
        cls._records.append(rec)
        return rec

    @classmethod
    def for_subject(cls, subject_id):
        return [r for r in cls._records if r.subject_id == subject_id]

    @classmethod
    def latest(cls, limit=50):
        return cls._records[-limit:]
