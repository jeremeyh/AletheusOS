from __future__ import annotations
import hashlib, json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any

class RSFError(RuntimeError): pass
class RSFValidationError(RSFError): pass
class RSFAuthorityError(RSFError): pass
class RSFInvariantError(RSFError): pass
class RSFRecoveryError(RSFError): pass
class RSFPersistenceError(RSFError): pass

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def _primitive(value: Any) -> Any:
    if is_dataclass(value):
        return _primitive(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(k): _primitive(v) for k,v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_primitive(v) for v in value]
    return value

def canonical_bytes(value: Any) -> bytes:
    return json.dumps(_primitive(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def sha256_digest(value: Any) -> str:
    data = value if isinstance(value, (bytes, bytearray)) else canonical_bytes(value)
    return "sha256:" + hashlib.sha256(bytes(data)).hexdigest()
