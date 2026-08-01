from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, rails: Path, claims: Path, output: Path) -> None:
        self.rails = rails
        self.claims = claims
        self.output = output

    def build(self) -> dict[str, Any]:
        rails = json.loads(self.rails.read_text(encoding="utf-8"))
        claims = json.loads(self.claims.read_text(encoding="utf-8"))
        report = {
            "flow_state": rails.get("flow_state"),
            "parallel_enabled": rails.get("parallel_in_out_enabled"),
            "claim_envelopes": claims.get("ambivalent_claim_count", 0),
            "envelope_policy": "authority_scope_plus_contract_plus_direction",
            "state": "enveloped",
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "flow-state-envelope.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
