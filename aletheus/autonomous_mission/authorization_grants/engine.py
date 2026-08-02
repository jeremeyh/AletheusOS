from __future__ import annotations

from hashlib import sha256
from typing import Any, ClassVar

from .models import AuthorizationGrant, MissionSpec


class Engine:
    """Issues scoped, expiring, MFA-bound human execution grants."""

    VERSION: ClassVar[str] = "33.15.0"

    def issue(
        self,
        mission: MissionSpec,
        actor_id: str,
        scopes: tuple[str, ...],
        issued_at: int,
        expires_at: int,
        mfa_verified: bool,
    ) -> AuthorizationGrant:
        if not mfa_verified:
            raise ValueError("MFA verification is required.")
        if expires_at <= issued_at:
            raise ValueError("Grant expiry must follow issue time.")
        material = (
            f"{mission.mission_id}:{actor_id}:{scopes}:"
            f"{issued_at}:{expires_at}:{mfa_verified}"
        )
        signature = sha256(material.encode()).hexdigest()
        return AuthorizationGrant(
            grant_id=f"grant_{signature[:20]}",
            mission_id=mission.mission_id,
            actor_id=actor_id,
            scopes=scopes,
            issued_at=issued_at,
            expires_at=expires_at,
            mfa_verified=mfa_verified,
            signature=signature,
        )

    def evaluate(self, mission: MissionSpec) -> dict[str, Any]:
        grant = self.issue(
            mission,
            "human:demo",
            ("REVIEW",),
            0,
            60,
            True,
        )
        return {"grant": grant, "humanAuthority": "PRESERVED"}
