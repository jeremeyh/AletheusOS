from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(frozen=True,slots=True)
class Identity:
    name:str
    kind:str
    version:str="1.0"
    id:UUID=field(default_factory=uuid4)
    created_at:datetime=field(default_factory=lambda:datetime.now(UTC))
    def __post_init__(self):
        if not self.name.strip(): raise ValueError("Identity name cannot be empty.")
        if not self.kind.strip(): raise ValueError("Identity kind cannot be empty.")
