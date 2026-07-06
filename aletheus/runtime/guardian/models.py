from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class GuardianEvent:
    source: str
    action: str
    target: str = ""
    risk: str = "low"
    allowed: bool = True
    conclave_status: str = ""
    watch_tower_requested: bool = False
    principle_x_required: bool = False
    created_at: str = ""

    def to_dict(self):
        data = asdict(self)
        if not data["created_at"]:
            data["created_at"] = datetime.utcnow().isoformat()
        return data
