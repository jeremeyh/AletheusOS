"""Canonical ownership inference."""

from __future__ import annotations

from pathlib import PurePosixPath


def infer_owner(path: PurePosixPath) -> str:
    parts = path.parts

    if len(parts) >= 2 and parts[0] == "aletheus":
        if parts[1] == "runtime":
            return "Constitutional Runtime Kernel"
        if parts[1] == "tooling":
            return "Genesis Engineering"
        if parts[1] == "platform_intelligence":
            return "Platform Intelligence"
        if parts[1] == "nimble":
            return "Nimble Experience Runtime"
        if parts[1] in {"applications", "cardhawk", "card_hawk"}:
            return "Product Application"
        return f"Aletheus capability: {parts[1]}"

    if parts and parts[0] == "tests":
        return "Validation"
    if parts and parts[0] == "docs":
        return "Architecture Documentation"
    if parts and parts[0] == "reports":
        return "Generated Evidence"

    return "Unresolved"
