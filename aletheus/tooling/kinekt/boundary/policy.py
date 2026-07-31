"""Boundary policy rules."""

from __future__ import annotations

from .models import BoundaryFinding


def evaluate(
    source: str,
    target: str,
    source_layer: str,
    target_layer: str,
    evidence: tuple[str, ...],
) -> BoundaryFinding | None:
    if source_layer == "runtime" and target_layer in {"experience", "product"}:
        return BoundaryFinding(
            code="RUNTIME_LAYER_LEAK",
            severity="high",
            source=source,
            target=target,
            source_layer=source_layer,
            target_layer=target_layer,
            message="Runtime must not depend on experience or product implementation.",
            evidence=evidence,
            recommendation="Introduce a runtime-facing contract or invert the dependency.",
        )

    if source_layer == "platform" and target_layer == "product":
        return BoundaryFinding(
            code="PLATFORM_PRODUCT_COUPLING",
            severity="high",
            source=source,
            target=target,
            source_layer=source_layer,
            target_layer=target_layer,
            message="Platform capabilities must remain product-independent.",
            evidence=evidence,
            recommendation="Move product-specific behavior behind a product adapter.",
        )

    if source_layer == "governance" and target_layer == "product":
        return BoundaryFinding(
            code="GOVERNANCE_IMPLEMENTATION_COUPLING",
            severity="medium",
            source=source,
            target=target,
            source_layer=source_layer,
            target_layer=target_layer,
            message="Governance should inspect products through stable evidence interfaces.",
            evidence=evidence,
            recommendation="Replace direct imports with a governed evidence contract.",
        )

    if source_layer == "experience" and target_layer == "runtime":
        return BoundaryFinding(
            code="EXPERIENCE_RUNTIME_INTERNAL_COUPLING",
            severity="medium",
            source=source,
            target=target,
            source_layer=source_layer,
            target_layer=target_layer,
            message="Experience code should depend on runtime contracts, not internals.",
            evidence=evidence,
            recommendation="Route the dependency through the runtime facade or public API.",
        )

    if source_layer == "runtime" and target_layer == "tooling":
        return BoundaryFinding(
            code="RUNTIME_TOOLING_DEPENDENCY",
            severity="high",
            source=source,
            target=target,
            source_layer=source_layer,
            target_layer=target_layer,
            message="Runtime must not depend on build or repository tooling.",
            evidence=evidence,
            recommendation="Move shared behavior into a runtime-owned platform contract.",
        )

    return None
