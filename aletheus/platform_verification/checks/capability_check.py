from __future__ import annotations

import importlib
import time

from aletheus.platform_verification.models import (
    VerificationResult,
    VerificationStatus,
)

CORE_CAPABILITIES = {
    "Atlas": "aletheus.atlas",
    "Repository DNA": "aletheus.repository_dna",
    "Watch Tower": "aletheus.watch_tower",
    "Oracle": "aletheus.oracle",
    "Genesis": "aletheus.genesis",
    "Ontology": "aletheus.ontology",
    "Concept Collision Engine": "aletheus.concept_collision_engine",
    "Runtime": "aletheus.runtime",
}


def capability_check() -> VerificationResult:
    start = time.perf_counter()
    missing = []

    for name, module_path in CORE_CAPABILITIES.items():
        try:
            importlib.import_module(module_path)
        except Exception as exc:
            missing.append(f"{name}: {exc!r}")

    duration = time.perf_counter() - start

    if missing:
        return VerificationResult(
            name="Capability Verification",
            status=VerificationStatus.FAIL,
            summary="One or more core capabilities failed to import.",
            duration_seconds=duration,
            errors=missing,
        )

    return VerificationResult(
        name="Capability Verification",
        status=VerificationStatus.PASS,
        summary=f"{len(CORE_CAPABILITIES)} core capabilities available.",
        duration_seconds=duration,
    )
