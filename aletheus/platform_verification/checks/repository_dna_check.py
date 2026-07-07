from __future__ import annotations

from pathlib import Path
import time

from aletheus.platform_verification.models import (
    VerificationResult,
    VerificationStatus,
)


EXPECTED_SUBSYSTEMS = {
    "runtime",
    "atlas",
    "oracle",
    "watch_tower",
    "repository_dna",
    "genesis",
    "ontology",
    "concept_collision_engine",
}


def repository_dna_check() -> VerificationResult:
    start = time.perf_counter()

    root = Path("aletheus")

    discovered = {
        p.name
        for p in root.iterdir()
        if p.is_dir()
    }

    missing = sorted(EXPECTED_SUBSYSTEMS - discovered)

    duration = time.perf_counter() - start

    if missing:
        return VerificationResult(
            name="Repository DNA",
            status=VerificationStatus.FAIL,
            summary="Required subsystems missing.",
            duration_seconds=duration,
            errors=missing,
        )

    return VerificationResult(
        name="Repository DNA",
        status=VerificationStatus.PASS,
        summary=f"{len(discovered)} subsystems discovered.",
        duration_seconds=duration,
    )
