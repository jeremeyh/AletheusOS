from __future__ import annotations
from dataclasses import asdict
from .model import ChainVerificationResult, MammothEvidenceRecord
from .digests import MammothDigest

class MammothRAFEvidenceBridge:
    """
    Produces deterministic evidence envelopes for RAF ingestion.

    This class is intentionally not a signer, certification authority,
    promotion authority, or release authority.
    """

    @staticmethod
    def build_envelope(
        record: MammothEvidenceRecord,
        chain: ChainVerificationResult,
    ) -> dict:
        record_payload = {
            "sequence": record.sequence,
            "event_id": record.event_id,
            "event_type": record.event_type.value,
            "object_id": record.object_id,
            "version_id": record.version_id,
            "content_digest": record.content_digest,
            "metadata_digest": record.metadata_digest,
            "previous_evidence_hash": record.previous_evidence_hash,
            "evidence_hash": record.evidence_hash,
            "occurred_at_iso": record.occurred_at_iso,
            "actor_capability": record.actor_capability,
            "authority_ref": record.authority_ref,
            "attributes": dict(record.attributes),
        }
        payload = {
            "schemaVersion": "1.0.0",
            "evidenceStandard": "ALETHEUSOS-MAMMOTH-INTEGRITY-PROVENANCE",
            "record": record_payload,
            "chainVerification": asdict(chain),
            "authorityBoundary": {
                "mammothSignsReleases": False,
                "mammothIssuesRAFCertificates": False,
                "rafRemainsExternalAuthority": True,
            },
        }
        payload["envelopeDigest"] = MammothDigest.canonical_sha256(payload)
        return payload
