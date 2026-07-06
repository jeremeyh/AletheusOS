from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .audit import ConclaveAuditLog
from .decoy import ConclaveDecoy
from .policy import ConclavePolicy
from .shield import ConclaveShield


class ConclaveEngine:
    """
    Conclave™
    Defensive containment, decoy, and preservation layer for AletheusOS.

    Conclave does not attack back.
    It shields, blocks, logs, decoys, and requests integrity checks.
    """

    VERSION = "1.0.0"

    def __init__(self, root="."):
        self.root = Path(root).resolve()
        self.policy = ConclavePolicy()
        self.audit = ConclaveAuditLog(self.root)
        self.decoy = ConclaveDecoy()
        self.shield = ConclaveShield(self.root, self.policy.protected_paths)

    def inspect(self, action: str, target: str = "", source: str = "unknown") -> dict:
        classification = self.shield.classify_action(action, target)
        risk = self._risk(action, target, classification)

        decision = {
            "conclave": {
                "version": self.VERSION,
                "timestamp": datetime.utcnow().isoformat(),
                "source": source,
                "action": action,
                "target": target,
                "classification": classification,
                "risk": risk,
                "allowed": risk not in {"critical", "high"},
                "response": self._response_for(risk),
                "principle_x": risk in {"critical", "high"},
                "watch_tower_requested": risk in {"critical", "high", "medium"},
            }
        }

        self.audit.write(decision["conclave"])
        return decision

    def protect(self, action: str, target: str = "", source: str = "unknown") -> dict:
        decision = self.inspect(action, target, source)
        conclave = decision["conclave"]

        if not conclave["allowed"]:
            conclave["shield_engaged"] = True
            conclave["decoy"] = self.decoy.blank()
        else:
            conclave["shield_engaged"] = False
            conclave["decoy"] = None

        self.audit.write(conclave)
        return decision

    def emergency_lockdown(self, reason: str = "manual") -> dict:
        event = {
            "conclave": {
                "version": self.VERSION,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "lockdown",
                "reason": reason,
                "protected_paths": self.policy.protected_paths,
                "principle_x": True,
                "watch_tower_requested": True,
                "message": "Conclave emergency lockdown engaged.",
            }
        }

        self.audit.write(event["conclave"])
        return event

    def _risk(self, action: str, target: str, classification: str) -> str:
        lowered = f"{action} {target}".lower()

        if classification == "blocked_protected_destructive":
            return "critical"

        if any(keyword in lowered for keyword in self.policy.destructive_keywords):
            return "high"

        if classification in {"suspicious_destructive", "protected_access"}:
            return "medium"

        return "low"

    def _response_for(self, risk: str) -> str:
        if risk == "critical":
            return "block, shield, decoy, audit, request Watch Tower scan, activate Principle X"
        if risk == "high":
            return "block, audit, decoy sensitive data, request Watch Tower scan"
        if risk == "medium":
            return "audit, monitor, request integrity review"
        return "allow and log"
