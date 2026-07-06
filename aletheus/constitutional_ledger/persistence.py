from __future__ import annotations

import json
from pathlib import Path


class ConstitutionalLedgerPersistence:
    GENESIS = "19.4"
    VERSION = "0.1.0"

    def save(self, entries: list[dict], path: str | Path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(entries, indent=2),
            encoding="utf-8",
        )
        return {
            "saved": True,
            "path": str(path),
            "entries": len(entries),
        }

    def load(self, path: str | Path):
        path = Path(path)

        if not path.exists():
            return []

        return json.loads(path.read_text(encoding="utf-8"))


constitutional_ledger_persistence = ConstitutionalLedgerPersistence()
