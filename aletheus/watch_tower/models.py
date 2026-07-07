from dataclasses import dataclass
from datetime import datetime
@dataclass
class IntegrityReport:
    passed: bool
    score: float
    summary: str
    created_at: str = datetime.utcnow().isoformat()
