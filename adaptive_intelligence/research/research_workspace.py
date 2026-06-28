from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class ResearchNote:
    research_type: str
    title: str
    body: str = ""
    subject: str = ""
    evidence: str = ""
    status: str = "active"
    note_id: str = field(default_factory=lambda: f"RS-{uuid.uuid4().hex[:10].upper()}")
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

class ResearchWorkspace:
    """7.0E — Research Workspace™."""
    _notes = []

    @classmethod
    def create(cls, research_type, title, body="", subject="", evidence="", status="active"):
        note = ResearchNote(research_type, title, body, subject, evidence, status)
        cls._notes.append(note)
        return note

    @classmethod
    def all(cls, research_type=None):
        if research_type:
            return [n for n in cls._notes if n.research_type == research_type]
        return cls._notes

    @classmethod
    def seed(cls):
        if not cls._notes:
            cls.create("Player Dossier", "Core prospect thesis", "Track player development, market pricing, and scarcity.")
            cls.create("Parallel Study", "Gold /10 premium thesis", "Gold /10 remains a high-conviction scarcity lane.")
        return cls._notes
