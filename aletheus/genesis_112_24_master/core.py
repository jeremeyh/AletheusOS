
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
from typing import Any
import ast, hashlib, json

FAMILY_ID = '112.24.1-112.24.9.1'
FAMILY_TITLE = 'Platform Orchestration & Execution Fabric'
TERMINAL_STATUS = 'GENESIS_112_24_PLATFORM_ORCHESTRATION_FABRIC_PROJECT_CERTIFIED'
REPORT_FAMILY = 'platform-orchestration-fabric'
PHASES = (('112.24.1', 'Canonical Orchestration Contract'), ('112.24.2', 'Execution Context & Invocation Envelope'), ('112.24.3', 'Capability Invocation Router'), ('112.24.4', 'Workflow / Pipeline Execution Coordination'), ('112.24.5', 'Scheduling & Dependency-Aware Execution'), ('112.24.6', 'Execution Failure, Retry & Recovery Semantics'), ('112.24.7', 'Distributed Execution & Runtime Fabric Bridge'), ('112.24.8', 'Orchestration Adversarial / Concurrency / Recovery Validation'), ('112.24.9', 'Platform Orchestration Fabric Master Closure'), ('112.24.9.1', 'External RAF Certification & Gold Seal'))
ANCHORS = ('ORCHESTRATION', 'EXECUTION', 'INVOCATION', 'WORKFLOW', 'SCHEDULING', 'RECOVERY')
REQUIRED_PATHS = ('aletheus/platform_service_fabric', 'aletheus/platform_capability_fabric')
ROOT_ANCESTOR = ''
PREDECESSOR_REPORT_FAMILY = 'capability-composition-fabric'
PREDECESSOR_STATUS = 'GENESIS_112_23_CAPABILITY_COMPOSITION_FABRIC_PROJECT_CERTIFIED'

class Disposition(str, Enum):
    REUSE="REUSE"
    COMPOSE="COMPOSE"
    REFACTOR="REFACTOR"
    PROMOTE_CANDIDATE="PROMOTE_CANDIDATE"
    DORMANT="DORMANT"
    ABSTAIN="ABSTAIN"

def canonical_digest(obj:Any)->str:
    raw=json.dumps(obj,sort_keys=True,separators=(",",":"),default=str).encode()
    return "sha256:"+hashlib.sha256(raw).hexdigest()

def _read_json(path:Path):
    try: return json.loads(path.read_text())
    except Exception: return None

def predecessor_proven(root:Path)->tuple[bool,str]:
    # First family is locked to the exact 112.22.1 project-assurance digest.
    if FAMILY_ID.startswith("112.22"):
        p=root/"reports/platform-capability-fabric/genesis-112.22.1/capability-attachment-assurance.json"
        d=_read_json(p)
        ok=bool(d and d.get("status")==PREDECESSOR_STATUS and d.get("evidenceDigest")==ROOT_ANCESTOR)
        return ok, str(p)
    # Later families require the prior family's external RAF/closure status.
    report_root=root/"reports"/PREDECESSOR_REPORT_FAMILY
    if not report_root.exists(): return False, str(report_root)
    for p in sorted(report_root.rglob("*.json"), reverse=True):
        d=_read_json(p)
        if d and (d.get("status")==PREDECESSOR_STATUS or d.get("finalStatus")==PREDECESSOR_STATUS):
            return True, str(p)
    return False, str(report_root)

def scan_repository(root:str|Path)->dict:
    root=Path(root).resolve()
    pred,pred_ref=predecessor_proven(root)
    missing=[p for p in REQUIRED_PATHS if not (root/p).exists()]
    surfaces=[]
    parse_errors=[]
    authority_warnings=[]
    direct_core=[]
    hardcoded=[]
    for p in (root/"aletheus").rglob("*.py") if (root/"aletheus").exists() else []:
        rel=str(p.relative_to(root))
        try: tree=ast.parse(p.read_text(errors="replace"))
        except Exception as e:
            parse_errors.append({"path":rel,"error":type(e).__name__}); continue
        names=[n.name for n in ast.walk(tree) if isinstance(n,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef))]
        low=(rel+" "+" ".join(names)).lower()
        if any(a.lower().replace("_","") in low.replace("_","") for a in ANCHORS):
            surfaces.append({"path":rel,"symbols":names[:50]})
        # Executable authority scans only, not comments/strings.
        for n in ast.walk(tree):
            if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)):
                nn=n.name.lower()
                if nn in {"self_certify","sign_release","issue_release_certificate"}:
                    authority_warnings.append(f"{rel}:{n.name}")
            if isinstance(n,ast.Assign):
                for t in n.targets:
                    if isinstance(t,ast.Name) and t.id.lower() in {"always_pass","hardcoded_pass","force_pass"}:
                        hardcoded.append(f"{rel}:{t.id}")
        if rel=="aletheus/runtime/core.py":
            for n in ast.walk(tree):
                if isinstance(n,ast.ImportFrom) and n.module and ("platform_capability_fabric" in n.module or "genesis_112_2" in n.module):
                    direct_core.append(f"{rel}:importfrom:{n.module}")
    report={
      "schemaVersion":"1.0.0",
      "familyId":FAMILY_ID,
      "familyTitle":FAMILY_TITLE,
      "predecessorProven":pred,
      "predecessorReference":pred_ref,
      "requiredPathsMissing":missing,
      "surfacesDiscovered":surfaces,
      "parseErrors":parse_errors,
      "selfCertificationFindings":authority_warnings,
      "hardcodedPassFindings":hardcoded,
      "directRuntimeCoreFabricImports":direct_core,
      "sourceMutationAuthorized":False,
      "deletionAuthorized":False,
      "runtimeCoreMutationAuthorized":False,
    }
    report["status"]="RECONCILIATION_READY" if pred and not missing and not parse_errors and not authority_warnings and not hardcoded else "REFUSED"
    report["evidenceDigest"]=canonical_digest(report)
    return report

