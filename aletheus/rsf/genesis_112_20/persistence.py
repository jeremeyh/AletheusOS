from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Protocol
from .bridge import RSFEvidenceEnvelope
from .common import RSFPersistenceError, canonical_bytes

class MammothGatewayProtocol(Protocol):
    async def persist(self, consumer, *, namespace: str, **kwargs): ...

@dataclass(frozen=True)
class AssurancePersistenceReceipt:
    object_id: str
    namespace: str
    content_type: str
    consumer_identity: str
    persisted_via_mammoth_gateway: bool

class RSFMammothPersistenceIntegration:
    NAMESPACE = "system.assurance.rsf"

    @staticmethod
    async def persist_assurance_evidence(
        mammoth_gateway: Any,
        consumer_identity: Any,
        envelope: RSFEvidenceEnvelope,
        retention_class: Any,
    ) -> AssurancePersistenceReceipt:
        if mammoth_gateway is None:
            raise RSFPersistenceError("Mammoth gateway is required")
        payload = canonical_bytes(asdict(envelope))
        result = await mammoth_gateway.persist(
            consumer_identity,
            namespace=RSFMammothPersistenceIntegration.NAMESPACE,
            object_type="rsf-assurance-evidence",
            content_type="application/json",
            data=payload,
            retention_class=retention_class,
            producer_capability="RSF_GENESIS_112_20_6",
        )
        object_id = getattr(result, "object_id", None) or getattr(result, "objectId", None)
        if object_id is None and isinstance(result, dict):
            object_id = result.get("object_id") or result.get("objectId")
        if not object_id:
            raise RSFPersistenceError("Mammoth gateway returned no canonical object identifier")
        return AssurancePersistenceReceipt(
            str(object_id), RSFMammothPersistenceIntegration.NAMESPACE,
            "application/json", str(consumer_identity), True
        )
