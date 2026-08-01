from __future__ import annotations

from collections import Counter
from typing import ClassVar

from .models import VocabularyTerm


class Engine:
    RESERVED_PLATFORM_NAMES: ClassVar[frozenset[str]] = frozenset(
        {
            "A•3ye",
            "THORᵡ",
            "Council",
            "Principle X",
            "Evidence Engine",
            "Knowledge Engine",
            "Reason Engine",
            "Memory Engine",
            "Predictive Engine",
            "Constitution",
            "Truth",
            "Balance Engine",
            "Gathering Mesh",
            "Temporal Graph",
        }
    )

    def validate(self, terms: tuple[VocabularyTerm, ...]) -> dict[str, object]:
        names = [term.name.casefold() for term in terms]
        duplicates = sorted(name for name, count in Counter(names).items() if count > 1)
        violations = [
            term.name
            for term in terms
            if term.name in self.RESERVED_PLATFORM_NAMES
            and term.tier != "PLATFORM_INTELLIGENCE_LANGUAGE"
        ]
        return {
            "valid": not duplicates and not violations,
            "duplicates": duplicates,
            "reservedNameViolations": violations,
            "termCount": len(terms),
        }
