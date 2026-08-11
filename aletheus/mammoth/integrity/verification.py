from __future__ import annotations
from .digests import MammothDigest
from .model import IntegrityVerificationResult

class MammothIntegrityVerifier:
    @staticmethod
    def verify_bytes(data: bytes, expected_digest: str) -> IntegrityVerificationResult:
        computed = MammothDigest.bytes_sha256(data)
        return IntegrityVerificationResult(
            valid=computed == expected_digest,
            expected_digest=expected_digest,
            computed_digest=computed,
            size_bytes=len(data),
        )

    @staticmethod
    def require_bytes(data: bytes, expected_digest: str) -> None:
        result = MammothIntegrityVerifier.verify_bytes(data, expected_digest)
        if not result.valid:
            raise ValueError(
                f"integrity verification failed: expected {result.expected_digest}, "
                f"computed {result.computed_digest}"
            )
