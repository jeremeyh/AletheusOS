from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class ExperienceSession:
    session_id: str
    user_id: str
    experience_id: str
    state: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class Engine:
    def __init__(self):
        self._sessions = {}

    def create(self, *, session_id, user_id, experience_id):
        s = ExperienceSession(session_id, user_id, experience_id)
        self._sessions[session_id] = s
        return s

    def update(self, session_id, patch):
        self._sessions[session_id].state.update(patch)
        return self._sessions[session_id]

    def get(self, session_id):
        return self._sessions[session_id]
