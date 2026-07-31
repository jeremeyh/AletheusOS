from __future__ import annotations

from typing import Any


class ArchitectureGovernanceRules:
    def __init__(self, runtime):

        self.runtime = runtime

        self.version = "1.0.0"

    def evaluate(self) -> dict[str, Any]:

        rules = {
            "commands_have_handlers": self.commands_have_handlers(),
            "domains_registered": self.domains_registered(),
            "registry_healthy": self.registry_healthy(),
            "architecture_validator_healthy": self.validator_healthy(),
        }

        violations = [name for name, result in rules.items() if not result]

        return {
            "engine": "Architecture Governance Rules Engine",
            "version": self.version,
            "compliant": len(violations) == 0,
            "rules": rules,
            "violations": violations,
        }

    def commands_have_handlers(self):

        try:
            audit = self.runtime.command_surface_audit()

            return audit.get("failed_commands", 1) == 0

        except Exception:
            return False

    def domains_registered(self):

        try:
            registry = self.runtime.registry_snapshot()

            return registry.get("domain_count", 0) > 0

        except Exception:
            return False

    def registry_healthy(self):

        try:
            return self.runtime.registry_snapshot().get("healthy", False)

        except Exception:
            return False

    def validator_healthy(self):

        try:
            result = self.runtime.architecture_validate()

            return result.get("healthy", False)

        except Exception:
            return False
