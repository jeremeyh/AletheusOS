from datetime import datetime
from pathlib import Path


class AuditLogger:
    """Audit trail logger."""

    LOG = Path("logs/audit.log")

    @classmethod
    def write(cls, actor, action, detail=""):
        cls.LOG.parent.mkdir(parents=True, exist_ok=True)
        line = f"{datetime.utcnow().isoformat()} | {actor} | {action} | {detail}\n"
        with cls.LOG.open("a", encoding="utf-8") as f:
            f.write(line)
        return line
