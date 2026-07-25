from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True,slots=True)
class LearningRecord:
    subject:str
    content:dict[str,Any]
    correlation_id:UUID|None=None
    id:UUID=field(default_factory=uuid4)
    created_at:datetime=field(default_factory=lambda:datetime.now(UTC))
class InMemoryLearningStore:
    def __init__(self): self._records=[]
    def preserve(self,record): self._records.append(record)
    @property
    def records(self): return tuple(self._records)
