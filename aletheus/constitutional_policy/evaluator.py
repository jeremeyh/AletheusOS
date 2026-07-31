from __future__ import annotations

from .models import ConstitutionalPolicy, PolicyEvaluationResult


class ConstitutionalPolicyEvaluator:
    GENESIS = "19.1"
    VERSION = "0.1.0"

    def evaluate(
        self,
        policy: ConstitutionalPolicy,
        evidence: dict,
    ) -> PolicyEvaluationResult:

        rule = policy.rule

        if rule == "minimum_confidence":
            confidence = float(evidence.get("confidence", 0))
            minimum = float(policy.metadata.get("minimum", 80))

            passed = confidence >= minimum

            return PolicyEvaluationResult(
                policy_id=policy.policy_id,
                passed=passed,
                reason=(
                    f"Confidence {confidence} meets minimum {minimum}."
                    if passed
                    else f"Confidence {confidence} is below minimum {minimum}."
                ),
                evidence=evidence,
            )

        if rule == "requires_consensus":
            consensus = bool(evidence.get("consensus", False))

            return PolicyEvaluationResult(
                policy_id=policy.policy_id,
                passed=consensus,
                reason=(
                    "Consensus is present." if consensus else "Consensus is missing."
                ),
                evidence=evidence,
            )

        if rule == "requires_principle_x":
            principle_x = bool(evidence.get("principle_x", False))

            return PolicyEvaluationResult(
                policy_id=policy.policy_id,
                passed=principle_x,
                reason=(
                    "Principle X authority is present."
                    if principle_x
                    else "Principle X authority is missing."
                ),
                evidence=evidence,
            )

        return PolicyEvaluationResult(
            policy_id=policy.policy_id,
            passed=False,
            reason=f"Unknown policy rule: {rule}",
            evidence=evidence,
        )


constitutional_policy_evaluator = ConstitutionalPolicyEvaluator()
