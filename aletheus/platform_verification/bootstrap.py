from __future__ import annotations

from .registry import VerificationRegistry


def bootstrap_verification_registry() -> VerificationRegistry:
    return VerificationRegistry()
