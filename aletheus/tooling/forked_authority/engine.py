from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, claims: Path, envelope: Path, output: Path) -> None:
        self.claims = claims
        self.envelope = envelope
        self.output = output

    def build(self) -> dict[str, Any]:
        claims = json.loads(self.claims.read_text(encoding="utf-8"))
        envelope = json.loads(self.envelope.read_text(encoding="utf-8"))
        forks = []
        for item in claims.get("claim_envelopes", []):
            if not isinstance(item, dict):
                continue
            forks.append(
                {
                    "claim": item.get("claim"),
                    "branches": item.get("envelope", {}),
                    "fork_type": "bounded_authority_fork",
                    "rejoin_policy": "constitutional_consensus",
                }
            )
        report = {
            "forked_claims": forks,
            "fork_count": len(forks),
            "flow_state": envelope.get("state"),
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "forked-authority-resolution.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
