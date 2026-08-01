from __future__ import annotations

import hashlib
import json

from .models import ProjectionNode


class Engine:
    def envelope(self, root: ProjectionNode, thesis: str) -> dict[str, object]:
        payload = {
            "runtimeVersion": "24.0.0",
            "thesis": thesis,
            "rootProjection": root.to_dict(),
            "projectionNeutral": True,
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        payload["constitutionalSignature"] = hashlib.sha256(raw.encode()).hexdigest()
        return payload
