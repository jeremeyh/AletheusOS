from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from aletheus.time_utils import utc_now_iso


def now() -> str:
    return utc_now_iso()


@dataclass
class EnterprisePolicy:
    name: str
    description: str = ""
    scope: str = "enterprise"
    rules: list[str] = field(default_factory=list)
    status: str = "active"
    policy_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class EnterpriseTeam:
    name: str
    description: str = ""
    members: list[str] = field(default_factory=list)
    team_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class EnterpriseDepartment:
    name: str
    description: str = ""
    teams: list[EnterpriseTeam] = field(default_factory=list)
    department_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        data = self.__dict__.copy()
        data["teams"] = [team.to_dict() for team in self.teams]
        return data


@dataclass
class EnterpriseOrganization:
    name: str
    description: str = ""
    departments: list[EnterpriseDepartment] = field(default_factory=list)
    policies: list[EnterprisePolicy] = field(default_factory=list)
    applications: list[str] = field(default_factory=list)
    status: str = "active"
    organization_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        data = self.__dict__.copy()
        data["departments"] = [department.to_dict() for department in self.departments]
        data["policies"] = [policy.to_dict() for policy in self.policies]
        return data


@dataclass
class AuditRecord:
    actor: str
    action: str
    target: str
    outcome: str = "recorded"
    metadata: dict[str, Any] = field(default_factory=dict)
    audit_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
