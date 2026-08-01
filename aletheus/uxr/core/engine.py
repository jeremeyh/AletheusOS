from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .models import Experience


class Engine:
    def finalize(self, experience: Experience, output: Path) -> dict[str, object]:
        payload = experience.to_dict()
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        payload["constitutionalSignature"] = hashlib.sha256(
            canonical.encode()
        ).hexdigest()
        output.mkdir(parents=True, exist_ok=True)
        (output / "universal-experience-runtime.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8"
        )
        return payload
