from dataclasses import dataclass
from datetime import datetime, UTC


@dataclass
class ReleaseCertification:
    approved: bool
    status: str
    health_score: float
    git_clean: bool
    summary: str
    created_at: str = datetime.now(UTC).isoformat()
