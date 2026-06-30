from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List
import uuid


def now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class EnterprisePolicy:
    name: str
    description: str = ""
    scope: str = "enterprise"
    rules: List[str] = field(default_factory=list)
    status: str = "active"
    policy_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class EnterpriseTeam:
    name: str
    description: str = ""
    members: List[str] = field(default_factory=list)
    team_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class EnterpriseDepartment:
    name: str
    description: str = ""
    teams: List[EnterpriseTeam] = field(default_factory=list)
    department_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
        data = self.__dict__.copy()
        data["teams"] = [team.to_dict() for team in self.teams]
        return data


@dataclass
class EnterpriseOrganization:
    name: str
    description: str = ""
    departments: List[EnterpriseDepartment] = field(default_factory=list)
    policies: List[EnterprisePolicy] = field(default_factory=list)
    applications: List[str] = field(default_factory=list)
    status: str = "active"
    organization_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
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
    metadata: Dict[str, Any] = field(default_factory=dict)
    audit_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__
