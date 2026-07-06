from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class WatchTowerFinding:
    code: str
    severity: str
    title: str
    message: str
    path: str = ""
    repairable: bool = False
    created_at: str = ""

    def to_dict(self):
        data = asdict(self)
        if not data["created_at"]:
            data["created_at"] = datetime.utcnow().isoformat()
        return data
