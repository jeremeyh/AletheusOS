from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import ast, hashlib, json, os, re, tempfile

STANDARD="ALETHEUSOS-GENESIS-112.21.2.1-CANONICAL-SERVICE-EVIDENCE-RESOLUTION"

CRITICAL_IDENTITIES={
    "ServiceRegistry","RuntimeInspector","EngineRegistry","RegistrationManager","LifecycleManager",
    "RuntimeRegistry","RuntimeBootValidator","RuntimeInvariantEngine","RuntimeDiagnostics","RuntimeDoctor",
    "RuntimeHardening","ApplicationRuntime","IntelligenceDispatcher","CompatibilityRegistry",
    "RuntimePluginManager","RuntimePlugin","HeartbeatService","AletheusDistributedRuntimeFabric",
    "AletheusAutonomousAgentRuntime","AletheusPluginManager","AletheusRuntimeSDK",
    "RuntimeReliabilityObservationFabric",
}

NON_SERVICE_PATTERNS=(
    re.compile(r"^_cmd_",re.I),
    re.compile(r"(Report|Metric|Health)$",re.I),
)

def canonical_digest(obj)->str:
    raw=json.dumps(obj,sort_keys=True,separators=(",",":"),default=str).encode()
    return "sha256:"+hashlib.sha256(raw).hexdigest()

def atomic_json(path:Path,obj)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    data=json.dumps(obj,indent=2,sort_keys=True,default=str).encode()
    fd,tmp=tempfile.mkstemp(prefix=path.name+".",dir=path.parent)
    try:
        with os.fdopen(fd,"wb") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def parse_file(p:Path):
    try: return ast.parse(p.read_text(encoding="utf-8",errors="replace"))
    except Exception: return None

def module_symbols(tree):
    classes=[]; funcs=[]; imports=[]; calls=[]; assignments=[]
    if tree is None: return classes,funcs,imports,calls,assignments
    for n in ast.walk(tree):
        if isinstance(n,ast.ClassDef): classes.append(n.name)
        elif isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)): funcs.append(n.name)
        elif isinstance(n,ast.Import): imports.extend(x.name for x in n.names)
        elif isinstance(n,ast.ImportFrom): imports.append(n.module or "")
        elif isinstance(n,ast.Call):
            if isinstance(n.func,ast.Name): calls.append(n.func.id)
            elif isinstance(n.func,ast.Attribute): calls.append(n.func.attr)
        elif isinstance(n,(ast.Assign,ast.AnnAssign)):
            assignments.append(getattr(n,"lineno",0))
    return classes,funcs,imports,calls,assignments

