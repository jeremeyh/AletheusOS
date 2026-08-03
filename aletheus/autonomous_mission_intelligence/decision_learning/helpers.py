from __future__ import annotations

from hashlib import sha256
from json import dumps
from typing import Any


def canonical_digest(payload: dict[str, Any]) -> str:
    encoded = dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()
