from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from typing import Any

from aletheus.time_utils import utc_now, utc_now_iso


def utc_now():
    return utc_now_iso()


@dataclass
class SecurityRole:
    role_id: str
    name: str
    permissions: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)


@dataclass
class SecurityAudit:
    audit_id: str
    action: str
    actor: str
    status: str
    timestamp: str = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)


class AletheusSecurityEngine:
    VERSION = "3.7.0"

    def __init__(self):

        self.roles: dict[str, SecurityRole] = {}
        self.assignments: dict[str, str] = {}
        self.audit_log: list[SecurityAudit] = []
        self.policies: dict[str, Any] = {}

    @property
    def version(self):
        return self.VERSION

    def bootstrap(self):

        if "Administrator" not in self.roles:
            self.create_role(
                "Administrator",
                permissions=["*"],
            )

        return self.statistics()

    def authenticate(self, identity: str):

        return {
            "identity": identity,
            "authenticated": True,
        }

    def authorize(self, identity: str, permission: str):

        role = self.assignments.get(identity)

        if role is None:
            return {
                "authorized": False,
                "reason": "No role assigned",
            }

        permissions = self.roles[role].permissions

        return {
            "authorized": ("*" in permissions or permission in permissions),
            "role": role,
        }

    def create_role(self, name: str, permissions=None):

        role = SecurityRole(
            role_id=str(uuid.uuid4()),
            name=name,
            permissions=permissions or [],
        )

        self.roles[name] = role

        return asdict(role)

    def assign_role(self, identity: str, role: str):

        if role not in self.roles:
            return {"error": "Role not found"}

        self.assignments[identity] = role

        return {
            "identity": identity,
            "role": role,
        }

    def policy(self, name: str, definition=None):

        self.policies[name] = definition or {}

        return {
            "policy": name,
            "definition": self.policies[name],
        }

    def audit(self, action: str, actor: str, status="success", metadata=None):

        audit = SecurityAudit(
            audit_id=str(uuid.uuid4()),
            action=action,
            actor=actor,
            status=status,
            metadata=metadata or {},
        )

        self.audit_log.append(audit)

        return asdict(audit)

    def statistics(self):

        return {
            "version": self.VERSION,
            "roles": len(self.roles),
            "assignments": len(self.assignments),
            "policies": len(self.policies),
            "audits": len(self.audit_log),
            "health": "healthy",
        }


security_core = AletheusSecurityEngine()
