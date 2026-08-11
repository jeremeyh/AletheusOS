from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os, tempfile

STANDARD="ALETHEUSOS-GENESIS-112.21.2.2-SEMANTIC-EQUIVALENCE-AUTHORITY-PROVENANCE"
PREDECESSOR="reports/platform-service-fabric/genesis-112.21.2.1/critical-service-resolution-map.json"

FOUNDATIONAL=("ServiceRegistry","RuntimeInspector","LifecycleManager","RuntimeRegistry")
CONTEXTUAL=("RegistrationManager","EngineRegistry","RuntimeReliabilityObservationFabric")
SEMANTIC_CLASSES={
 "SEMANTICALLY_EQUIVALENT","SUPERSET","SUBSET","COMPATIBILITY_FACADE","DELEGATE",
 "COMPLEMENTARY","CONFLICTING_AUTHORITY","DISTINCT_CAPABILITY","INSUFFICIENT_EVIDENCE"
}
DISPOSITIONS={
 "REUSE","COMPOSE","REFACTOR","PROMOTE_CANDIDATE_PENDING_PRESERVATION_PROOF",
 "DEPRECATE_CANDIDATE_PENDING_CALLSITE_MIGRATION","ABSTAIN"
}

def digest(obj):
    raw=json.dumps(obj,sort_keys=True,separators=(",",":"),default=str).encode()
    return "sha256:"+hashlib.sha256(raw).hexdigest()

def atomic_json(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    data=json.dumps(obj,indent=2,sort_keys=True,default=str).encode()
    fd,tmp=tempfile.mkstemp(prefix=path.name+".",dir=path.parent)
    try:
        with os.fdopen(fd,"wb") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def _parse(path):
    try: return ast.parse(path.read_text(encoding="utf-8",errors="replace"))
    except Exception: return None

def _name(n):
    if isinstance(n,ast.Name): return n.id
    if isinstance(n,ast.Attribute): return _name(n.value)+"."+n.attr
    if isinstance(n,ast.Call): return _name(n.func)
    return ""

def _method(m):
    args=[a.arg for a in m.args.args]
    calls=sorted({_name(n.func) for n in ast.walk(m) if isinstance(n,ast.Call) and _name(n.func)})
    raises=sorted({_name(n.exc) for n in ast.walk(m) if isinstance(n,ast.Raise) and n.exc})
    writes=sorted({n.attr for n in ast.walk(m) if isinstance(n,ast.Attribute) and isinstance(n.ctx,ast.Store)})
    return {"name":m.name,"async":isinstance(m,ast.AsyncFunctionDef),"args":args,
            "calls":calls,"raises":raises,"stateWrites":writes}

def surface(path, identity):
    tree=_parse(path)
    if tree is None:
        return {"parseable":False,"identity":identity,"publicMethods":[],"classes":[],"imports":[]}
    imports=[]; classes=[]; methods=[]; top=[]; assignments=[]
    for n in tree.body:
        if isinstance(n,ast.Import): imports += [x.name for x in n.names]
        elif isinstance(n,ast.ImportFrom): imports.append(n.module or "")
        elif isinstance(n,ast.ClassDef):
            cm=[_method(x) for x in n.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef)) and not x.name.startswith("_")]
            classes.append({"name":n.name,"bases":[_name(x) for x in n.bases],"publicMethods":cm})
            if n.name==identity: methods=cm
        elif isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and not n.name.startswith("_"):
            top.append(_method(n))
        elif isinstance(n,(ast.Assign,ast.AnnAssign)):
            assignments.append(getattr(n,"lineno",0))
    if not methods and len(classes)==1: methods=classes[0]["publicMethods"]
    return {"parseable":True,"identity":identity,"classes":classes,"publicMethods":methods,
            "topLevelPublicFunctions":top,"imports":sorted(set(imports)),
            "moduleAssignments":assignments}

