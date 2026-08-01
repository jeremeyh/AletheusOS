from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Invariant:
    invariant_id: str
    field: str
    operator: str
    expected: Any


class Engine:
    def evaluate(
        self, payload: dict[str, Any], invariants: tuple[Invariant, ...]
    ) -> dict[str, object]:
        failures: list[str] = []
        for rule in invariants:
            actual = payload.get(rule.field)
            if (
                rule.operator == "equals"
                and actual != rule.expected
                or rule.operator == "not_equals"
                and actual == rule.expected
                or rule.operator == "present"
                and rule.field not in payload
            ):
                failures.append(rule.invariant_id)
        return {
            "status": "PASSED" if not failures else "REJECTED",
            "failures": failures,
            "executionAllowed": not failures,
        }