class DeepEvidenceResolver:
    @staticmethod
    def load_decision_map(project:Path)->dict:
        p=project/"reports/platform-service-fabric/genesis-112.21.2/service-architecture-decision-map.json"
        if not p.exists(): raise RuntimeError(f"missing predecessor decision map: {p}")
        return json.loads(p.read_text())

    @classmethod
    def resolve(cls, project_root:str|Path)->dict:
        root=Path(project_root).resolve()
        prior=cls.load_decision_map(root)
        decisions=[]
        for d in prior.get("decisions",[]):
            ident=d.get("identity","")
            if any(p.search(ident) for p in NON_SERVICE_PATTERNS):
                decisions.append({
                    "identity":ident,"priorClassification":d.get("classification"),
                    "resolution":"OUT_OF_SCOPE_PLATFORM_COMMAND_OR_TELEMETRY",
                    "canonicalCandidate":None,"confidence":95,
                    "reason":"Not a service architecture authority identity; exclude from service canonicalization."
                })
                continue
            if ident not in CRITICAL_IDENTITIES and d.get("classification")=="ABSTAIN":
                continue
            candidates=[]
            for rel in d.get("candidates",[]):
                p=root/rel
                tree=parse_file(p) if p.exists() else None
                classes,funcs,imports,calls,assignments=module_symbols(tree)
                text=p.read_text(encoding="utf-8",errors="replace") if p.exists() else ""
                candidates.append({
                    "path":rel,
                    "exists":p.exists(),
                    "classes":classes,
                    "functions":funcs,
                    "imports":imports,
                    "calls":calls,
                    "testReferences":0,
                    "runtimeCoreReferences":0,
                    "registrationReferences":0,
                    "importedBy":[],
                    "sha256":"sha256:"+hashlib.sha256(text.encode()).hexdigest() if p.exists() else None,
                })
            # repository-wide import/call evidence
            pyfiles=[p for p in root.rglob("*.py") if ".git" not in p.parts and "__pycache__" not in p.parts and ".venv" not in p.parts]
            for c in candidates:
                base=Path(c["path"]).stem
                symbol=ident
                for p in pyfiles:
                    try: txt=p.read_text(encoding="utf-8",errors="replace")
                    except Exception: continue
                    if p.as_posix().endswith(c["path"]): continue
                    if symbol in txt or c["path"].replace("/",".").removesuffix(".py") in txt:
                        c["importedBy"].append(str(p.relative_to(root)))
                    if "aletheus/runtime/core.py" in str(p):
                        c["runtimeCoreReferences"] += txt.count(symbol)
                    if "/tests/" in f"/{p.relative_to(root)}/":
                        c["testReferences"] += txt.count(symbol)
                    if "register" in txt.lower():
                        c["registrationReferences"] += txt.count(symbol)
                c["importedBy"]=sorted(set(c["importedBy"]))[:200]

            resolution="ABSTAIN"
            canonical=None
            confidence=55
            reason="Evidence remains insufficient for safe canonical selection."
            if len(candidates)==1:
                c=candidates[0]
                weight=len(c["importedBy"])+2*c["testReferences"]+2*c["runtimeCoreReferences"]+c["registrationReferences"]
                if weight>=8:
                    resolution="REUSE"
                    canonical=c["path"]; confidence=85
                    reason="Single implementation has strong repository integration evidence."
                elif weight>=3:
                    resolution="REFACTOR"
                    canonical=c["path"]; confidence=78
                    reason="Single implementation is active but boundary/lifecycle contract should be formalized."
            elif len(candidates)>1:
                scores=[]
                for c in candidates:
                    score=len(c["importedBy"])+2*c["testReferences"]+2*c["runtimeCoreReferences"]+c["registrationReferences"]
                    scores.append((score,c))
                scores.sort(key=lambda x:x[0], reverse=True)
                if len(scores)>=2 and scores[0][0]>=max(6,scores[1][0]*2+2):
                    resolution="PROMOTE_CANDIDATE_PENDING_PRESERVATION_PROOF"
                    canonical=scores[0][1]["path"]; confidence=84
                    reason="One implementation strongly dominates integration evidence, but weaker candidate capability must be preserved or intentionally retired."
                else:
                    resolution="ABSTAIN"
                    confidence=60
                    reason="Competing implementations remain too close to select safely."

            decisions.append({
                "identity":ident,
                "priorClassification":d.get("classification"),
                "resolution":resolution,
                "canonicalCandidate":canonical,
                "confidence":confidence,
                "reason":reason,
                "candidates":candidates,
                "requiredBeforeMutation":[
                    "confirm authority owner",
                    "confirm lifecycle semantics",
                    "confirm registration path",
                    "confirm dependency direction",
                    "confirm capability preservation for competing candidates",
                ] if resolution!="OUT_OF_SCOPE_PLATFORM_COMMAND_OR_TELEMETRY" else []
            })
        out={
            "schemaVersion":"1.0.0","standard":STANDARD,
            "generatedAtIso":datetime.now(timezone.utc).isoformat(),
            "predecessorEvidenceDigest":prior.get("evidenceDigest"),
            "decisions":decisions,
            "summary":{},
            "sourceMutationAuthorized":False,
            "canonicalPromotionAuthorized":False,
            "deletionAuthorized":False,
            "status":"CANONICAL_SERVICE_EVIDENCE_DOSSIER_READY"
        }
        for d in decisions:
            out["summary"][d["resolution"]]=out["summary"].get(d["resolution"],0)+1
        out["evidenceDigest"]=canonical_digest(out)
        return out

    @classmethod
    def write(cls, project_root:str|Path)->dict:
        root=Path(project_root).resolve()
        out=cls.resolve(root)
        dest=root/"reports/platform-service-fabric/genesis-112.21.2.1"
        atomic_json(dest/"canonical-service-evidence-resolution-dossier.json",out)
        critical=[d for d in out["decisions"] if d["identity"] in CRITICAL_IDENTITIES]
        atomic_json(dest/"critical-service-resolution-map.json",{
            "schemaVersion":"1.0.0","criticalDecisions":critical,
            "evidenceDigest":canonical_digest(critical)
        })
        return out
