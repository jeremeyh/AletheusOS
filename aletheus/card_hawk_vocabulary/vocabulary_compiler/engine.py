from __future__ import annotations

from typing import Any

from .models import CapabilityMapping, VocabularyTerm


class Engine:
    def compile(
        self,
        *,
        application: str,
        terms: tuple[VocabularyTerm, ...],
        mappings: tuple[CapabilityMapping, ...],
    ) -> dict[str, Any]:
        if application != "CARD_HAWK":
            raise ValueError("Genesis 27 compiler is scoped to CARD_HAWK")

        mapped_names = {mapping.experience_name for mapping in mappings}
        term_names = {term.name for term in terms}
        unresolved = sorted(mapped_names.difference(term_names))

        return {
            "application": application,
            "experienceVocabulary": [
                {
                    "name": term.name,
                    "meaning": term.meaning,
                    "family": term.domain_family,
                    "tier": term.tier,
                }
                for term in sorted(terms, key=lambda item: item.name)
            ],
            "semanticMappings": [
                {
                    "platformCapability": mapping.platform_capability,
                    "applicationCapability": mapping.application_capability,
                    "experienceName": mapping.experience_name,
                    "semanticContract": mapping.semantic_contract,
                }
                for mapping in mappings
            ],
            "unresolvedMappings": unresolved,
            "valid": not unresolved,
            "nimbleReady": True,
            "uxrReady": True,
            "axiomUXReady": True,
        }
