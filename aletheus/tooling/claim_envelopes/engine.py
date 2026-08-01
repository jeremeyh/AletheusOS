from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, catalog: Path, roots: Path, output: Path) -> None:
        self.catalog = catalog
        self.roots = roots
        self.output = output

    def build(self) -> dict[str, Any]:
        catalog = json.loads(self.catalog.read_text(encoding="utf-8"))
        roots = json.loads(self.roots.read_text(encoding="utf-8"))
        claims: dict[str, list[str]] = defaultdict(list)
        entries = [
            item for item in catalog.get("entries", []) if isinstance(item, dict)
        ]
        for item in entries:
            claim = str(item.get("authority", "")).strip().casefold()
            if claim:
                claims[claim].append(str(item.get("name")))

        envelopes = []
        for claim, owners in claims.items():
            if len(owners) < 2:
                continue
            envelopes.append(
                {
                    "claim": claim,
                    "owners": sorted(owners),
                    "resolution": "fork_by_scope",
                    "envelope": {
                        owner: f"{claim} within {owner} bounded authority"
                        for owner in sorted(owners)
                    },
                }
            )
        report = {
            "claim_envelopes": envelopes,
            "ambivalent_claim_count": len(envelopes),
            "root_resolution_count": roots.get("resolved_count", 0),
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "ambivalent-claim-envelopes.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
