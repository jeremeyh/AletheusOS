from __future__ import annotations
from pathlib import Path
import ast
from .common import digest
from .g112_21_9 import PlatformServiceFabricMasterClosure

FORBIDDEN_NAMES={"issue_release_certificate","sign_release","self_certify","certify_release"}

class ExternalRAFProjectCertification:
    @staticmethod
    def _scan_for_self_certification(root:Path):
        findings=[]
        target=root/"aletheus/platform_service_fabric"
        if not target.exists():
            return findings
        for p in target.rglob("*.py"):
            if "__pycache__" in p.parts: continue
            try: tree=ast.parse(p.read_text(encoding="utf-8",errors="replace"))
            except Exception: continue
            for n in ast.walk(tree):
                if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in FORBIDDEN_NAMES:
                    findings.append(str(p.relative_to(root))+":"+n.name)
        return findings

    @classmethod
    def certify(cls, project_root, closure_payload=None):
        root=Path(project_root).resolve()
        closure=closure_payload or PlatformServiceFabricMasterClosure.close()
        checks={
          "masterClosureEvidenceComplete": closure.get("status")=="PLATFORM_SERVICE_FABRIC_MASTER_CLOSURE_EVIDENCE_COMPLETE",
          "closureRequiresExternalRAF": closure.get("externalRAFCertificationRequired") is True,
          "noServiceFabricSelfCertification": len(cls._scan_for_self_certification(root))==0,
          "mammothBoundaryDeclared": closure["checks"].get("mammothCertifiedPersistenceBoundaryRequired") is True,
          "rsfAuthorityPreserved": closure["checks"].get("rsfReliabilityAuthorityPreserved") is True,
          "runtimeCoreCompositionRootPreserved": closure["checks"].get("runtimeCoreCompositionRootPreserved") is True,
          "noSecondRegistryAuthority": closure["checks"].get("noSecondRegistryAuthorityCreated") is True,
        }
        ok=all(checks.values())
        result={
          "standard":"ALETHEUSOS-GENESIS-112.21.9.1-EXTERNAL-RAF-PROJECT-CERTIFICATION",
          "closureEvidenceDigest":closure["evidenceDigest"],
          "checks":checks,
          "status":"GENESIS_112_21_PLATFORM_SERVICE_FABRIC_PROJECT_CERTIFIED" if ok else "REFUSED",
        }
        result["certificationDigest"]=digest(result)
        return result
