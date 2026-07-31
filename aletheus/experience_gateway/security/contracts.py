from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Protocol

PrincipalRole = Literal[
    "viewer",
    "operator",
    "administrator",
    "platform_architect",
]

PolicyOutcome = Literal[
    "allow",
    "deny",
]


@dataclass(frozen=True, slots=True)
class Principal:
    subject_id: str
    display_name: str
    roles: tuple[PrincipalRole, ...]
    entitlements: tuple[str, ...] = ()
    authentication_method: str = "local"
    authenticated: bool = True
    attributes: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.subject_id.strip():
            raise ValueError("Principal subject_id cannot be empty.")

        if not self.display_name.strip():
            raise ValueError("Principal display_name cannot be empty.")

        if not self.roles:
            raise ValueError("Principal must have at least one role.")


@dataclass(frozen=True, slots=True)
class AuthorizationDecision:
    outcome: PolicyOutcome
    reason: str
    policy_id: str
    principal_id: str
    command_id: str
    matched_roles: tuple[PrincipalRole, ...] = ()
    matched_entitlements: tuple[str, ...] = ()

    @property
    def allowed(self) -> bool:
        return self.outcome == "allow"


class AuthorizationPolicy(Protocol):
    def evaluate(
        self,
        *,
        principal: Principal,
        command_id: str,
        command_risk: str,
        required_entitlements: tuple[str, ...],
    ) -> AuthorizationDecision: ...
