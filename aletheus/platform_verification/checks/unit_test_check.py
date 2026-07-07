from __future__ import annotations

import subprocess
import time
import re

from aletheus.platform_verification.models import (
    VerificationResult,
    VerificationStatus,
)


def unit_test_check() -> VerificationResult:
    start = time.perf_counter()

    process = subprocess.run(
        ["python", "-m", "pytest", "aletheus", "-q"],
        capture_output=True,
        text=True,
    )

    duration = time.perf_counter() - start

    output = process.stdout + process.stderr

    passed = re.search(r"(\d+)\s+passed", output)

    summary = "Unit tests executed."

    if passed:
        summary = f"{passed.group(1)} tests passed."

    if process.returncode == 0:
        return VerificationResult(
            name="Unit Test Verification",
            status=VerificationStatus.PASS,
            summary=summary,
            duration_seconds=duration,
        )

    return VerificationResult(
        name="Unit Test Verification",
        status=VerificationStatus.FAIL,
        summary="Unit tests failed.",
        duration_seconds=duration,
        errors=[output],
    )
