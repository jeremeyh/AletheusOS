from aletheus.time_utils import utc_now, utc_now_iso
from dataclasses import dataclass
from datetime import datetime
@dataclass
class IntegrityReport:
    passed: bool
    score: float
    summary: str
    created_at: str = utc_now_iso()
