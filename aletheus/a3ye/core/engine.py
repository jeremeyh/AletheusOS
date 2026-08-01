from __future__ import annotations

import hashlib
import json
from typing import Any

from .models import A3yeResponse


class Engine:
    VERSION = "25.0.0"

    def envelope(self, response: A3yeResponse) -> dict[str, Any]:
        payload = {
            "engineVersion": self.VERSION,
            "designation": "A3YE",
            "role": "CONSTITUTIONAL_VOICE_OF_ALETHEUSOS",
            "thesis": response.thesis,
            "determination": response.determination.__dict__,
            "minorityOpinions": list(response.minority_opinions),
            "disclosures": list(response.disclosures),
            "projections": list(response.projections),
            "metadata": response.metadata,
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        payload["signature"] = hashlib.sha256(canonical.encode()).hexdigest()
        return payload
