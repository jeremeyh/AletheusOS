"""
Semantic Command Registration.

Binds semantic commands directly to the bounded AletheusSemanticCore.
"""

from __future__ import annotations

from typing import Any


def _serialize(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return value.to_dict()

    if hasattr(value, "__dict__"):
        return dict(value.__dict__)

    return value


def register_semantic_commands(runtime):
    commands = runtime.commands
    semantic = runtime.semantic

    def create_concept(payload=None):
        payload = payload or {}

        concept = semantic.create_concept(
            name=payload.get("name", "Untitled Concept"),
            concept_type=payload.get(
                "concept_type",
                "concept",
            ),
            description=payload.get("description", ""),
            aliases=payload.get("aliases"),
            metadata=payload.get("metadata"),
        )

        return _serialize(concept)

    def search_concepts(payload=None):
        payload = payload or {}

        return semantic.search_concepts(
            query=payload.get("query", ""),
            concept_type=payload.get(
                "concept_type",
                "",
            ),
        )

    def assert_fact(payload=None):
        payload = payload or {}

        assertion = semantic.assert_fact(
            subject=payload.get("subject", ""),
            predicate=payload.get("predicate", ""),
            object_value=payload.get(
                "object_value",
                payload.get("object", ""),
            ),
            confidence=payload.get(
                "confidence",
                0.75,
            ),
            source=payload.get(
                "source",
                "aletheus",
            ),
            metadata=payload.get("metadata"),
        )

        return _serialize(assertion)

    def query(payload=None):
        payload = payload or {}

        return semantic.query_assertions(
            subject=payload.get("subject", ""),
            predicate=payload.get("predicate", ""),
            object_value=payload.get(
                "object_value",
                payload.get("object", ""),
            ),
        )

    def explain(payload=None):
        payload = payload or {}

        return semantic.explain_concept(
            name=payload.get("name", ""),
        )

    def bootstrap_cardhawk(payload=None):
        return semantic.bootstrap_cardhawk_semantics()

    def statistics(payload=None):
        return semantic.stats()

    commands.register(
        "semantic.concept.create",
        create_concept,
        replace=True,
    )
    commands.register(
        "semantic.concept.search",
        search_concepts,
        replace=True,
    )
    commands.register(
        "semantic.assert",
        assert_fact,
        replace=True,
    )
    commands.register(
        "semantic.query",
        query,
        replace=True,
    )
    commands.register(
        "semantic.explain",
        explain,
        replace=True,
    )
    commands.register(
        "semantic.bootstrap.cardhawk",
        bootstrap_cardhawk,
        replace=True,
    )
    commands.register(
        "semantic.stats",
        statistics,
        replace=True,
    )
