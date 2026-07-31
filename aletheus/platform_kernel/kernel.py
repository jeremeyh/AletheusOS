from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from aletheus.capabilities import (
    CapabilityHost,
    RuntimeCapability,
)
from aletheus.executive_kernel import ExecutiveKernel
from aletheus.runtime.adapter import DefaultRuntimeAdapter


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class PlatformKernelStatus:
    """
    High-level platform status.

    This is intentionally small. Detailed runtime, executive, and
    capability status belongs to their respective subsystems.
    """

    status: str
    message: str
    runtime_attached: bool
    executive_online: bool
    installed_capabilities: int
    generated_at: str = field(default_factory=utc_now)


class PlatformKernel:
    """
    AletheusOS Platform Kernel

    Coordinates the major platform subsystems:

    - Executive Kernel
    - Runtime Adapter
    - Capability Host

    It does not replace runtime/core.py.
    It does not execute business logic.
    It does not know product-specific capabilities like Card Hawk internals.
    """

    def __init__(
        self,
        runtime: Any | None = None,
        executive_kernel: ExecutiveKernel | None = None,
        capability_host: CapabilityHost | None = None,
    ) -> None:
        self.runtime = runtime
        self.runtime_adapter = (
            DefaultRuntimeAdapter(runtime) if runtime is not None else None
        )
        self.executive_kernel = executive_kernel or ExecutiveKernel()
        self.capability_host = capability_host or CapabilityHost()
        self.boot_events: list[dict] = []

    # ---------------------------------------------------------
    # Boot / Attachment
    # ---------------------------------------------------------

    def attach_runtime(
        self,
        runtime: Any,
    ) -> None:
        self.runtime = runtime
        self.runtime_adapter = DefaultRuntimeAdapter(runtime)
        self.executive_kernel.attach_runtime(runtime)

        self.boot_events.append(
            {
                "event": "runtime_attached",
                "timestamp": utc_now(),
            }
        )

    def boot(self) -> None:
        """
        Boot the platform kernel.

        v1 is intentionally non-invasive. It does not boot runtime/core.py.
        It only records platform readiness around already-created subsystems.
        """

        self.boot_events.append(
            {
                "event": "platform_kernel_booted",
                "timestamp": utc_now(),
            }
        )

    # ---------------------------------------------------------
    # Capability Hosting
    # ---------------------------------------------------------

    def install_capability(
        self,
        capability: RuntimeCapability,
    ) -> None:
        self.capability_host.install(
            capability=capability,
            runtime=self.runtime,
        )

        self.boot_events.append(
            {
                "event": "capability_installed",
                "capability_id": capability.metadata().capability_id,
                "timestamp": utc_now(),
            }
        )

    def start_capabilities(self) -> None:
        self.capability_host.start_all()

    def stop_capabilities(self) -> None:
        self.capability_host.stop_all()

    # ---------------------------------------------------------
    # Status / Summary
    # ---------------------------------------------------------

    def status(self) -> PlatformKernelStatus:
        executive_status = self.executive_kernel.status()

        return PlatformKernelStatus(
            status="online",
            message="Platform Kernel online.",
            runtime_attached=self.runtime is not None,
            executive_online=executive_status.status == "online",
            installed_capabilities=len(self.capability_host.all()),
        )

    def summary(self) -> dict:
        status = self.status()

        return {
            "kernel": "Platform Kernel",
            "status": status.status,
            "message": status.message,
            "runtime_attached": status.runtime_attached,
            "executive_online": status.executive_online,
            "runtime": (
                self.runtime_adapter.boot_summary()
                if self.runtime_adapter is not None
                else {
                    "status": "unattached",
                }
            ),
            "executive": self.executive_kernel.boot_summary(),
            "capabilities": self.capability_host.summary(),
            "boot_events": self.boot_events,
            "generated_at": status.generated_at,
        }
