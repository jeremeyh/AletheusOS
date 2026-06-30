from __future__ import annotations

from typing import Any, Dict, List

from aletheus.semantic.models import SemanticAssertion, SemanticConcept


class AletheusSemanticCore:
    def __init__(self) -> None:
        self.version = "1.1.0"
        self.concepts: List[SemanticConcept] = []
        self.assertions: List[SemanticAssertion] = []

    def create_concept(
        self,
        name: str,
        concept_type: str = "concept",
        description: str = "",
        aliases: List[str] | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> SemanticConcept:
        existing = self.find_concept_exact(name)
        if existing:
            return existing

        concept = SemanticConcept(
            name=name,
            concept_type=concept_type,
            description=description,
            aliases=aliases or [],
            metadata=metadata or {},
        )
        self.concepts.append(concept)
        return concept

    def find_concept_exact(self, name: str) -> SemanticConcept | None:
        needle = name.lower()
        for concept in self.concepts:
            names = [concept.name.lower()] + [alias.lower() for alias in concept.aliases]
            if needle in names:
                return concept
        return None

    def search_concepts(self, query: str = "", concept_type: str = "") -> List[Dict[str, Any]]:
        results = self.concepts

        if query:
            needle = query.lower()
            results = [
                concept for concept in results
                if needle in concept.name.lower()
                or needle in concept.description.lower()
                or any(needle in alias.lower() for alias in concept.aliases)
            ]

        if concept_type:
            results = [concept for concept in results if concept.concept_type == concept_type]

        return [concept.to_dict() for concept in results]

    def assert_fact(
        self,
        subject: str,
        predicate: str,
        object_value: str,
        confidence: float = 0.75,
        source: str = "aletheus",
        metadata: Dict[str, Any] | None = None,
    ) -> SemanticAssertion:
        assertion = SemanticAssertion(
            subject=subject,
            predicate=predicate,
            object_value=object_value,
            confidence=confidence,
            source=source,
            metadata=metadata or {},
        )
        self.assertions.append(assertion)
        return assertion

    def query_assertions(
        self,
        subject: str = "",
        predicate: str = "",
        object_value: str = "",
    ) -> List[Dict[str, Any]]:
        results = self.assertions

        if subject:
            results = [item for item in results if item.subject.lower() == subject.lower()]

        if predicate:
            results = [item for item in results if item.predicate.lower() == predicate.lower()]

        if object_value:
            results = [item for item in results if item.object_value.lower() == object_value.lower()]

        return [item.to_dict() for item in results]

    def explain_concept(self, name: str) -> Dict[str, Any]:
        concept = self.find_concept_exact(name)
        related_assertions = [
            item.to_dict()
            for item in self.assertions
            if item.subject.lower() == name.lower()
            or item.object_value.lower() == name.lower()
        ]

        return {
            "concept": concept.to_dict() if concept else None,
            "assertions": related_assertions,
            "relationship_count": len(related_assertions),
        }

    def bootstrap_cardhawk_semantics(self) -> Dict[str, Any]:
        concepts = [
            ("Card Hawk Foundation™", "application", "Flagship reference application running on Aletheus."),
            ("Aletheus™", "operating_system", "Universal Intelligence Operating System."),
            ("Asset Vault", "service", "Canonical collectible asset registry."),
            ("Portfolio Engine", "service", "Portfolio value and allocation intelligence."),
            ("Marketplace Intelligence", "service", "Market signal, comps, and opportunity detection."),
            ("THORᵡ", "engine", "Trading Heuristic Opportunity Rating."),
            ("DEF", "engine", "Decision Engine Framework."),
            ("Hawk A•Eye™", "engine", "Visual intelligence and recognition engine."),
        ]

        created = [
            self.create_concept(name, concept_type, description).to_dict()
            for name, concept_type, description in concepts
        ]

        assertions = [
            self.assert_fact("Card Hawk Foundation™", "runs_on", "Aletheus™", 0.99, "bootstrap").to_dict(),
            self.assert_fact("Card Hawk Foundation™", "uses", "Asset Vault", 0.95, "bootstrap").to_dict(),
            self.assert_fact("Card Hawk Foundation™", "uses", "Portfolio Engine", 0.95, "bootstrap").to_dict(),
            self.assert_fact("Card Hawk Foundation™", "uses", "Marketplace Intelligence", 0.95, "bootstrap").to_dict(),
            self.assert_fact("THORᵡ", "supports", "Marketplace Intelligence", 0.9, "bootstrap").to_dict(),
            self.assert_fact("DEF", "supports", "Card Hawk Foundation™", 0.9, "bootstrap").to_dict(),
        ]

        return {"concepts": created, "assertions": assertions}

    def stats(self) -> Dict[str, Any]:
        by_type: Dict[str, int] = {}

        for concept in self.concepts:
            by_type[concept.concept_type] = by_type.get(concept.concept_type, 0) + 1

        return {
            "version": self.version,
            "concepts": len(self.concepts),
            "assertions": len(self.assertions),
            "concepts_by_type": by_type,
        }


semantic_core = AletheusSemanticCore()
