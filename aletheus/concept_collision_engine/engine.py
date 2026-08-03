from __future__ import annotations

from collections.abc import Iterable

from .models import (
    CollisionFinding,
    CollisionOutcome,
    CollisionReport,
    CollisionSeverity,
    CollisionType,
    ConceptSignature,
)


class ConceptCollisionEngine:
    """
    Evaluates a proposed concept against known concepts.

    Constitutional purpose:
    enforce the Principle of Non-Redundant Evolution.
    """

    def __init__(self, similarity_threshold: float = 0.72) -> None:
        self.similarity_threshold = similarity_threshold

    def evaluate(
        self,
        candidate: ConceptSignature,
        existing: Iterable[ConceptSignature],
    ) -> CollisionReport:
        report = CollisionReport(candidate=candidate)

        for target in existing:
            finding = self._compare(candidate, target)
            if finding:
                report.add_finding(finding)

        return report

    def _compare(
        self,
        source: ConceptSignature,
        target: ConceptSignature,
    ) -> CollisionFinding | None:
        if source.name.lower() == target.name.lower():
            return CollisionFinding(
                source=source,
                target=target,
                collision_type=CollisionType.SEMANTIC,
                severity=CollisionSeverity.COLLISION_RISK,
                confidence=1.0,
                recommended_outcome=CollisionOutcome.NEEDS_ADR,
                rationale="Exact canonical name match detected.",
                requires_adr=True,
            )

        if (
            source.authority
            and target.authority
            and source.authority == target.authority
        ) and (
            source.owns and target.owns and source.owns.lower() == target.owns.lower()
        ):
            return CollisionFinding(
                source=source,
                target=target,
                collision_type=CollisionType.AUTHORITY,
                severity=CollisionSeverity.VIOLATION,
                confidence=0.96,
                recommended_outcome=CollisionOutcome.REASSIGN_AUTHORITY,
                rationale="Two concepts claim the same sovereign authority domain.",
                requires_adr=True,
            )

        source_terms = source.normalized_terms()
        target_terms = target.normalized_terms()

        if not source_terms or not target_terms:
            return None

        overlap = source_terms.intersection(target_terms)
        union = source_terms.union(target_terms)
        score = len(overlap) / len(union)

        if score >= self.similarity_threshold:
            return CollisionFinding(
                source=source,
                target=target,
                collision_type=CollisionType.SEMANTIC,
                severity=CollisionSeverity.OVERLAP_RISK,
                confidence=round(score, 3),
                recommended_outcome=CollisionOutcome.NEEDS_ADR,
                rationale=f"Semantic overlap detected: {sorted(overlap)}",
                requires_adr=True,
            )

        if (
            source.family
            and target.family
            and source.family == target.family
            and score >= 0.45
        ):
            return CollisionFinding(
                source=source,
                target=target,
                collision_type=CollisionType.FUNCTIONAL,
                severity=CollisionSeverity.ADJACENT,
                confidence=round(score, 3),
                recommended_outcome=CollisionOutcome.KEEP,
                rationale="Concepts are adjacent within the same family; review recommended.",
            )

        return None
