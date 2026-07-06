from __future__ import annotations

from datetime import UTC, datetime

from .models import CapabilityGrant


class GrantManager:

    GENESIS = "21.6"
    VERSION = "1.0.0"

    def __init__(self):
        self._grants: list[CapabilityGrant] = []

    def grant(
        self,
        identity_id: str,
        capability_id: str,
        granted_by: str = "system",
        reason: str = "",
        expires_at: str | None = None,
    ):

        grant = CapabilityGrant(
            identity_id=identity_id,
            capability_id=capability_id,
            granted_by=granted_by,
            reason=reason,
            expires_at=expires_at,
        )

        self._grants.append(grant)

        return grant

    def revoke(
        self,
        identity_id: str,
        capability_id: str,
    ):

        self._grants = [
            g
            for g in self._grants
            if not (
                g.identity_id == identity_id
                and g.capability_id == capability_id
            )
        ]

    def grants_for(self, identity_id: str):

        return [
            g
            for g in self._grants
            if g.identity_id == identity_id
        ]

    def has(
        self,
        identity_id: str,
        capability_id: str,
    ):

        return any(
            g.identity_id == identity_id
            and g.capability_id == capability_id
            for g in self._grants
        )

    def statistics(self):

        return {
            "grants": len(self._grants),
            "genesis": self.GENESIS,
            "version": self.VERSION,
        }

    def health(self):

        return {
            "status": "healthy",
            **self.statistics(),
        }


grant_manager = GrantManager()
