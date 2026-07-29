from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .boot_phase import BootPhase


@dataclass(slots=True)
class BootContext:
    runtime: Any
    phase: BootPhase = BootPhase.CREATED
    instances: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    trace: list[dict[str, Any]] = field(default_factory=list)

    def transition(
        self,
        phase: BootPhase,
        detail: str = "",
    ) -> None:
        self.phase = phase
        self.trace.append(
            {
                "phase": phase.value,
                "detail": detail,
            }
        )

    def fail(self, error: Exception | str) -> None:
        self.errors.append(str(error))
        self.transition(BootPhase.FAILED, str(error))
