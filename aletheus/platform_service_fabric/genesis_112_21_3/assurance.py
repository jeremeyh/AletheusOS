from __future__ import annotations
from pathlib import Path
import ast, json, hashlib, os, tempfile
from .contracts import BindingDisposition
from .bindings import CanonicalBindingRegistry, CANONICAL_BINDING_DESCRIPTORS, PREDECESSOR_EXPECTED_DIGEST

PREDECESSOR_REPORT="reports/platform-service-fabric/genesis-112.21.2.3/runtime-registry-authority-resolution.json"
PREDECESSOR_GATE="reports/platform-service-fabric/genesis-112.21.2.3/genesis-112.21.3-entry-gate.json"

def _atomic(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    data=json.dumps(obj,indent=2,sort_keys=True).encode()
    fd,tmp=tempfile.mkstemp(prefix=path.name+".",dir=path.parent)
    try:
        with os.fdopen(fd,"wb") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def _digest(obj):
    return "sha256:"+hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":")).encode()).hexdigest()

class Genesis112213Assurance:
    @staticmethod
    def validate_predecessor(project_root):
        root=Path(project_root).resolve()
        rp=root/PREDECESSOR_REPORT
        gp=root/PREDECESSOR_GATE
        if not rp.exists() or not gp.exists():
            raise RuntimeError("Genesis 112.21.2.3 predecessor evidence is missing")
        report=json.loads(rp.read_text())
        gate=json.loads(gp.read_text())
        if report.get("evidenceDigest") != PREDECESSOR_EXPECTED_DIGEST:
            raise RuntimeError("Genesis 112.21.2.3 evidence digest does not match locked ancestry")
        if not gate.get("entryPermitted"):
            raise RuntimeError("Genesis 112.21.3 entry gate is not permitted")
        if gate.get("foundationalBlockers"):
            raise RuntimeError("Genesis 112.21.3 entry refused: foundational blockers remain")
        return report,gate

    @staticmethod
    def boundary_checks():
        ds=CANONICAL_BINDING_DESCRIPTORS
        ids=[d.identity.service_id for d in ds]
        checks={
          "uniqueCanonicalServiceIds":len(ids)==len(set(ids)),
          "serviceRegistryComposed":next(d for d in ds if d.identity.service_id=="platform.service.discovery").disposition==BindingDisposition.COMPOSE,
          "runtimeInspectorComposed":next(d for d in ds if d.identity.service_id=="platform.runtime.inspection").disposition==BindingDisposition.COMPOSE,
          "engineRegistryDistinctAuthority":next(d for d in ds if d.identity.service_id=="platform.engine.registration").identity.authority.value=="ENGINE_REGISTRATION",
          "lifecycleContractFormalized":any(d.identity.service_id=="platform.lifecycle.coordination" for d in ds),
          "rsfAuthorityPreserved":next(d for d in ds if d.identity.service_id=="platform.reliability.observation").identity.owner_domain=="RSF",
          "mammothPersistenceOwnerDeclared":all(d.identity.persistence_owner=="MAMMOTH" for d in ds),
          "rafFinalAuthorityDeclared":all(d.identity.release_authority=="RAF" for d in ds),
          "runtimeCoreMutationRequired":False,
          "sourceReplacementRequired":False,
        }
        return checks

    @classmethod
    def write_assurance(cls, project_root):
        cls.validate_predecessor(project_root)
        registry=CanonicalBindingRegistry()
        ev=registry.evidence()
        checks=cls.boundary_checks()
        passed=all(v is True for k,v in checks.items() if k not in ("runtimeCoreMutationRequired","sourceReplacementRequired")) and not checks["runtimeCoreMutationRequired"] and not checks["sourceReplacementRequired"]
        out={
          "schemaVersion":"1.0.0",
          "standard":"ALETHEUSOS-GENESIS-112.21.3-CANONICAL-SERVICE-CONTRACT-ASSURANCE",
          "predecessorEvidenceDigest":PREDECESSOR_EXPECTED_DIGEST,
          "bindingEvidenceDigest":ev.canonical_digest(),
          "checks":checks,
          "status":"CANONICAL_SERVICE_CONTRACT_BINDING_READY" if passed else "REFUSED",
          "next":"112.21.4 Lifecycle / Registration Fabric integration",
        }
        out["evidenceDigest"]=_digest(out)
        root=Path(project_root).resolve()
        dest=root/"reports/platform-service-fabric/genesis-112.21.3"
        _atomic(dest/"canonical-service-contract-assurance.json",out)
        _atomic(dest/"canonical-service-binding-descriptors.json",{
          "schemaVersion":"1.0.0",
          "serviceIds":[d.identity.service_id for d in CANONICAL_BINDING_DESCRIPTORS],
          "runtimeRegistryDisposition":"EXCLUDE_NON_CANONICAL",
          "bindingEvidenceDigest":ev.canonical_digest(),
          "sourceMutationRequired":False,
          "runtimeCoreMutationRequired":False,
        })
        return out
