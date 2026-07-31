from __future__ import annotations


class RegistryGovernanceRules:
    VERSION = "1.0.0"

    def validate(self, runtime):

        violations = []

        registry = getattr(runtime, "registry", None)

        if registry is None:
            return {"compliant": False, "violations": ["registry_missing"]}

        snapshot = registry.snapshot()

        if snapshot.get("domain_count", 0) == 0:
            violations.append("no_domains_registered")

        for name, domain in registry.domains.items():
            if domain is None:
                violations.append(f"invalid_domain:{name}")

        return {
            "engine": "Registry Governance Rules",
            "version": self.VERSION,
            "compliant": len(violations) == 0,
            "violations": violations,
            "snapshot": snapshot,
        }
