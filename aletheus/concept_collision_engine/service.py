from __future__ import annotations

from collections.abc import Iterable

from .engine import ConceptCollisionEngine
from .models import CollisionReport, ConceptSignature
from .registry import ConceptCollisionRegistry


class ConceptCollisionService:
    """
    Service facade for collision checks.

    Future integrations:
    - Repository DNA
    - Watch Tower
    - Atlas
    - Genesis preflight
    - Council review
    """

    authority = "Watch Tower™"
    family = "Platform Intelligence"
    knows = "concept collision and non-redundant evolution"

    def __init__(
        self,
        registry: ConceptCollisionRegistry | None = None,
        engine: ConceptCollisionEngine | None = None,
    ) -> None:
        self.registry = registry or ConceptCollisionRegistry()
        self.engine = engine or ConceptCollisionEngine()

    def register_concept(self, concept: ConceptSignature) -> None:
        self.registry.register(concept)

    def register_many(self, concepts: Iterable[ConceptSignature]) -> None:
        self.registry.load_many(concepts)

    def evaluate(self, candidate: ConceptSignature) -> CollisionReport:
        return self.engine.evaluate(candidate, self.registry.all())

    def preflight(self, candidate: ConceptSignature) -> bool:
        return self.evaluate(candidate).passed
