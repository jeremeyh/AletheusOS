"""Dependency policy evaluation."""

from __future__ import annotations

from .models import PolicyFinding


def evaluate_dependency(
    source_module: str,
    source_capability: str | None,
    target_module: str,
    target_capability: str | None,
    evidence: tuple[str, ...],
) -> PolicyFinding | None:
    if source_module.startswith("aletheus.runtime") and target_module.startswith(
        ("aletheus.nimble", "aletheus.applications", "aletheus.cardhawk")
    ):
        return PolicyFinding(
            code="RUNTIME_DEPENDS_ON_PRODUCT_OR_EXPERIENCE",
            severity="high",
            source=source_module,
            target=target_module,
            message="Runtime must remain independent of product and experience layers.",
            evidence=evidence,
        )

    if source_capability in {"Kinekt", "Genesis", "Platform Intelligence"} and (
        target_capability == "Card Hawk"
    ):
        return PolicyFinding(
            code="PLATFORM_DEPENDS_ON_PRODUCT",
            severity="high",
            source=source_module,
            target=target_module,
            message="Platform capabilities must not depend on product applications.",
            evidence=evidence,
        )

    if source_module.startswith("aletheus.governance") and target_module.startswith(
        ("aletheus.cardhawk", "aletheus.card_hawk")
    ):
        return PolicyFinding(
            code="GOVERNANCE_PRODUCT_COUPLING",
            severity="medium",
            source=source_module,
            target=target_module,
            message="Governance should inspect products through stable interfaces.",
            evidence=evidence,
        )

    return None
