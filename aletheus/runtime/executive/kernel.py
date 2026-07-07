from datetime import datetime, UTC

from .models import ExecutiveDecision, ExecutiveState


class ExecutiveKernel:
    """
    Executive Kernel™

    Lightweight coordination layer for AletheusOS runtime operations.

    It coordinates lifecycle, registry, service, mission, and governance
    concerns without owning their implementation.
    """

    def __init__(self):
        self.state = ExecutiveState()

    def decide(self, action: str, reason: str = "", metadata: dict | None = None):
        decision = ExecutiveDecision(
            action=action,
            status="accepted",
            reason=reason,
            metadata=metadata or {},
        )

        self.state.last_decision = decision
        self.state.updated_at = datetime.now(UTC).isoformat()

        return decision

    def activate_service(self, name: str):
        if name not in self.state.active_services:
            self.state.active_services.append(name)

        self.state.status = "active"
        self.state.updated_at = datetime.now(UTC).isoformat()

        return self.decide(
            action="activate_service",
            reason=f"Service '{name}' activated by Executive Kernel.",
            metadata={"service": name},
        )

    def register_mission(self, mission: str):
        if mission not in self.state.active_missions:
            self.state.active_missions.append(mission)

        self.state.updated_at = datetime.now(UTC).isoformat()

        return self.decide(
            action="register_mission",
            reason=f"Mission '{mission}' registered with Executive Kernel.",
            metadata={"mission": mission},
        )

    def health(self):
        return {
            "status": self.state.status,
            "active_services": list(self.state.active_services),
            "active_missions": list(self.state.active_missions),
            "last_decision": (
                self.state.last_decision.__dict__
                if self.state.last_decision
                else None
            ),
            "updated_at": self.state.updated_at,
        }
