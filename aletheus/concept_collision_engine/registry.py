from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from .models import ConceptSignature


class ConceptCollisionRegistry:
    """In-memory concept registry used by the collision engine."""

    def __init__(self) -> None:
        self._concepts: Dict[str, ConceptSignature] = {}

    def register(self, concept: ConceptSignature) -> None:
        key = concept.name.lower()
        self._concepts[key] = concept

    def get(self, name: str) -> Optional[ConceptSignature]:
        return self._concepts.get(name.lower())

    def all(self) -> List[ConceptSignature]:
        return list(self._concepts.values())

    def load_many(self, concepts: Iterable[ConceptSignature]) -> None:
        for concept in concepts:
            self.register(concept)
