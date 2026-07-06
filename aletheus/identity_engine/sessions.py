from __future__ import annotations

from uuid import uuid4

from .models import IdentitySession


class SessionManager:

    GENESIS = "21.7"
    VERSION = "1.0.0"

    def __init__(self):
        self._sessions: dict[str, IdentitySession] = {}

    def create(
        self,
        identity_id: str,
    ) -> IdentitySession:

        session = IdentitySession(
            session_id=f"session.{uuid4().hex[:16]}",
            identity_id=identity_id,
            authenticated=True,
        )

        self._sessions[session.session_id] = session

        return session

    def get(
        self,
        session_id: str,
    ) -> IdentitySession | None:

        return self._sessions.get(session_id)

    def revoke(
        self,
        session_id: str,
    ) -> None:

        self._sessions.pop(session_id, None)

    def active_sessions(self):

        return list(self._sessions.values())

    def statistics(self):

        return {
            "sessions": len(self._sessions),
            "genesis": self.GENESIS,
            "version": self.VERSION,
        }

    def health(self):

        return {
            "status": "healthy",
            **self.statistics(),
        }


session_manager = SessionManager()
