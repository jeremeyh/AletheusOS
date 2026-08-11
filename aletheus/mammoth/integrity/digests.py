from __future__ import annotations
import hashlib
from typing import Any
from aletheus.mammoth.serialization.canonical import canonical_json_bytes

class MammothDigest:
    @staticmethod
    def bytes_sha256(data: bytes) -> str:
        return "sha256:" + hashlib.sha256(bytes(data)).hexdigest()

    @staticmethod
    def canonical_sha256(value: Any) -> str:
        return MammothDigest.bytes_sha256(canonical_json_bytes(value))