def repository_evidence(root, rel, identity):
    module=rel.replace("/",".").removesuffix(".py")
    importers=[]; tests=[]; core=[]; registrars=[]; instantiators=[]
    for p in root.rglob("*.py"):
        if any(x in p.parts for x in (".git",".venv","__pycache__")): continue
        try: r=str(p.relative_to(root)); txt=p.read_text(encoding="utf-8",errors="replace")
        except Exception: continue
        if r==rel: continue
        if identity in txt or module in txt:
            importers.append(r)
            if "/tests/" in f"/{r}/" or r.startswith("tests/"): tests.append(r)
            if r=="aletheus/runtime/core.py": core.append(r)
            if "register" in txt.lower(): registrars.append(r)
            if f"{identity}(" in txt: instantiators.append(r)
    return {k:sorted(set(v)) for k,v in {
        "importedBy":importers,"testReferences":tests,"runtimeCoreReferences":core,
        "registrationReferences":registrars,"instantiationReferences":instantiators}.items()}

def compare(a,b):
    am={x["name"]:x for x in a.get("publicMethods",[])}
    bm={x["name"]:x for x in b.get("publicMethods",[])}
    A=set(am); B=set(bm)
    shared=A&B
    sigdiff=[m for m in shared if (am[m]["args"],am[m]["async"]) != (bm[m]["args"],bm[m]["async"])]
    return {
      "leftOnlyMethods":sorted(A-B),"rightOnlyMethods":sorted(B-A),"sharedMethods":sorted(shared),
      "signatureDifferences":sorted(sigdiff),
      "leftImportsOnly":sorted(set(a.get("imports",[]))-set(b.get("imports",[]))),
      "rightImportsOnly":sorted(set(b.get("imports",[]))-set(a.get("imports",[]))),
      "methodSetEqual":A==B,"signatureCompatible":not sigdiff,
      "leftSuperset":bool(A>B),"rightSuperset":bool(B>A)
    }

def semantic_class(candidates):
    if len(candidates)<2: return "INSUFFICIENT_EVIDENCE"
    c=compare(candidates[0]["surface"],candidates[1]["surface"])
    if c["methodSetEqual"] and c["signatureCompatible"]: return "SEMANTICALLY_EQUIVALENT"
    if c["leftSuperset"] or c["rightSuperset"]: return "SUPERSET"
    if c["sharedMethods"] and (c["leftOnlyMethods"] or c["rightOnlyMethods"]): return "COMPLEMENTARY"
    return "DISTINCT_CAPABILITY"

def disposition(identity, sem, candidates):
    if len(candidates)==1:
        ev=candidates[0]["evidence"]
        active=len(ev["importedBy"])+len(ev["registrationReferences"])+len(ev["runtimeCoreReferences"])
        if identity=="RuntimeReliabilityObservationFabric":
            return "REFACTOR", "RSF-owned observation surface must remain behind a bounded reliability evidence interface."
        if active>=3: return "REFACTOR", "Single active implementation; formalize authority/lifecycle contract before binding."
        return "ABSTAIN", "Single implementation lacks sufficient live integration evidence for canonical binding."
    if sem=="SEMANTICALLY_EQUIVALENT":
        return "PROMOTE_CANDIDATE_PENDING_PRESERVATION_PROOF", "Surfaces appear equivalent; provenance and call-site migration proof are still required before canonical promotion."
    if sem=="SUPERSET":
        return "PROMOTE_CANDIDATE_PENDING_PRESERVATION_PROOF", "One public surface is a superset; behavioral and compatibility preservation remain unproven."
    if sem in ("COMPLEMENTARY","DISTINCT_CAPABILITY"):
        return "COMPOSE", "Competing surfaces expose materially distinct capability; preserve both behind explicit authority boundaries unless deeper evidence proves duplication."
    return "ABSTAIN", "Semantic evidence is insufficient or conflicting."

