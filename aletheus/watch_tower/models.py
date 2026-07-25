from dataclasses import dataclass

from aletheus.time_utils import utc_now_iso


@dataclass
class IntegrityReport:
    passed: bool
    score: float
    summary: str
    created_at: str = utc_now_iso()
