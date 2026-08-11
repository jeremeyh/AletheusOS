from __future__ import annotations
from dataclasses import asdict, is_dataclass
import hashlib, json
from typing import Any, List

class EvidenceJournal:
    """In-memory journal. Durable writes require an injected Mammoth gateway."""
    def __init__(self):
        self._events: List[dict] = []

    def append(self, event: Any) -> str:
        payload=asdict(event) if is_dataclass(event) else dict(event)
        raw=json.dumps(payload, sort_keys=True, separators=(",",":"), default=str).encode()
        digest="sha256:"+hashlib.sha256(raw).hexdigest()
        self._events.append({"digest":digest,"payload":payload})
        return digest

    def persist(self, mammoth_gateway) -> Any:
        if mammoth_gateway is None or not callable(getattr(mammoth_gateway,"persist_assurance_evidence",None)):
            raise RuntimeError("Mammoth gateway required; direct persistence refused")
        return mammoth_gateway.persist_assurance_evidence(tuple(self._events))

    def events(self):
        return tuple(self._events)
