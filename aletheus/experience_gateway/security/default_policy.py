from __future__ import annotations

from dataclasses import dataclass

from .contracts import (
    AuthorizationDecision,
    Principal,
    PrincipalRole,
)

ROLE_RANK: dict[PrincipalRole, int] = {
    "viewer": 10,
    "operator": 20,
    "administrator": 30,
    "platform_architect": 40,
}

MINIMUM_ROLE_BY_RISK: dict[str, PrincipalRole] = {
    "read_only": "viewer",
    "low": "operator",
    "moderate": "administrator",
    "high": "platform_architect",
}


@dataclass(frozen=True, slots=True)
class DefaultAuthorizationPolicy:
    policy_id: str = "aletheus.command-policy.v0.1"

    def evaluate(
        self,
        *,
        principal: Principal,
        command_id: str,
        command_risk: str,
        required_entitlements: tuple[str, ...],
    ) -> AuthorizationDecision:
        if not principal.authenticated:
            return AuthorizationDecision(
                outcome="deny",
                reason="Principal is not authenticated.",
                policy_id=self.policy_id,
                principal_id=principal.subject_id,
                command_id=command_id,
            )

        minimum_role = MINIMUM_ROLE_BY_RISK.get(
            command_risk
        )

        if minimum_role is None:
            return AuthorizationDecision(
                outcome="deny",
                reason=(
                    "Command risk is not recognized by "
                    "the authorization policy."
                ),
                policy_id=self.policy_id,
                principal_id=principal.subject_id,
                command_id=command_id,
            )

        principal_rank = max(
            ROLE_RANK[role]
            for role in principal.roles
        )

        required_rank = ROLE_RANK[
            minimum_role
        ]

        matched_roles = tuple(
            role
            for role in principal.roles
            if ROLE_RANK[role] >= required_rank
        )

        if principal_rank < required_rank:
            return AuthorizationDecision(
                outcome="deny",
                reason=(
                    f"Command risk '{command_risk}' requires "
                    f"role '{minimum_role}' or higher."
                ),
                policy_id=self.policy_id,
                principal_id=principal.subject_id,
                command_id=command_id,
                matched_roles=matched_roles,
            )

        missing_entitlements = tuple(
            entitlement
            for entitlement in required_entitlements
            if entitlement not in principal.entitlements
        )

        if missing_entitlements:
            return AuthorizationDecision(
                outcome="deny",
                reason=(
                    "Principal lacks required entitlement(s): "
                    + ", ".join(missing_entitlements)
                ),
                policy_id=self.policy_id,
                principal_id=principal.subject_id,
                command_id=command_id,
                matched_roles=matched_roles,
            )

        return AuthorizationDecision(
            outcome="allow",
            reason=(
                "Principal role and entitlements satisfy "
                "the command policy."
            ),
            policy_id=self.policy_id,
            principal_id=principal.subject_id,
            command_id=command_id,
            matched_roles=matched_roles,
            matched_entitlements=required_entitlements,
        )


def create_default_authorization_policy(
) -> DefaultAuthorizationPolicy:
    return DefaultAuthorizationPolicy()
