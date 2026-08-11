from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AssetNote:
    note: str
    category: str = "Founder"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class AssetNotes:
    """
    Founder Notes™

    Journal-style notes for acquisition thesis, seller interaction,
    inspection, grading, disposition, and future plans.
    """

    notes: list[AssetNote] = field(default_factory=list)

    def add(self, note: str, category: str = "Founder") -> AssetNote:
        item = AssetNote(note=note, category=category)
        self.notes.append(item)
        return item

    def all(self):
        return [note.__dict__ for note in self.notes]