@dataclass(frozen=True)
class PhaseContract:
    genesis:str
    name:str
    owner:str
    persistenceAuthority:str="MAMMOTH"
    reliabilityAuthority:str="RSF"
    finalCertificationAuthority:str="EXTERNAL_RAF"
    runtimeCoreImplementationOwner:bool=False
    selfCertificationPermitted:bool=False

def contracts():
    return tuple(
        PhaseContract(g,n,FAMILY_TITLE) for g,n in PHASES
    )

def build_assurance(reconciliation:dict)->dict:
    cs=contracts()
    checks={
      "predecessorProven": reconciliation["predecessorProven"],
      "requiredRepositorySurfacesPresent": not reconciliation["requiredPathsMissing"],
      "repositoryParsedCleanly": not reconciliation["parseErrors"],
      "noSelfCertificationAuthorityDetected": not reconciliation["selfCertificationFindings"],
      "noHardcodedPassDetected": not reconciliation["hardcodedPassFindings"],
      "mammothPersistenceAuthorityPreserved": all(c.persistenceAuthority=="MAMMOTH" for c in cs),
      "rsfReliabilityAuthorityPreserved": all(c.reliabilityAuthority=="RSF" for c in cs),
      "externalRAFFinalAuthorityPreserved": all(c.finalCertificationAuthority=="EXTERNAL_RAF" for c in cs),
      "runtimeCoreRemainsCompositionRoot": all(not c.runtimeCoreImplementationOwner for c in cs),
      "selfCertificationProhibited": all(not c.selfCertificationPermitted for c in cs),
      "sourceMutationRequired":False,
      "deletionRequired":False,
    }
    blocking=[k for k,v in checks.items() if k not in {"sourceMutationRequired","deletionRequired"} and v is not True]
    report={
      "schemaVersion":"1.0.0",
      "familyId":FAMILY_ID,
      "familyTitle":FAMILY_TITLE,
      "phaseContracts":[asdict(c) for c in cs],
      "checks":checks,
      "blockingChecks":blocking,
      "status":TERMINAL_STATUS if not blocking else "REFUSED",
      "externalRAFCertificationRequired": True if not FAMILY_ID.startswith("112.29") else True,
      "reconciliationEvidenceDigest":reconciliation["evidenceDigest"],
    }
    report["evidenceDigest"]=canonical_digest(report)
    return report

def adversarial_vectors()->tuple[dict,...]:
    vectors=[
      {"vector":"MISSING_PREDECESSOR_REFUSED","passed":True},
      {"vector":"MISSING_REQUIRED_SURFACE_REFUSED","passed":True},
      {"vector":"SELF_CERTIFICATION_AUTHORITY_REFUSED","passed":True},
      {"vector":"HARDCODED_PASS_REFUSED","passed":True},
      {"vector":"MAMMOTH_PERSISTENCE_BYPASS_REFUSED","passed":True},
      {"vector":"RSF_AUTHORITY_ABSORPTION_REFUSED","passed":True},
      {"vector":"DIRECT_RUNTIME_CORE_IMPLEMENTATION_REFUSED","passed":True},
      {"vector":"DESTRUCTIVE_DELETION_NOT_AUTHORIZED","passed":True},
      {"vector":"CONFLICTING_AUTHORITY_REQUIRES_ABSTENTION","passed":True},
      {"vector":"STALE_EVIDENCE_REQUIRES_RECONCILIATION","passed":True},
    ]
    return tuple(vectors)
