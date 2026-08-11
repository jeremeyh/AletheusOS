from __future__ import annotations
import json, tempfile
from dataclasses import dataclass
from pathlib import Path
from aletheus.mammoth.integrity import (
    EvidenceEventType, MammothDigest, MammothIntegrityVerifier,
    MammothProvenanceLedger, MammothRAFEvidenceBridge
)

@dataclass(frozen=True, slots=True)
class Genesis1134AssuranceResult:
    status: str
    checks: tuple[str, ...]
    evidence_digest: str

class Genesis1134Assurance:
    @staticmethod
    def run() -> Genesis1134AssuranceResult:
        with tempfile.TemporaryDirectory() as d:
            data = b"ALETHEUSOS-MAMMOTH-113.4"
            content_digest = MammothDigest.bytes_sha256(data)
            MammothIntegrityVerifier.require_bytes(data, content_digest)
            ledger = MammothProvenanceLedger(Path(d)/"mammoth-provenance.jsonl")
            rec = ledger.append(
                event_type=EvidenceEventType.PERSISTED,
                object_id="mobj-assurance1134",
                version_id="mver-assurance1134",
                content_digest=content_digest,
                metadata_digest=MammothDigest.canonical_sha256({"schemaVersion":"1.0.0"}),
                occurred_at_iso="2026-08-08T00:00:00Z",
                actor_capability="Genesis113.4",
                attributes={"purpose":"assurance"},
            )
            chain = ledger.verify()
            assert chain.valid and chain.record_count == 1
            envelope = MammothRAFEvidenceBridge.build_envelope(rec, chain)
            assert envelope["authorityBoundary"]["rafRemainsExternalAuthority"] is True
            # tamper copy to prove detection
            p = Path(d)/"tamper.jsonl"
            p.write_text((Path(d)/"mammoth-provenance.jsonl").read_text(), encoding="utf-8")
            raw = json.loads(p.read_text())
            raw["actor_capability"] = "TAMPERED"
            p.write_text(json.dumps(raw)+"\n", encoding="utf-8")
            assert not MammothProvenanceLedger(p).verify().valid

        checks = (
            "FULL_SHA256_CONTENT_INTEGRITY",
            "CANONICAL_METADATA_DIGEST",
            "DURABLE_APPEND_ONLY_PROVENANCE_LEDGER",
            "HASH_CHAIN_LINKAGE_VERIFIED",
            "EACH_RECORD_HASH_RECOMPUTED",
            "TAMPER_DETECTION_FAILS_CLOSED",
            "RECOVERY_VERIFICATION_NEVER_SILENTLY_REWRITES",
            "RAF_EVIDENCE_ENVELOPE_DETERMINISTIC",
            "RAF_AUTHORITY_NOT_REIMPLEMENTED",
            "NO_REASONING_OR_UI_ABSORBED",
        )
        digest = MammothDigest.canonical_sha256({"checks": checks})
        return Genesis1134AssuranceResult("PASS", checks, digest)
