from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ExecutiveKernelStatus:
    status: str
    message: str
    runtime_attached: bool
    generated_at: str = field(default_factory=utc_now)


class ExecutiveKernel:
    """
    AletheusOS Executive Kernel

    The Executive Kernel is the constitutional orchestration layer
    above the runtime kernel.

    It does not replace runtime/core.py.

    It coordinates:
    - runtime attachment
    - platform boot posture
    - constitutional orchestration
    - high-level platform status
    """

    def __init__(self) -> None:
        self.runtime: Any | None = None
        self.boot_events: List[Dict[str, Any]] = []

    def attach_runtime(self, runtime: Any) -> None:
        self.runtime = runtime
        self.boot_events.append(
            {
                "event": "runtime_attached",
                "timestamp": utc_now(),
            }
        )

    def status(self) -> ExecutiveKernelStatus:
        return ExecutiveKernelStatus(
            status="online" if self.runtime else "initializing",
            message=(
                "Executive Kernel online."
                if self.runtime
                else "Executive Kernel awaiting runtime attachment."
            ),
            runtime_attached=self.runtime is not None,
        )

    def boot_summary(self) -> dict:
        status = self.status()

        return {
            "kernel": "Executive Kernel",
            "status": status.status,
            "message": status.message,
            "runtime_attached": status.runtime_attached,
            "boot_events": self.boot_events,
            "generated_at": status.generated_at,
        }