class SemanticAuthorityResolver:
    @staticmethod
    def load_prior(root):
        p=root/PREDECESSOR
        if not p.exists(): raise RuntimeError(f"missing predecessor critical map: {p}")
        data=json.loads(p.read_text())
        if not data.get("evidenceDigest"): raise RuntimeError("predecessor evidence digest missing")
        return data

    @classmethod
    def resolve(cls, project_root):
        root=Path(project_root).resolve()
        prior=cls.load_prior(root)
        prior_map={d.get("identity"):d for d in prior.get("criticalDecisions",[])}
        identities=[x for x in FOUNDATIONAL+CONTEXTUAL if x in prior_map]
        decisions=[]
        for identity in identities:
            old=prior_map[identity]
            cs=[]
            for raw in old.get("candidates",[]):
                rel=raw.get("path") if isinstance(raw,dict) else raw
                p=root/rel
                s=surface(p,identity) if p.exists() else {"parseable":False,"publicMethods":[]}
                cs.append({"path":rel,"exists":p.exists(),"sha256":("sha256:"+hashlib.sha256(p.read_bytes()).hexdigest()) if p.exists() else None,
                           "surface":s,"evidence":repository_evidence(root,rel,identity) if p.exists() else {}})
            sem=semantic_class(cs)
            disp,why=disposition(identity,sem,cs)
            pair=compare(cs[0]["surface"],cs[1]["surface"]) if len(cs)>=2 else None
            decisions.append({
              "identity":identity,"priority":"FOUNDATIONAL" if identity in FOUNDATIONAL else "CONTEXTUAL",
              "predecessorResolution":old.get("resolution"),"semanticClassification":sem,
              "architecturalDisposition":disp,"reason":why,"candidates":cs,
              "capabilityPreservationMatrix":pair,
              "authorityQuestions":[
                "Which component owns registration authority?",
                "Which component owns lifecycle transitions?",
                "Which direction may dependencies flow?",
                "Is this a runtime composition surface, domain service, compatibility facade, or observation-only surface?"
              ],
              "mutationGate":{
                "sourceMutationAuthorized":False,"canonicalPromotionAuthorized":False,"deletionAuthorized":False,
                "requiresContractTests":True,"requiresCallsiteMigrationProof":len(cs)>1,
                "requiresCapabilityPreservationProof":len(cs)>1
              }
            })
        blockers=[d["identity"] for d in decisions if d["priority"]=="FOUNDATIONAL" and d["architecturalDisposition"]=="ABSTAIN"]
        out={
          "schemaVersion":"1.0.0","standard":STANDARD,"generatedAtIso":datetime.now(timezone.utc).isoformat(),
          "predecessorCriticalMapDigest":prior["evidenceDigest"],
          "semanticVocabulary":sorted(SEMANTIC_CLASSES),"dispositionVocabulary":sorted(DISPOSITIONS),
          "decisions":decisions,"foundationalBlockers":blockers,
          "sourceMutationAuthorized":False,"canonicalPromotionAuthorized":False,"deletionAuthorized":False,
          "runtimeCoreMutationAuthorized":False,
          "status":"SEMANTIC_AUTHORITY_PROVENANCE_EVIDENCE_READY" if not blockers else "ABSTENTION_REMAINS",
          "nextGate":"GENESIS_112_21_3_CONTRACT_BINDING_ONLY_AFTER_FOUNDATIONAL_ABSTENTIONS_RESOLVED"
        }
        out["evidenceDigest"]=digest(out)
        return out

    @classmethod
    def write(cls, project_root):
        root=Path(project_root).resolve()
        out=cls.resolve(root)
        dest=root/"reports/platform-service-fabric/genesis-112.21.2.2"
        atomic_json(dest/"semantic-equivalence-authority-provenance-report.json",out)
        atomic_json(dest/"capability-preservation-matrix.json",{
          "schemaVersion":"1.0.0",
          "predecessorCriticalMapDigest":out["predecessorCriticalMapDigest"],
          "matrices":[{"identity":d["identity"],"semanticClassification":d["semanticClassification"],
                       "architecturalDisposition":d["architecturalDisposition"],
                       "matrix":d["capabilityPreservationMatrix"]} for d in out["decisions"]],
          "evidenceDigest":digest([d["capabilityPreservationMatrix"] for d in out["decisions"]])
        })
        atomic_json(dest/"genesis-112.21.3-entry-gate.json",{
          "entryPermitted":not bool(out["foundationalBlockers"]),
          "foundationalBlockers":out["foundationalBlockers"],
          "sourceMutationPermitted":False,
          "contractTestScaffoldingRequired":True,
          "evidenceDigest":out["evidenceDigest"]
        })
        return out
