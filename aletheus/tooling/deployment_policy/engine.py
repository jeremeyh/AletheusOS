from __future__ import annotations

import json
from pathlib import Path
from typing import Any

POLICIES = {
    "development": {
        "require_ready": False,
        "allow_warn": True,
    },
    "staging": {
        "require_ready": True,
        "allow_warn": True,
    },
    "production": {
        "require_ready": True,
        "allow_warn": False,
    },
    "emergency": {
        "require_ready": False,
        "allow_warn": True,
    },
    "rollback": {
        "require_ready": False,
        "allow_warn": True,
    },
}


class Engine:
    def __init__(self, output: Path) -> None:
        self.output = output

    def evaluate(
        self,
        environment: str,
        certification: str,
    ) -> dict[str, Any]:
        policy = POLICIES[environment]
        allowed = (
            certification == "READY"
            or (certification == "WARN" and policy["allow_warn"])
            or not policy["require_ready"]
        )
        report = {
            "environment": environment,
            "certification": certification,
            "allowed": allowed,
            "policy": policy,
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "deployment-policy.json").write_text(
            json.dumps(report, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return report
