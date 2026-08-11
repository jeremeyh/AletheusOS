from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class RuntimeContext:
    command: str
    payload: dict[str, Any] = field(default_factory=dict)
    application: str = "system"
    founder: str = "Founder"
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    results: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    trace: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_result(self, key: str, value: Any) -> None:
        self.results[key] = value

    def add_error(self, error: Any) -> None:
        self.errors.append(str(error))

    def add_trace(self, stage: str, detail: Any) -> None:
        self.trace.append(
            {
                "stage": stage,
                "detail": detail,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "command": self.command,
            "application": self.application,
            "founder": self.founder,
            "payload": self.payload,
            "created_at": self.created_at,
            "results": self.results,
            "errors": self.errors,
            "trace": self.trace,
            "metadata": self.metadata,
        }
