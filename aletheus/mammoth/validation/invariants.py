from __future__ import annotations

import re
from datetime import datetime

_OBJECT_RE = re.compile(r"^mobj-[a-f0-9]{32}$")
_VERSION_RE = re.compile(r"^mver-[a-f0-9]{32}$")
_LINEAGE_RE = re.compile(r"^mlin-[a-f0-9]{32}$")
_DIGEST_RE = re.compile(r"^sha256:[a-f0-9]{64}$")
_NAMESPACE_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._:-]{0,127}$")


class MammothInvariantViolation(ValueError):
    pass


class MammothInvariants:
    @staticmethod
    def require_nonblank(value: str, field: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise MammothInvariantViolation(f"{field} must be a nonblank string")
        return value.strip()

    @staticmethod
    def validate_object_id(value: str) -> str:
        if not _OBJECT_RE.fullmatch(value):
            raise MammothInvariantViolation(f"invalid Mammoth object_id: {value!r}")
        return value

    @staticmethod
    def validate_version_id(value: str) -> str:
        if not _VERSION_RE.fullmatch(value):
            raise MammothInvariantViolation(f"invalid Mammoth version_id: {value!r}")
        return value

    @staticmethod
    def validate_lineage_id(value: str) -> str:
        if not _LINEAGE_RE.fullmatch(value):
            raise MammothInvariantViolation(f"invalid Mammoth lineage_id: {value!r}")
        return value

    @staticmethod
    def validate_digest(value: str) -> str:
        if not _DIGEST_RE.fullmatch(value):
            raise MammothInvariantViolation(f"invalid Mammoth SHA-256 digest: {value!r}")
        return value

    @staticmethod
    def validate_namespace(value: str) -> str:
        if not _NAMESPACE_RE.fullmatch(value):
            raise MammothInvariantViolation(f"invalid Mammoth namespace: {value!r}")
        return value

    @staticmethod
    def validate_iso8601(value: str) -> str:
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except Exception as exc:
            raise MammothInvariantViolation(f"invalid ISO-8601 timestamp: {value!r}") from exc
        return value
