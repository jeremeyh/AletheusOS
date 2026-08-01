from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path


class Engine:
    def certify(self, payload: dict[str, object], output: Path) -> dict[str, object]:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        signature = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        report = {
            "timestamp": datetime.now(UTC).isoformat(),
            "payload": payload,
            "signature": signature,
            "status": "certified",
        }

        output.mkdir(parents=True, exist_ok=True)

        (output / "continuous-certification.json").write_text(
            json.dumps(report, indent=2, sort_keys=True),
            encoding="utf-8",
        )

        return report
