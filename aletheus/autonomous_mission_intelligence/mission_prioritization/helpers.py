from __future__ import annotations

from hashlib import sha256
from json import dumps
from typing import Any


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def digest(payload: dict[str, Any]) -> str:
    canonical = dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return sha256(canonical.encode()).hexdigest()
