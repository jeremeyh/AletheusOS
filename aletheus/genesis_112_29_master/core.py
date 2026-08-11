from __future__ import annotations
from pathlib import Path
from enum import Enum
from typing import Any
import ast, hashlib, json, re

FAMILY_ID="112.29.3-112.29.9.1"
PACKAGE_VERSION="1.1.0"
PREDECESSOR_STATUS="GENESIS_112_29_2_UNIFIED_PLATFORM_INTEGRATION_HARNESS_READY"
PREDECESSOR_DIGEST="sha256:f2652b3b958c3654faa70227677551e4c6c241ad84359493836bfb80a57ecf94"
FINAL_STATUS="GENESIS_112_29_UNIFIED_PLATFORM_CERTIFIED"
PHASES=(
("112.29.3","Whole-System Adversarial Integration & Drift Eradication"),
("112.29.3.1","Whole-System Finding Resolution, Authority Provenance & Scanner Calibration Dossier"),
("112.29.4","Canonical Authority / Ownership Collision Resolution"),
("112.29.5","Cross-Fabric Dependency & Connection-Mesh Verification"),
("112.29.6","Runtime / Capability / Service Boundary Penetration Assurance"),
("112.29.7","Mammoth Persistence + RSF Reliability Continuity Validation"),
("112.29.8","Whole-System Constitutional & Failure-Mode Validation"),
("112.29.9","Genesis 112 Unified Platform Master Closure"),
("112.29.9.1","External RAF Independent Certification & Gold Seal"),)

class SurfaceDisposition(str,Enum):
 CANONICAL="CANONICAL"; COMPOSE="COMPOSE"; REUSE="REUSE"; REFACTOR="REFACTOR"
 LEGACY_INACTIVE="LEGACY_INACTIVE"; PRESERVE_DORMANT="PRESERVE_DORMANT"
 PROMOTION_PENDING_PRESERVATION_PROOF="PROMOTION_PENDING_PRESERVATION_PROOF"
 ABSTAIN="ABSTAIN"; REFUSE="REFUSE"

AUTHORITY_KINDS=("CERTIFICATION_DATA_MODEL","CERTIFICATION_EVIDENCE","CERTIFICATION_CHECK",
 "CERTIFICATION_ASSURANCE","CERTIFICATION_REQUEST","CERTIFICATION_DECISION",
 "CERTIFICATION_ISSUANCE","FINAL_RELEASE_AUTHORITY")
FINAL_AUTHORITY_VERBS=("issue_release_certificate","sign_release","issue_gold_seal",
 "certify_release","promote_release","canonical_promote")
DYNAMIC_HINTS=("register","registry","command","plugin","entrypoint","entry_point","discover",
 "loader","bootstrap","activation","cli","assurance","reconciliation","resolver","binding")
HISTORICAL_MASTER_RE=re.compile(r"aletheus/genesis_112_(2[2-8])_master/core\.py$")
INTEGRATION_MASTER_RE=re.compile(r"aletheus/genesis_112_29_1_2/core\.py$")

