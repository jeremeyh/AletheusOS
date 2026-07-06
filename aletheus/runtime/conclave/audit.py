import json
from datetime import datetime
from pathlib import Path


class ConclaveAuditLog:
    def __init__(self, root="."):
        self.root = Path(root).resolve()
        self.path = self.root / "reports" / "conclave" / "conclave_audit.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, event: dict):
        event = dict(event)
        event["timestamp"] = datetime.utcnow().isoformat()
        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event, sort_keys=True) + "\n")
