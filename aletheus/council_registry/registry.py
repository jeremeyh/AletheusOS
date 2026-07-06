from __future__ import annotations

from .models import CouncilMember


class CouncilRegistry:
    GENESIS = "16.6"
    VERSION = "0.1.0"

    def __init__(self):
        self._members: dict[str, CouncilMember] = {}

    def register(self, member: CouncilMember):
        self._members[member.member_id] = member
        return member

    def get(self, member_id: str):
        return self._members.get(member_id)

    def list(self):
        return [member.to_dict() for member in self._members.values()]

    def count(self):
        return len(self._members)

    def health(self):
        return {
            "name": "Council Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "members": self.count(),
        }

    def statistics(self):
        return {
            "members": self.count(),
            "member_ids": sorted(self._members.keys()),
        }
