from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class SentinelFinding:
    service: str
    status: str
    severity: str
    message: str
    created_at: str = ""

    def to_dict(self):
        data = asdict(self)
        if not data["created_at"]:
            data["created_at"] = datetime.utcnow().isoformat()
        return data
