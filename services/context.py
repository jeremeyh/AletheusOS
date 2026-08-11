from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class PipelineContext:
    command: str
    payload: dict[str, Any] = field(default_factory=dict)
    founder: str = "Founder"
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)
    results: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def add_result(self, key: str, value: Any) -> None:
        self.results[key] = value

    def add_warning(self, warning: str) -> None:
        self.warnings.append(warning)

    def add_error(self, error: str) -> None:
        self.errors.append(error)

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "command": self.command,
            "founder": self.founder,
            "created_at": self.created_at,
            "payload": self.payload,
            "metadata": self.metadata,
            "results": self.results,
            "warnings": self.warnings,
            "errors": self.errors,
            "ok": self.ok,
        }
