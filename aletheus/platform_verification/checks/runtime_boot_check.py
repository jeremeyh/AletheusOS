from __future__ import annotations

import time

from aletheus.platform_verification.models import (
    VerificationResult,
    VerificationStatus,
)


def runtime_boot_check() -> VerificationResult:
    start = time.perf_counter()

    try:
        from aletheus.runtime import AletheusRuntime

        runtime = AletheusRuntime()

        duration = time.perf_counter() - start

        return VerificationResult(
            name="Runtime Boot",
            status=VerificationStatus.PASS,
            summary=f"{runtime.__class__.__name__} initialized successfully.",
            duration_seconds=duration,
        )

    except Exception as exc:
        duration = time.perf_counter() - start

        return VerificationResult(
            name="Runtime Boot",
            status=VerificationStatus.FAIL,
            summary="Runtime failed to initialize.",
            duration_seconds=duration,
            errors=[repr(exc)],
        )
