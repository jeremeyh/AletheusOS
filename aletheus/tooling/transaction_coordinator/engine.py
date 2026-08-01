from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class Transaction:
    transaction_id: str
    releases: list[str]
    status: str = "planned"
    checkpoints: list[dict[str, Any]] = field(default_factory=list)


class Engine:
    def __init__(self, output: Path) -> None:
        self.output = output

    def begin(self, transaction_id: str, releases: list[str]) -> Transaction:
        return Transaction(transaction_id=transaction_id, releases=releases)

    def checkpoint(self, transaction: Transaction, release: str, commit: str) -> None:
        transaction.checkpoints.append({"release": release, "commit": commit})
        transaction.status = "in_progress"

    def commit(self, transaction: Transaction) -> dict[str, Any]:
        transaction.status = "committed"
        report = {
            "transaction_id": transaction.transaction_id,
            "releases": transaction.releases,
            "checkpoints": transaction.checkpoints,
            "status": transaction.status,
            "rollback_mode": "all_or_nothing",
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "transaction-coordinator.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
