from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os, re, tempfile

STANDARD="ALETHEUSOS-GENESIS-112.21.2.3-RUNTIMEREGISTRY-AUTHORITY-RESOLUTION"
PREDECESSOR_REPORT="reports/platform-service-fabric/genesis-112.21.2.2/semantic-equivalence-authority-provenance-report.json"
PREDECESSOR_GATE="reports/platform-service-fabric/genesis-112.21.2.2/genesis-112.21.3-entry-gate.json"

RUNTIME_REGISTRY="aletheus/mesh/runtime_registry.py"
COMPARATORS=(
    ("EngineRegistry","aletheus/runtime/registries.py"),
    ("ServiceRegistry.Primary","aletheus/runtime/registries.py"),
    ("ServiceRegistry.Services","aletheus/runtime/services/service_registry.py"),
    ("RegistrationManager","aletheus/runtime/managers/registration_manager.py"),
)

AUTHORITY_CLASSES={
    "MESH_MEMBERSHIP_REGISTRY",
    "PLATFORM_RUNTIME_REGISTRY",
    "COMPATIBILITY_SURFACE",
    "LEGACY_INACTIVE",
    "COMPLEMENTARY_REGISTRY",
    "INSUFFICIENT_EVIDENCE",
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

def parse(path):
    try: return ast.parse(path.read_text(encoding="utf-8",errors="replace"))
    except Exception: return None

def name(node):
    if isinstance(node,ast.Name): return node.id
    if isinstance(node,ast.Attribute):
        left=name(node.value)
        return f"{left}.{node.attr}" if left else node.attr
    return ""

def public_surface(path):
    tree=parse(path)
    if tree is None:
        return {"parseable":False,"classes":[],"functions":[],"imports":[],"methods":[]}
    imports=[]; classes=[]; functions=[]; methods=[]
    for n in tree.body:
        if isinstance(n,ast.Import):
            imports.extend(x.name for x in n.names)
        elif isinstance(n,ast.ImportFrom):
            imports.append(n.module or "")
        elif isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and not n.name.startswith("_"):
            functions.append(n.name)
        elif isinstance(n,ast.ClassDef):
            cm=[]
            for m in n.body:
                if isinstance(m,(ast.FunctionDef,ast.AsyncFunctionDef)) and not m.name.startswith("_"):
                    cm.append({
                        "name":m.name,
                        "args":[a.arg for a in m.args.args],
                        "async":isinstance(m,ast.AsyncFunctionDef),
                        "calls":sorted({name(x.func) for x in ast.walk(m) if isinstance(x,ast.Call) and name(x.func)}),
                    })
            classes.append({"name":n.name,"methods":cm})
            if n.name=="RuntimeRegistry":
                methods=cm
    if not methods and len(classes)==1:
        methods=classes[0]["methods"]
    return {"parseable":True,"classes":classes,"functions":functions,
            "imports":sorted(set(imports)),"methods":methods}

def source_files(root):
    # Only executable/source evidence counts toward authority.
    # Reports, package evidence, docs and generated artifacts are intentionally excluded.
    roots=[root/"aletheus",root/"tests"]
    for base in roots:
        if not base.exists(): continue
        for p in base.rglob("*.py"):
            if any(x in p.parts for x in (".git",".venv","venv","__pycache__","node_modules")): continue
            if "platform_service_fabric" in p.parts and "genesis_112_21" in "/".join(p.parts):
                # Do not let reconciliation analyzers create self-referential authority evidence.
                continue
            yield p

def repo_usage(root, rel, symbol_hint):
    module=rel.replace("/",".").removesuffix(".py")
    imported_by=[]; tests=[]; core=[]; mesh=[]; distributed=[]; registration=[]; instantiation=[]
    for p in source_files(root):
        try:
            r=str(p.relative_to(root)); txt=p.read_text(encoding="utf-8",errors="replace")
        except Exception:
            continue
        if r==rel: continue
        if not (symbol_hint in txt or module in txt or re.search(r"\bfrom\s+aletheus\.mesh\.runtime_registry\b|\bimport\s+aletheus\.mesh\.runtime_registry\b",txt)):
            continue
        imported_by.append(r)
        if r.startswith("tests/") or "/tests/" in f"/{r}/": tests.append(r)
        if r=="aletheus/runtime/core.py": core.append(r)
        if "/mesh/" in f"/{r}/": mesh.append(r)
        if "distributed" in r.lower(): distributed.append(r)
        if "register" in txt.lower(): registration.append(r)
        if re.search(r"\bRuntimeRegistry\s*\(",txt): instantiation.append(r)
    return {k:sorted(set(v)) for k,v in {
      "importedBy":imported_by,"testReferences":tests,"runtimeCoreReferences":core,
      "meshReferences":mesh,"distributedReferences":distributed,
      "registrationReferences":registration,"instantiationReferences":instantiation}.items()}

def token_semantics(surface, text):
    words=set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*",text.lower()))
    methods={m["name"].lower() for m in surface.get("methods",[])}
    mesh_terms={"node","peer","heartbeat","member","membership","cluster","mesh","remote","endpoint","lease"}
    platform_terms={"service","engine","capability","runtime","command","application","provider"}
    return {
      "meshSignals":sorted((words|methods)&mesh_terms),
      "platformSignals":sorted((words|methods)&platform_terms),
    }

def compare_methods(left,right):
    L={m["name"] for m in left.get("methods",[])}
    R={m["name"] for m in right.get("methods",[])}
    return {"shared":sorted(L&R),"runtimeRegistryOnly":sorted(L-R),"comparatorOnly":sorted(R-L),
            "overlapRatio":round(len(L&R)/max(1,len(L|R)),4)}

class RuntimeRegistryAuthorityResolver:
    @staticmethod
    def load_predecessor(root):
        rp=root/PREDECESSOR_REPORT
        gp=root/PREDECESSOR_GATE
        if not rp.exists(): raise RuntimeError(f"missing predecessor semantic report: {rp}")
        if not gp.exists(): raise RuntimeError(f"missing predecessor entry gate: {gp}")
        report=json.loads(rp.read_text())
        gate=json.loads(gp.read_text())
        if not report.get("evidenceDigest"): raise RuntimeError("predecessor semantic evidence digest missing")
        if "RuntimeRegistry" not in gate.get("foundationalBlockers",[]):
            raise RuntimeError("RuntimeRegistry is not the declared predecessor foundational blocker")
        return report,gate

    @classmethod
    def resolve(cls, project_root):
        root=Path(project_root).resolve()
        predecessor,gate=cls.load_predecessor(root)
        rr=root/RUNTIME_REGISTRY

        comparisons=[]
        if not rr.exists():
            authority="LEGACY_INACTIVE"
            disposition="EXCLUDE_FROM_112_21_3_PLATFORM_AUTHORITY"
            blocker=False
            confidence=95
            reason="RuntimeRegistry surface is absent; it cannot own current platform runtime authority."
            evidence={"exists":False}
        else:
            text=rr.read_text(encoding="utf-8",errors="replace")
            surf=public_surface(rr)
            usage=repo_usage(root,RUNTIME_REGISTRY,"RuntimeRegistry")
            semantics=token_semantics(surf,text)
            for ident,rel in COMPARATORS:
                p=root/rel
                if p.exists():
                    comparisons.append({
                        "identity":ident,
                        "path":rel,
                        "methodComparison":compare_methods(surf,public_surface(p))
                    })
            evidence={
              "exists":True,
              "sha256":"sha256:"+hashlib.sha256(rr.read_bytes()).hexdigest(),
              "surface":surf,
              "usage":usage,
              "semanticSignals":semantics,
            }

            live_source_refs=len(usage["importedBy"])
            runtime_refs=len(usage["runtimeCoreReferences"])
            reg_refs=len(usage["registrationReferences"])
            inst_refs=len(usage["instantiationReferences"])
            mesh_refs=len(usage["meshReferences"])+len(usage["distributedReferences"])
            use_score=live_source_refs+2*runtime_refs+2*reg_refs+2*inst_refs
            mesh_score=mesh_refs+len(semantics["meshSignals"])
            platform_score=runtime_refs+reg_refs+len(semantics["platformSignals"])
            max_overlap=max([c["methodComparison"]["overlapRatio"] for c in comparisons] or [0.0])

            if use_score==0:
                authority="LEGACY_INACTIVE"
                disposition="PRESERVE_AS_NON_CANONICAL_DORMANT_SURFACE"
                blocker=False
                confidence=92
                reason="No live source imports, registration references, runtime-core references, or instantiations were detected."
            elif mesh_score>=platform_score+3 and runtime_refs==0:
                authority="MESH_MEMBERSHIP_REGISTRY"
                disposition="EXCLUDE_FROM_PLATFORM_SERVICE_REGISTRY_AUTHORITY_AND_PRESERVE_FOR_MESH"
                blocker=False
                confidence=88
                reason="Usage and semantic signals are predominantly mesh/distributed membership oriented."
            elif runtime_refs>0 and reg_refs>=2 and platform_score>mesh_score:
                authority="PLATFORM_RUNTIME_REGISTRY"
                disposition="BIND_EXPLICITLY_IN_112_21_3_WITH_CONTRACT_TESTS"
                blocker=False
                confidence=82
                reason="Live runtime-core and registration evidence supports platform runtime authority."
            elif max_overlap>=0.65 and use_score>0:
                authority="COMPLEMENTARY_REGISTRY"
                disposition="COMPOSE_WITH_EXISTING_REGISTRIES_BEHIND_EXPLICIT_BOUNDARY"
                blocker=False
                confidence=80
                reason="Live usage exists and public-method overlap with another registry is substantial."
            elif use_score<=2 and mesh_score==0 and platform_score==0:
                authority="COMPATIBILITY_SURFACE"
                disposition="PRESERVE_AS_COMPATIBILITY_SURFACE_PENDING_CALLSITE_PROOF"
                blocker=False
                confidence=75
                reason="Very weak live usage and no authority signals indicate a compatibility-oriented surface."
            else:
                authority="INSUFFICIENT_EVIDENCE"
                disposition="ABSTAIN"
                blocker=True
                confidence=55
                reason="Evidence does not safely distinguish platform authority from mesh/compatibility responsibility."

        out={
          "schemaVersion":"1.0.0",
          "standard":STANDARD,
          "generatedAtIso":datetime.now(timezone.utc).isoformat(),
          "predecessorSemanticEvidenceDigest":predecessor["evidenceDigest"],
          "predecessorEntryGateDigest":gate.get("evidenceDigest"),
          "runtimeRegistry":{
            "path":RUNTIME_REGISTRY,
            "authorityClassification":authority,
            "architecturalDisposition":disposition,
            "confidence":confidence,
            "reason":reason,
            "evidence":evidence,
            "comparisons":comparisons
          },
          "constitutionalFinding":{
            "platformAuthorityGrantedByNameAlone":False,
            "sourceMutationAuthorized":False,
            "runtimeCoreMutationAuthorized":False,
            "deletionAuthorized":False,
            "existingMeshCapabilityPreserved":True,
            "existingRegistryCapabilitiesPreserved":True
          },
          "foundationalBlockers":["RuntimeRegistry"] if blocker else [],
          "genesis11221_3EntryPermitted":not blocker,
          "entryConditions":[
            "ServiceRegistry complementary surfaces are composed, not blindly collapsed.",
            "RuntimeInspector distinct capabilities are composed by capability.",
            "LifecycleManager, RegistrationManager and EngineRegistry receive explicit bounded contracts.",
            "RSF reliability observation remains RSF-owned behind a bounded evidence interface.",
            "No runtime/core.py mutation is performed merely to satisfy the entry gate.",
            "Contract tests are required before canonical binding."
          ],
          "status":"RUNTIMEREGISTRY_AUTHORITY_RESOLVED" if not blocker else "RUNTIMEREGISTRY_AUTHORITY_UNRESOLVED"
        }
        out["evidenceDigest"]=digest(out)
        return out

    @classmethod
    def write(cls, project_root):
        root=Path(project_root).resolve()
        result=cls.resolve(root)
        dest=root/"reports/platform-service-fabric/genesis-112.21.2.3"
        atomic_json(dest/"runtime-registry-authority-resolution.json",result)
        atomic_json(dest/"genesis-112.21.3-entry-gate.json",{
          "schemaVersion":"1.0.0",
          "entryPermitted":result["genesis11221_3EntryPermitted"],
          "foundationalBlockers":result["foundationalBlockers"],
          "runtimeRegistryAuthorityClassification":result["runtimeRegistry"]["authorityClassification"],
          "runtimeRegistryArchitecturalDisposition":result["runtimeRegistry"]["architecturalDisposition"],
          "sourceMutationPermitted":False,
          "runtimeCoreMutationPermitted":False,
          "contractTestsRequired":True,
          "entryConditions":result["entryConditions"],
          "evidenceDigest":result["evidenceDigest"]
        })
        return result
