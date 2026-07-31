"""Layer classification for Kinekt™ boundary analysis."""

from __future__ import annotations


def classify_layer(node_id: str, name: str, capability: str | None) -> str:
    haystack = " ".join(
        value for value in (node_id, name, capability or "") if value
    ).lower()

    if any(token in haystack for token in ("runtime", "crk", "kernel")):
        return "runtime"
    if any(token in haystack for token in ("truth", "principle x", "constitution")):
        return "constitutional"
    if "governance" in haystack:
        return "governance"
    if any(
        token in haystack
        for token in (
            "platform intelligence",
            "mammoth",
            "ctf",
            "kinekt",
            "storage",
            "registry",
        )
    ):
        return "platform"
    if any(token in haystack for token in ("nimble", "experience", "ui")):
        return "experience"
    if any(
        token in haystack
        for token in ("card hawk", "cardhawk", "application", "product")
    ):
        return "product"
    if any(token in haystack for token in ("tooling", "genesis")):
        return "tooling"
    return "unknown"