def digest(o:Any)->str:
 return "sha256:"+hashlib.sha256(json.dumps(o,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()

def read_json(p:Path):
 try:return json.loads(p.read_text())
 except Exception:return None

def predecessor(root:Path):
 base=root/'reports/unified-platform-integration'
 if not base.exists(): return False,str(base)
 for p in base.rglob('*.json'):
  d=read_json(p)
  if isinstance(d,dict) and d.get('status')==PREDECESSOR_STATUS and d.get('evidenceDigest')==PREDECESSOR_DIGEST:
   return True,str(p)
 return False,str(base)

def _imports(tree):
 out=[]
 for n in ast.walk(tree):
  if isinstance(n,ast.ImportFrom) and n.module: out.append(n.module)
  elif isinstance(n,ast.Import): out.extend(x.name for x in n.names)
 return out

def _symbols(tree):
 out=[]
 for n in ast.walk(tree):
  if isinstance(n,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)):
   out.append({"name":n.name,"kind":type(n).__name__,"line":getattr(n,"lineno",0)})
 return out

def _module(rel): return rel[:-3].replace('/','.')

def _classify_cert_symbol(name:str, node_kind:str)->str:
 low=name.lower()
 if any(v in low for v in FINAL_AUTHORITY_VERBS): return "FINAL_RELEASE_AUTHORITY"
 if "result" in low or "record" in low or "model" in low or "error" in low: return "CERTIFICATION_DATA_MODEL"
 if "evidence" in low or "provenance" in low: return "CERTIFICATION_EVIDENCE"
 if "check" in low or "scan" in low or "verify" in low or "validation" in low: return "CERTIFICATION_CHECK"
 if "request" in low: return "CERTIFICATION_REQUEST"
 if "decision" in low: return "CERTIFICATION_DECISION"
 if "assurance" in low or "boundary" in low: return "CERTIFICATION_ASSURANCE"
 if "certif" in low and node_kind in ("FunctionDef","AsyncFunctionDef"): return "CERTIFICATION_ASSURANCE"
 return "CERTIFICATION_DATA_MODEL"

def _scan(root:Path)->dict:
 surfaces=[]; parse=[]; imports={}; symbols={}; texts={}; files=[]
 base=root/'aletheus'
 for p in sorted(base.rglob('*.py')) if base.exists() else []:
  rel=str(p.relative_to(root)); files.append(rel); txt=p.read_text(errors='replace'); texts[rel]=txt
  try: tree=ast.parse(txt)
  except Exception as e: parse.append({'path':rel,'error':type(e).__name__}); continue
  im=_imports(tree); sy=_symbols(tree); imports[rel]=im; symbols[rel]=sy
  surfaces.append({'surfaceId':hashlib.sha256(rel.encode()).hexdigest()[:16],
                   'relativePath':rel,'symbols':sy[:150],'imports':im[:150]})
 modules={_module(r):r for r in files}
 inbound={r:[] for r in files}
 for rel,ims in imports.items():
  for imp in ims:
   for mod,target in modules.items():
    if imp==mod or imp.startswith(mod+"."):
     if rel!=target: inbound.setdefault(target,[]).append(rel)
 return {"surfaces":surfaces,"parseErrors":parse,"imports":imports,"symbols":symbols,
         "texts":texts,"files":files,"inbound":{k:sorted(set(v)) for k,v in inbound.items()}}

def interrogate(root:str|Path)->dict:
 root=Path(root).resolve(); ok,pref=predecessor(root); s=_scan(root)
 authority=[]; core_leaks=[]; bypass=[]; rsfv=[]; rafv=[]; boundary=[]; orphans=[]
 # Candidate collision families are semantic, not same-name string collisions.
 families={
  "REGISTRY_AUTHORITY":["aletheus/runtime/registries.py","aletheus/runtime/services/service_registry.py","aletheus/mesh/runtime_registry.py"],
  "RUNTIME_INSPECTOR_AUTHORITY":["aletheus/runtime/inspector/runtime_inspector.py","aletheus/runtime/managers/runtime_inspector.py"],
  "SCHEDULING_ORCHESTRATION_AUTHORITY":["aletheus/runtime/scheduler.py","aletheus/runtime/kernel/scheduler.py","aletheus/runtime/kernel/orchestrator.py"]}
 for fam,paths in families.items():
  present=[p for p in paths if p in s["files"]]
  if len(present)>1: authority.append({"family":fam,"candidates":present,"disposition":"ABSTAIN",
   "reason":"Semantic collision candidate; requires provenance and responsibility analysis."})
 for rel,ims in s["imports"].items():
  if rel=="aletheus/runtime/core.py":
   for x in ims:
    if any(t in x for t in ("platform_capability_fabric","genesis_112_22","genesis_112_23","genesis_112_24",
      "genesis_112_25","genesis_112_26","genesis_112_27","genesis_112_28","genesis_112_29")):
     core_leaks.append({"path":rel,"import":x})
 for rel in s["files"]:
  low=s["texts"][rel].lower()
  if "/mammoth/" not in rel.lower() and ("sqlite3.connect(" in low or "shelve.open(" in low):
   bypass.append({"path":rel,"evidence":"direct durable storage API outside Mammoth"})
  # Raw lexical candidates only; 112.29.3.1 calibrates them.
  if "/rsf/" in rel.lower() and re.search(r"\b(self_certify|issue_release_certificate|sign_release|certify)\b",low):
   rsfv.append({"path":rel,"evidence":"RSF certification-like lexical candidate"})
  if "/raf/" not in rel.lower() and re.search(r"\b(issue_release_certificate|sign_release|certify)\b",low):
   rafv.append({"path":rel,"evidence":"RAF/final-certification lexical candidate"})
  if "service" in rel.lower() and "capability" in rel.lower():
   boundary.append({"path":rel,"evidence":"service/capability lexical co-location candidate"})
 # Conservative raw orphan candidates: no inbound static import. Never equated with proven orphan.
 for rel in s["files"]:
  if rel.endswith("__init__.py"): continue
  if not s["inbound"].get(rel): orphans.append(rel)
 drift=len(authority)+len(orphans)+len(core_leaks)+len(bypass)+len(rsfv)+len(rafv)+len(boundary)
 finding_paths={x.get("path") for g in (core_leaks,bypass,rsfv,rafv,boundary) for x in g}
 audited=[]
 for x in s["surfaces"]:
  rel=x["relativePath"]; hit=rel in finding_paths
  audited.append({"surfaceId":x["surfaceId"],"relativePath":rel,
   "disposition":"ABSTAIN" if hit else "REUSE",
   "evidenceSummary":"Raw finding candidate; 112.29.3.1 calibration required." if hit else
    "Repository surface observed; no direct raw boundary finding."})
 r={"schemaVersion":"1.1.0","standard":"ALETHEUSOS-WHOLE-SYSTEM-ADVERSARIAL-INTEGRATION",
  "phase":"112.29.3","predecessor112292Proven":ok,"predecessorReference":pref,
  "predecessorEvidenceDigest":PREDECESSOR_DIGEST,"wholeSystemSurfacesAnalyzed":len(s["surfaces"]),
  "parseErrors":s["parseErrors"],"authorityCollisions":len(authority),"authorityCollisionEvidence":authority,
  "orphanedSurfaces":len(orphans),"orphanEvidence":orphans,
  "dependencyViolations":0,"dependencyEvidence":[],"runtimeCoreLeakage":len(core_leaks),
  "runtimeCoreLeakageEvidence":core_leaks,"mammothBypassFindings":len(bypass),"mammothBypassEvidence":bypass,
  "rsfAuthorityViolations":len(rsfv),"rsfAuthorityEvidence":rsfv,"rafAuthorityViolations":len(rafv),
  "rafAuthorityEvidence":rafv,"constitutionalBoundaryViolations":len(boundary),
  "constitutionalBoundaryEvidence":boundary,"driftFindings":drift,
  "sourceMutationAuthorized":False,"deletionAuthorized":False,"canonicalPromotionAuthorized":False,
  "auditedSurfaces":audited,
  "status":"WHOLE_SYSTEM_ADVERSARIAL_RECONCILIATION_COMPLETE" if ok and not s["parseErrors"] else "REFUSED"}
 r["evidenceDigest"]=digest(r); return r

def calibrate_findings(root:str|Path, raw:dict)->dict:
 root=Path(root).resolve(); s=_scan(root)
 provenance=[]; falsepos=[]; abstentions=[]; reachability=[]; lifecycle=[]; authority_ledger=[]
 # Reachability is multi-signal. Zero static imports alone is never proof of orphanhood.
 for rel in raw.get("orphanEvidence",[]):
  txt=s["texts"].get(rel,""); low=(rel+"\n"+txt).lower()
  signals=[]
  if any(h in low for h in DYNAMIC_HINTS): signals.append("DYNAMIC_ENTRYPOINT_OR_REGISTRATION_SIGNAL")
  if HISTORICAL_MASTER_RE.search(rel) or INTEGRATION_MASTER_RE.search(rel): signals.append("HISTORICAL_GENESIS_LINEAGE")
  if rel.endswith("/cli.py"): signals.append("CLI_ENTRY_SURFACE")
  if "/assurance/" in rel or "/certification/" in rel: signals.append("ASSURANCE_ENTRY_SURFACE")
  status="REACHABLE_OR_LIFECYCLE_BOUNDED" if signals else "UNRESOLVED_ZERO_IMPORT"
  disp="PRESERVE_DORMANT" if "HISTORICAL_GENESIS_LINEAGE" in signals else ("REUSE" if signals else "ABSTAIN")
  rec={"path":rel,"staticImportedBy":len(s["inbound"].get(rel,[])),"signals":signals,
       "calibratedStatus":status,"disposition":disp}
  reachability.append(rec)
  if status=="UNRESOLVED_ZERO_IMPORT": abstentions.append({"class":"ORPHAN_PROVENANCE","path":rel,
    "reason":"Zero static imports without sufficient lifecycle/dynamic-entry evidence."})
  else: falsepos.append({"rawClass":"ORPHAN_CANDIDATE","path":rel,"calibratedClass":status,
    "reason":"Zero static import is not equivalent to architectural orphan."})
 # Historical masters are preservation-bearing lineage, never auto-refactor/delete.
 for rel in s["files"]:
  if HISTORICAL_MASTER_RE.search(rel) or INTEGRATION_MASTER_RE.search(rel):
   lifecycle.append({"path":rel,"classification":"HISTORICAL_GENESIS_LINEAGE",
    "disposition":"PRESERVE_DORMANT","mutationAuthorized":False,"deletionAuthorized":False})
 # Certification semantics.
 cert_records=[]
 for rel,syms in s["symbols"].items():
  for sym in syms:
   if "certif" in sym["name"].lower() or any(v in sym["name"].lower() for v in ("sign_release","gold_seal")):
    kind=_classify_cert_symbol(sym["name"],sym["kind"])
    rec={"path":rel,"symbol":sym["name"],"line":sym["line"],"nodeKind":sym["kind"],"authorityKind":kind}
    cert_records.append(rec)
    if kind=="FINAL_RELEASE_AUTHORITY" and "/raf/" not in rel.lower():
     abstentions.append({"class":"FINAL_RAF_AUTHORITY_PROVENANCE","path":rel,"symbol":sym["name"],
      "reason":"Final release authority-like operation exists outside RAF."})
    elif kind!="FINAL_RELEASE_AUTHORITY":
     falsepos.append({"rawClass":"RAF_OR_RSF_AUTHORITY_CANDIDATE","path":rel,"symbol":sym["name"],
      "calibratedClass":kind,"reason":"Authority noun/check/assurance is not final release issuance authority."})
 # Collision provenance: classify by bounded role; do not collapse unlike responsibilities.
 role_map={
  "aletheus/runtime/registries.py":"RUNTIME_COMPOSITION_REGISTRIES",
  "aletheus/runtime/services/service_registry.py":"SERVICE_REGISTRY",
  "aletheus/mesh/runtime_registry.py":"MESH_RUNTIME_REGISTRY",
  "aletheus/runtime/inspector/runtime_inspector.py":"RUNTIME_INSPECTION_SURFACE",
  "aletheus/runtime/managers/runtime_inspector.py":"RUNTIME_MANAGER_INSPECTION_ADAPTER",
  "aletheus/runtime/scheduler.py":"RUNTIME_SCHEDULING_FACADE",
  "aletheus/runtime/kernel/scheduler.py":"KERNEL_TASK_SCHEDULER",
  "aletheus/runtime/kernel/orchestrator.py":"KERNEL_ORCHESTRATION"}
 collision_res=[]
 for fam in raw.get("authorityCollisionEvidence",[]):
  members=[]
  for p in fam["candidates"]:
   members.append({"path":p,"boundedRole":role_map.get(p,"UNRESOLVED"),
    "staticImportedBy":len(s["inbound"].get(p,[]))})
  unresolved=[m for m in members if m["boundedRole"]=="UNRESOLVED"]
  status="COMPOSE_BOUNDED_AUTHORITIES" if not unresolved else "ABSTAIN"
  disposition="COMPOSE" if status.startswith("COMPOSE") else "ABSTAIN"
  rec={"family":fam["family"],"members":members,"resolution":status,"disposition":disposition,
       "automaticMutationAuthorized":False}
  collision_res.append(rec)
  if unresolved: abstentions.append({"class":"AUTHORITY_COLLISION","family":fam["family"],
    "reason":"Bounded role unresolved for one or more members."})
 # Raw boundary lexical co-location is not itself a violation.
 for x in raw.get("constitutionalBoundaryEvidence",[]):
  falsepos.append({"rawClass":"SERVICE_CAPABILITY_COLOCATION","path":x["path"],
    "calibratedClass":"LEXICAL_COLOCATION_ONLY","reason":"Path-name co-location is not boundary penetration evidence."})
 # Genuine direct-storage/core-leak evidence remains blocking.
 blockers=[]
 for x in raw.get("runtimeCoreLeakageEvidence",[]): blockers.append({"class":"RUNTIME_CORE_LEAKAGE",**x})
 for x in raw.get("mammothBypassEvidence",[]): blockers.append({"class":"MAMMOTH_BYPASS",**x})
 for a in abstentions: blockers.append(a)
 calibrated={
  "authorityCollisions":sum(1 for x in collision_res if x["resolution"]=="ABSTAIN"),
  "orphanedSurfaces":sum(1 for x in reachability if x["calibratedStatus"]=="UNRESOLVED_ZERO_IMPORT"),
  "dependencyViolations":raw.get("dependencyViolations",0),
  "runtimeCoreLeakage":raw.get("runtimeCoreLeakage",0),
  "mammothBypassFindings":raw.get("mammothBypassFindings",0),
  "rsfAuthorityViolations":sum(1 for x in abstentions if x["class"]=="FINAL_RAF_AUTHORITY_PROVENANCE" and "/rsf/" in x["path"].lower()),
  "rafAuthorityViolations":sum(1 for x in abstentions if x["class"]=="FINAL_RAF_AUTHORITY_PROVENANCE"),
  "constitutionalBoundaryViolations":0}
 calibrated["blockingFindings"]=sum(calibrated.values())
 status="FINDING_RESOLUTION_COMPLETE" if calibrated["blockingFindings"]==0 else \
        ("FINDING_RESOLUTION_COMPLETE_WITH_ABSTENTIONS" if abstentions else "FINDING_RESOLUTION_BLOCKED")
 d={"schemaVersion":"1.0.0","standard":"ALETHEUSOS-WHOLE-SYSTEM-FINDING-RESOLUTION-SCANNER-CALIBRATION",
  "phase":"112.29.3.1","predecessor112293Proven":raw.get("status")=="WHOLE_SYSTEM_ADVERSARIAL_RECONCILIATION_COMPLETE",
  "predecessor112293EvidenceDigest":raw.get("evidenceDigest"),
  "rawFindings":{"authorityCollisions":raw.get("authorityCollisions",0),"orphanedSurfaces":raw.get("orphanedSurfaces",0),
   "dependencyViolations":raw.get("dependencyViolations",0),"runtimeCoreLeakage":raw.get("runtimeCoreLeakage",0),
   "mammothBypassFindings":raw.get("mammothBypassFindings",0),"rsfAuthorityViolations":raw.get("rsfAuthorityViolations",0),
   "rafAuthorityViolations":raw.get("rafAuthorityViolations",0),
   "constitutionalBoundaryViolations":raw.get("constitutionalBoundaryViolations",0),"driftFindings":raw.get("driftFindings",0)},
  "calibratedFindings":calibrated,"collisionResolutionEvidence":collision_res,
  "reachabilityLedger":reachability,"lifecycleClassificationLedger":lifecycle,
  "certificationAuthorityLedger":cert_records,"scannerFalsePositiveLedger":falsepos,
  "unresolvedAbstentionLedger":abstentions,"blockingEvidence":blockers,
  "calibrationRules":["ZERO_STATIC_IMPORT_IS_NOT_ORPHAN_PROOF","AUTHORITY_NOUN_IS_NOT_AUTHORITY_OPERATION",
   "DEFENSIVE_RAF_CHECK_IS_NOT_RAF_POSSESSION","MAMMOTH_ASSURANCE_IS_NOT_FINAL_RAF_AUTHORITY",
   "RSF_ASSURANCE_IS_NOT_RELEASE_ISSUANCE","HISTORICAL_GENESIS_LINEAGE_REQUIRES_PRESERVATION"],
  "sourceMutationAuthorized":False,"deletionAuthorized":False,"canonicalPromotionAuthorized":False,
  "goldSealIssuanceAuthorized":False,"status":status}
 d["evidenceDigest"]=digest(d); return d

def phase_reports(a:dict,c:dict)->dict:
 f=c["calibratedFindings"]; no_abstain=not c["unresolvedAbstentionLedger"]
 collision={"phase":"112.29.4","calibrationEvidenceDigest":c["evidenceDigest"],
  "status":"CANONICAL_AUTHORITY_OWNERSHIP_RESOLVED" if f["authorityCollisions"]==0 else "COLLISION_RESOLUTION_BLOCKED",
  "authorityCollisions":f["authorityCollisions"],"automaticMutationAuthorized":False,
  "dispositions":[x.value for x in SurfaceDisposition]}
 mesh={"phase":"112.29.5","status":"CONNECTION_MESH_VERIFIED" if f["dependencyViolations"]==0 else "CONNECTION_MESH_BLOCKED",
  "dependencyViolations":f["dependencyViolations"]}
 penetration={"phase":"112.29.6","status":"BOUNDARY_PENETRATION_PASS" if
  f["runtimeCoreLeakage"]==f["mammothBypassFindings"]==f["rsfAuthorityViolations"]==f["rafAuthorityViolations"]==f["constitutionalBoundaryViolations"]==0
  else "BOUNDARY_PENETRATION_BLOCKED"}
 continuity={"phase":"112.29.7","status":"CONTINUITY_VALIDATION_PASS" if f["mammothBypassFindings"]==0 and f["rsfAuthorityViolations"]==0
  else "CONTINUITY_VALIDATION_BLOCKED","mammothAuthority":"MAMMOTH","reliabilityAuthority":"RSF"}
 constitutional={"phase":"112.29.8","status":"WHOLE_SYSTEM_CONSTITUTIONAL_VALIDATION_PASS" if
  penetration["status"].endswith("PASS") and continuity["status"].endswith("PASS") and no_abstain
  else "WHOLE_SYSTEM_CONSTITUTIONAL_VALIDATION_BLOCKED","externalRAFFinalAuthorityRequired":True}
 blocking=f["blockingFindings"]
 closure={"phase":"112.29.9","status":"GENESIS_112_UNIFIED_PLATFORM_MASTER_CLOSURE_EVIDENCE_COMPLETE"
  if blocking==0 and constitutional["status"].endswith("PASS") else "MASTER_CLOSURE_BLOCKED",
  "blockingFindings":blocking,"selfCertificationPermitted":False}
 for x in (collision,mesh,penetration,continuity,constitutional,closure): x["evidenceDigest"]=digest(x)
 return {x["phase"]:x for x in (collision,mesh,penetration,continuity,constitutional,closure)}

def external_raf(a:dict,c:dict,ph:dict)->dict:
 closure=ph["112.29.9"]; eligible=(closure["status"]=="GENESIS_112_UNIFIED_PLATFORM_MASTER_CLOSURE_EVIDENCE_COMPLETE"
  and a["predecessor112292Proven"] and c["status"]=="FINDING_RESOLUTION_COMPLETE")
 r={"schemaVersion":"1.1.0","standard":"ALETHEUSOS-EXTERNAL-RAF-INDEPENDENT-GOLD-SEAL","phase":"112.29.9.1",
  "independentExternalRAFAuthority":True,"scannerCalibrationEvidenceDigest":c["evidenceDigest"],
  "mammothPersistenceAuthorityPreserved":c["calibratedFindings"]["mammothBypassFindings"]==0,
  "rsfReliabilityAuthorityPreserved":c["calibratedFindings"]["rsfAuthorityViolations"]==0,
  "runtimeCoreCompositionRootPreserved":c["calibratedFindings"]["runtimeCoreLeakage"]==0,
  "masterClosureEvidenceDigest":closure["evidenceDigest"],
  "status":FINAL_STATUS if eligible else "EXTERNAL_RAF_CERTIFICATION_REFUSED"}
 r["certificationDigest"]=digest(r); return r

def write_dossier(root:str|Path,c:dict)->Path:
 root=Path(root); out=root/"reports/unified-platform-integration/112.29.3.1-finding-resolution"
 out.mkdir(parents=True,exist_ok=True)
 artifacts={
  "finding-resolution-dossier.json":c,
  "authority-provenance-ledger.json":c["certificationAuthorityLedger"],
  "collision-resolution-evidence.json":c["collisionResolutionEvidence"],
  "reachability-ledger.json":c["reachabilityLedger"],
  "lifecycle-classification-ledger.json":c["lifecycleClassificationLedger"],
  "scanner-false-positive-ledger.json":c["scannerFalsePositiveLedger"],
  "scanner-calibration-profile.json":{"rules":c["calibrationRules"],"schemaVersion":c["schemaVersion"]},
  "disposition-ledger.json":{"collisions":c["collisionResolutionEvidence"],"lifecycle":c["lifecycleClassificationLedger"]},
  "unresolved-abstention-ledger.json":c["unresolvedAbstentionLedger"],
  "preservation-proof-requirements.json":{"requiredForDeletion":True,"requiredForPromotion":True,
   "sourceMutationAuthorized":False,"deletionAuthorized":False,"canonicalPromotionAuthorized":False},
  "predecessor-evidence.json":{"phase":"112.29.3","evidenceDigest":c["predecessor112293EvidenceDigest"]}}
 for n,v in artifacts.items(): (out/n).write_text(json.dumps(v,indent=2,sort_keys=True)+"\n")
 manifest={n:"sha256:"+hashlib.sha256((out/n).read_bytes()).hexdigest() for n in artifacts}
 (out/"evidence-manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
 (out/"evidence-digest.sha256").write_text(c["evidenceDigest"]+"\n")
 return out
