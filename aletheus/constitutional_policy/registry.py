from __future__ import annotations

from .models import ConstitutionalPolicy


class ConstitutionalPolicyRegistry:
    GENESIS = "19.1"
    VERSION = "0.1.0"

    def __init__(self):
        self._policies: dict[str, ConstitutionalPolicy] = {}

    def register(self, policy: ConstitutionalPolicy):
        self._policies[policy.policy_id] = policy
        return policy

    def get(self, policy_id: str):
        return self._policies.get(policy_id)

    def list(self):
        return [policy.to_dict() for policy in self._policies.values()]

    def enabled(self):
        return [policy for policy in self._policies.values() if policy.enabled]

    def count(self):
        return len(self._policies)

    def statistics(self):
        return {
            "policies": self.count(),
            "policy_ids": sorted(self._policies.keys()),
        }
