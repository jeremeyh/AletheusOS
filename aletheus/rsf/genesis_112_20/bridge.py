from __future__ import annotations
from dataclasses import dataclass, asdict
from .common import sha256_digest, utc_now_iso, RSFAuthorityError
from .contracts import RSFAssuranceContract, ReliabilityAssuranceState

@dataclass(frozen=True)
class RSFEvidenceEnvelope:
    schema_version: str
    standard: str
    component_id: str
    state: ReliabilityAssuranceState
    contract_standard: str
    evidence_refs: tuple[str, ...]
    emitted_at_iso: str
    payload_digest: str

class RSFEvidenceBridge:
    STANDARD = "ALETHEUSOS-RSF-EVIDENCE-BRIDGE"

    @classmethod
    def emit(
        cls,
        contract: RSFAssuranceContract,
        evidence_refs: tuple[str, ...],
    ) -> RSFEvidenceEnvelope:
        body = {
            "schemaVersion":"1.0.0",
            "standard":cls.STANDARD,
            "componentId":contract.component_id,
            "state":contract.current_state.value,
            "contractStandard":contract.standard,
            "evidenceRefs":list(evidence_refs),
        }
        return RSFEvidenceEnvelope(
            "1.0.0", cls.STANDARD, contract.component_id, contract.current_state,
            contract.standard, evidence_refs, utc_now_iso(), sha256_digest(body)
        )

class RAFEvidenceConsumerBoundary:
    """
    RAF may consume and validate RSF evidence, but this boundary does not grant
    RAF authority to rewrite the RSF evidence and does not grant RSF authority
    to sign or issue a release certificate.
    """
    @staticmethod
    def validate_for_consumption(envelope: RSFEvidenceEnvelope) -> bool:
        return (
            envelope.standard == RSFEvidenceBridge.STANDARD
            and envelope.payload_digest.startswith("sha256:")
            and len(envelope.payload_digest) == 71
        )

    @staticmethod
    def sign_release_from_rsf(*_args, **_kwargs):
        raise RSFAuthorityError("RSF evidence bridge cannot issue or sign a release certificate")
