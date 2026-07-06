from __future__ import annotations

from aletheus.platform_subscriptions import platform_subscriptions

from .monitor import runtime_supervisor_monitor
from .policies import runtime_supervisor_policy
from .recovery import runtime_recovery


class RuntimeSupervisor:
    GENESIS = "16.1"
    VERSION = "0.1.0"

    WATCHED_EVENTS = [
        "platform.booting",
        "platform.online",
        "platform.degraded",
        "platform.shutdown",
        "application.started",
        "application.stopped",
        "application.failed",
        "component.failed",
    ]

    def __init__(self):
        self.observations = []
        self.decisions = []
        self.recovery_results = []
        self.registered = False

    def handle_event(self, event):
        observation = runtime_supervisor_monitor.observe(event)
        decision = runtime_supervisor_policy.evaluate(observation)
        recovery = runtime_recovery.execute(decision)

        self.observations.append(observation.to_dict())
        self.decisions.append(decision.to_dict())
        self.recovery_results.append(recovery)

        return {
            "observation": observation.to_dict(),
            "decision": decision.to_dict(),
            "recovery": recovery,
        }

    def register(self):
        if self.registered:
            return {
                "registered": True,
                "subscriptions": len(self.WATCHED_EVENTS),
                "message": "Runtime Supervisor already registered.",
            }

        for event_type in self.WATCHED_EVENTS:
            platform_subscriptions.subscribe(
                event_type,
                "runtime_supervisor",
                self.handle_event,
            )

        self.registered = True

        return {
            "registered": True,
            "subscriptions": len(self.WATCHED_EVENTS),
        }

    def health(self):
        return {
            "name": "Runtime Supervisor",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "registered": self.registered,
            "observations": len(self.observations),
            "decisions": len(self.decisions),
            "recovery_results": len(self.recovery_results),
        }

    def statistics(self):
        return {
            "observations": len(self.observations),
            "decisions": len(self.decisions),
            "recovery_results": len(self.recovery_results),
            "watched_events": self.WATCHED_EVENTS,
        }


runtime_supervisor = RuntimeSupervisor()
