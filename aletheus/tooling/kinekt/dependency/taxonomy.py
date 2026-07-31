"""Canonical capability and ownership taxonomy."""

from __future__ import annotations


def infer_capability(module: str, owner: str | None) -> str | None:
    if module.startswith("aletheus.runtime"):
        return "Constitutional Runtime Kernel"
    if module.startswith("aletheus.tooling.kinekt"):
        return "Kinekt"
    if module.startswith("aletheus.tooling.genesis"):
        return "Genesis"
    if module.startswith("aletheus.governance"):
        return "Constitutional Governance"
    if module.startswith("aletheus.nimble"):
        return "Nimble"
    if module.startswith("aletheus.platform_intelligence"):
        return "Platform Intelligence"
    if module.startswith(("aletheus.cardhawk", "aletheus.card_hawk")):
        return "Card Hawk"
    if owner and owner.startswith("Aletheus capability:"):
        return owner.removeprefix("Aletheus capability:").strip()
    return None


def capability_owner(capability: str) -> str:
    mapping = {
        "Constitutional Runtime Kernel": "Runtime",
        "Kinekt": "Genesis Engineering",
        "Genesis": "Genesis Engineering",
        "Constitutional Governance": "Governance",
        "Nimble": "Experience",
        "Platform Intelligence": "Platform Intelligence",
        "Card Hawk": "Product",
    }
    return mapping.get(capability, "Unresolved")
