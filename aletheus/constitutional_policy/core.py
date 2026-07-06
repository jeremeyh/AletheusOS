from __future__ import annotations

from .evaluator import constitutional_policy_evaluator
from .models import ConstitutionalPolicy
from .registry import ConstitutionalPolicyRegistry


class ConstitutionalPolicyEngine:
    GENESIS = "19.1"
    VERSION = "0.1.0"

    def __init__(self):
        self.registry = ConstitutionalPolicyRegistry()
        self._bootstrapped = False

    def bootstrap_defaults(self):
        if self._bootstrapped:
            return self.statistics()

        defaults = [
            ConstitutionalPolicy(
                policy_id="policy.minimum_confidence",
                name="Minimum Confidence Policy",
                rule="minimum_confidence",
                description="Requires constitutional decisions to meet a minimum confidence threshold.",
                metadata={"minimum": 80},
            ),
            ConstitutionalPolicy(
                policy_id="policy.requires_consensus",
                name="Council Consensus Required",
                rule="requires_consensus",
                description="Requires a Council consensus result before constitutional approval.",
            ),
            ConstitutionalPolicy(
                policy_id="policy.requires_principle_x",
                name="Principle X Authority Required",
                rule="requires_principle_x",
                description="Requires Principle X authority for constitutional decisions.",
            ),
        ]

        for policy in defaults:
            self.registry.register(policy)

        self._bootstrapped = True
        return self.statistics()

    def evaluate(self, evidence: dict):
        self.bootstrap_defaults()

        results = [
            constitutional_policy_evaluator.evaluate(
                policy,
                evidence,
            ).to_dict()
            for policy in self.registry.enabled()
        ]

        passed = all(result["passed"] for result in results)

        return {
            "passed": passed,
            "results": results,
        }

    def health(self):
        return {
            "name": "Constitutional Policy Engine",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "bootstrapped": self._bootstrapped,
            "policies": self.registry.count(),
        }

    def statistics(self):
        return {
            "name": "Constitutional Policy Engine",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            **self.registry.statistics(),
        }


constitutional_policy_engine = ConstitutionalPolicyEngine()
