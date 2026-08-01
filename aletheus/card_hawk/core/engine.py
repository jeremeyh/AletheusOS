from __future__ import annotations

import hashlib
import json
from typing import Any

from .models import CardDetermination


class Engine:
    VERSION = "26.0.0"

    def envelope(self, determination: CardDetermination) -> dict[str, Any]:
        payload = {
            "runtime": "CARD_HAWK_A3YE",
            "version": self.VERSION,
            "asset": determination.asset.__dict__,
            "valuation": {
                "low": determination.fair_value_low,
                "mid": determination.fair_value_mid,
                "high": determination.fair_value_high,
            },
            "decision": determination.decision,
            "vector": determination.vector.__dict__,
            "disclosures": list(determination.disclosures),
            "minorityViews": list(determination.minority_views),
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        payload["signature"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return payload
