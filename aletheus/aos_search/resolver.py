from __future__ import annotations

from .providers import provider_registry


class SearchResolver:
    GENESIS = "21.8"
    VERSION = "1.0.0"

    def resolve(self, execution_plan):
        resolved = []
        missing = []

        for provider_id in execution_plan.providers:
            provider = provider_registry.get(provider_id)

            if provider and provider.enabled:
                resolved.append(provider.to_dict())
            else:
                missing.append(provider_id)

        return {
            "plan": execution_plan.to_dict(),
            "resolved_providers": resolved,
            "missing_providers": missing,
            "ready": len(missing) == 0,
        }

    def health(self):
        return {
            "status": "healthy",
            "genesis": self.GENESIS,
            "version": self.VERSION,
        }


search_resolver = SearchResolver()
