from __future__ import annotations

import hashlib
import json


class Engine:
    def commit(self, event: dict[str, object]) -> dict[str, str]:
        raw = json.dumps(event, sort_keys=True, separators=(",", ":"))
        return {
            "eventHash": hashlib.sha256(raw.encode()).hexdigest(),
            "status": "APPEND_ONLY_COMMITMENT_CREATED",
        }
