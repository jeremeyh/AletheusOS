from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, output: Path) -> None:
        self.output = output

    def append(
        self,
        *,
        release: str,
        commit: str,
        installer: Path,
        certification: str,
        rollback_point: str,
        runtime_compatibility: str,
    ) -> dict[str, Any]:
        self.output.mkdir(parents=True, exist_ok=True)
        ledger = self.output / "installation-provenance-ledger.jsonl"
        installer_hash = hashlib.sha256(installer.read_bytes()).hexdigest()
        entry = {
            "release": release,
            "commit": commit,
            "installer_hash": installer_hash,
            "timestamp": datetime.now(UTC).isoformat(),
            "certification": certification,
            "rollback_point": rollback_point,
            "runtime_compatibility": runtime_compatibility,
        }
        with ledger.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(entry, sort_keys=True) + "\n")
        return entry
