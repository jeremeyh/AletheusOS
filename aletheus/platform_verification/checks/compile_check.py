from __future__ import annotations

import subprocess
import time

from aletheus.platform_verification.models import (
    VerificationResult,
    VerificationStatus,
)


def compile_check() -> VerificationResult:
    start = time.perf_counter()

    process = subprocess.run(
        ["python", "-m", "compileall", "aletheus"],
        capture_output=True,
        text=True,
    )

    duration = time.perf_counter() - start

    if process.returncode == 0:
        return VerificationResult(
            name="Compile Verification",
            status=VerificationStatus.PASS,
            summary="Python compilation completed successfully.",
            duration_seconds=duration,
        )

    return VerificationResult(
        name="Compile Verification",
        status=VerificationStatus.FAIL,
        summary="Compilation failed.",
        duration_seconds=duration,
        errors=[process.stderr or process.stdout],
    )
