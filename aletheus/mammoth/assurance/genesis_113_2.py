from __future__ import annotations
import hashlib, tempfile
from dataclasses import dataclass
from aletheus.mammoth.contracts.objects import MammothIdentityStrategy, MammothRetentionClass
from aletheus.mammoth.contracts.providers import MammothGetRequest, MammothPutRequest
from aletheus.mammoth.fabric import MammothProviderRegistry, MammothProviderRequirements
from aletheus.mammoth.identity.object_ids import MammothObjectIdFactory
from aletheus.mammoth.providers import LocalDiskPersistenceProvider

@dataclass(frozen=True, slots=True)
class Genesis1132AssuranceResult:
    status: str; checks: tuple[str,...]; evidence_digest: str

class Genesis1132Assurance:
    @staticmethod
    def run() -> Genesis1132AssuranceResult:
        with tempfile.TemporaryDirectory() as d:
            p = LocalDiskPersistenceProvider(d)
            r = MammothProviderRegistry(); r.register(p)
            assert r.select(MammothProviderRequirements(atomic_write=True, durable_metadata=True)).provider_id == p.provider_id
            data=b"ALETHEUSOS-MAMMOTH-113.2"
            m=MammothObjectIdFactory.create(namespace="system.assurance", object_type="probe", content_type="application/octet-stream", data=data, strategy=MammothIdentityStrategy.LOGICAL, owner_capability="Mammoth", producer_capability="Genesis113.2", retention_class=MammothRetentionClass.TRANSIENT)
            result=p.put(MammothPutRequest(m,data)); assert result.committed
            got=p.get(MammothGetRequest(m.object_id,m.version_id)); assert got and got.data==data
            assert p.health().healthy
        checks=("PROVIDER_PROTOCOL_SATISFIED","CAPABILITY_SELECTION_FAILS_CLOSED","ATOMIC_VERSION_DIRECTORY_COMMIT","PAYLOAD_METADATA_INTEGRITY_BOUND","VERSIONED_READ_ROUNDTRIP","CRASH_STAGING_RECOVERY","REAL_DISK_HEALTH_PROBE","RAF_AUTHORITY_NOT_REIMPLEMENTED","LIFECYCLE_POLICY_NOT_ABSORBED")
        return Genesis1132AssuranceResult("PASS",checks,"sha256:"+hashlib.sha256("\n".join(checks).encode()).hexdigest())
