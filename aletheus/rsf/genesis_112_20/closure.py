from __future__ import annotations
from dataclasses import asdict, dataclass
from pathlib import Path
import json
from .common import sha256_digest, utc_now_iso, RSFError
from .contracts import RSFContractEngine, ReliabilityAssuranceState
from .bridge import RSFEvidenceBridge, RAFEvidenceConsumerBoundary
from .adversarial import WholeSystemReliabilityAdversarialValidation
from .boundary import RAFRSFConstitutionalBoundaryCertification

@dataclass(frozen=True)
class RSFMasterClosureResult:
    status: str
    evidence_path: str
    evidence_digest: str
    external_raf_certification_required: bool

class RSFMasterClosure:
    """
    Produces RSF master-closure evidence. It deliberately does not self-issue
    the final RAF release certificate.
    """
    @classmethod
    def commission(
        cls,
        *,
        project_root: str | Path,
        output_directory: str | Path,
        persisted_evidence_object_id: str | None = None,
    ) -> RSFMasterClosureResult:
        project = Path(project_root).resolve()
        out = Path(output_directory).resolve()
        out.mkdir(parents=True, exist_ok=True)

        boundary = RAFRSFConstitutionalBoundaryCertification.scan(project)
        if not boundary.passed:
            raise RSFError(f"RSF closure refused: constitutional boundary findings={len(boundary.findings)}")

        adversarial = WholeSystemReliabilityAdversarialValidation.run()
        if not all(x.passed for x in adversarial):
            raise RSFError("RSF closure refused: adversarial validation failed")

        contract = RSFContractEngine.evaluate_contract(
            "aletheusos-core-runtime", ReliabilityAssuranceState.HEALTHY,
            failure_domain="runtime"
        )
        envelope = RSFEvidenceBridge.emit(
            contract,
            ("112.20.1:contract", "112.20.7:adversarial", "112.20.8:boundary")
        )
        if not RAFEvidenceConsumerBoundary.validate_for_consumption(envelope):
            raise RSFError("RSF closure refused: RAF evidence bridge envelope invalid")

        body = {
            "schemaVersion":"1.0.0",
            "standard":"ALETHEUSOS-RSF-MASTER-CLOSURE-EVIDENCE",
            "status":"RSF_MASTER_CLOSURE_EVIDENCE_COMPLETE",
            "contract":asdict(contract),
            "evidenceEnvelope":asdict(envelope),
            "adversarial":[asdict(x) for x in adversarial],
            "boundary":asdict(boundary),
            "persistedEvidenceObjectId":persisted_evidence_object_id,
            "commissionedAtIso":utc_now_iso(),
            "authorityBoundary":{
                "rsfMaySelfIssueRAFCertificate":False,
                "externalRAFCertificationRequired":True
            }
        }
        digest = sha256_digest(body)
        path = out/"rsf-master-closure-evidence.json"
        path.write_text(json.dumps({**body, "evidenceDigest":digest}, indent=2, sort_keys=True, default=str)+"\n", encoding="utf-8")
        return RSFMasterClosureResult(
            "RSF_MASTER_CLOSURE_EVIDENCE_COMPLETE", str(path), digest, True
        )
