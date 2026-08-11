from __future__ import annotations
from pathlib import Path
from typing import Any
import hashlib, json, re

from . import core

PHASES_FULL=(
("112.29.3","Whole-System Adversarial Integration & Drift Eradication"),
("112.29.3.1","Whole-System Finding Resolution, Authority Provenance & Scanner Calibration Dossier"),
("112.29.3.2","Calibrated Finding Adjudication & Evidence Closure"),
("112.29.4","Canonical Authority / Ownership Collision Resolution"),
("112.29.5","Cross-Fabric Dependency & Connection-Mesh Verification"),
("112.29.6","Runtime / Capability / Service Boundary Penetration Assurance"),
("112.29.7","Mammoth Persistence + RSF Reliability Continuity Validation"),
("112.29.8","Whole-System Constitutional & Failure-Mode Validation"),
("112.29.9","Genesis 112 Unified Platform Master Closure"),
("112.29.9.1","External RAF Independent Certification & Gold Seal"),)

PACKAGE_VERSION="1.2.0"
VERSIONED_LEGACY_RE=re.compile(
    r"/(?:agents|planning|workflow|plugins|persistence|distributed|federation|telemetry|tenancy|security|high_availability|event_bus)_v\d+/"
)

def _finding_id(kind:str,path:str,symbol:str="")->str:
    return "FND-"+hashlib.sha256((kind+"|"+path+"|"+symbol).encode()).hexdigest()[:16].upper()

def _line_for_pattern(text:str,patterns:list[str])->int:
    for i,line in enumerate(text.splitlines(),1):
        if any(p.lower() in line.lower() for p in patterns):
            return i
    return 0

def _reference_evidence(scan:dict, rel:str)->dict:
    mod=rel[:-3].replace("/",".") if rel.endswith(".py") else rel.replace("/",".")
    stem=Path(rel).stem
    tokens={mod,mod.split(".")[-1],stem}
    refs=[]; reg=[]; runtime=[]; tests=[]
    for other,txt in scan.get("texts",{}).items():
        if other==rel:
            continue
        low=txt.lower()
        if any(t and t in txt for t in tokens):
            refs.append(other)
            if any(k in low for k in ("register","registry","binding","activation","attach","entrypoint","entry_point")):
                reg.append(other)
            if other=="aletheus/runtime/core.py" or "/runtime/" in other:
                runtime.append(other)
            if "/test" in other or other.startswith("tests/"):
                tests.append(other)
    return {
        "staticImporters":scan.get("inbound",{}).get(rel,[]),
        "textualReferences":sorted(set(refs)),
        "registrationReferences":sorted(set(reg)),
        "runtimeReferences":sorted(set(runtime)),
        "testReferences":sorted(set(tests)),
    }

def adjudicate_findings(root:str|Path, calibration:dict)->dict:
    root=Path(root).resolve()
    scan=core._scan(root)
    records=[]

    # ORPHAN / reachability adjudication
    for finding in calibration.get("unresolvedAbstentionLedger",[]):
        if finding.get("class")!="ORPHAN_PROVENANCE":
            continue
        rel=finding.get("path","")
        text=scan.get("texts",{}).get(rel,"")
        ev=_reference_evidence(scan,rel)
        signals=[]
        if ev["registrationReferences"]:
            signals.append("REGISTRATION_REFERENCE")
        if ev["runtimeReferences"]:
            signals.append("RUNTIME_ATTACHMENT_REFERENCE")
        if ev["testReferences"]:
            signals.append("TEST_REFERENCE")
        if rel.endswith("/cli.py") or "/cli/" in rel:
            signals.append("CLI_ENTRYPOINT")
        if any(x in rel for x in ("/certification/","/assurance/","/reconciliation","/resolver")):
            signals.append("ASSURANCE_OR_RECONCILIATION_ENTRYPOINT")
        if core.HISTORICAL_MASTER_RE.search(rel) or core.INTEGRATION_MASTER_RE.search(rel):
            signals.append("HISTORICAL_GENESIS_LINEAGE")
        if VERSIONED_LEGACY_RE.search("/"+rel):
            signals.append("VERSIONED_LEGACY_SURFACE")
        low=text.lower()
        if any(k in low for k in (
            'if __name__ == "__main__"',
            "if __name__ == '__main__'",
            "argparse","click.command","typer."
        )):
            signals.append("EXECUTABLE_ENTRYPOINT")

        if "HISTORICAL_GENESIS_LINEAGE" in signals:
            disposition=core.SurfaceDisposition.PRESERVE_DORMANT.value
            rationale="Historical Genesis lineage is evidence-bearing and must be preserved; zero static imports do not establish orphanhood."
            confidence=.96; blocking=False
        elif "VERSIONED_LEGACY_SURFACE" in signals and not ev["runtimeReferences"] and not ev["registrationReferences"]:
            disposition=core.SurfaceDisposition.PRESERVE_DORMANT.value
            rationale="Versioned legacy surface has no live runtime/registration evidence; preserve dormant rather than delete or promote."
            confidence=.93; blocking=False
        elif any(x in signals for x in (
            "REGISTRATION_REFERENCE","RUNTIME_ATTACHMENT_REFERENCE","TEST_REFERENCE",
            "CLI_ENTRYPOINT","ASSURANCE_OR_RECONCILIATION_ENTRYPOINT","EXECUTABLE_ENTRYPOINT"
        )):
            disposition=core.SurfaceDisposition.REUSE.value
            rationale="Runtime, registration, test, assurance, or executable-entry evidence establishes bounded reachability."
            confidence=.91; blocking=False
        else:
            disposition=core.SurfaceDisposition.ABSTAIN.value
            rationale="No sufficient runtime, registration, test, entrypoint, or lifecycle evidence establishes a safe disposition."
            confidence=.55; blocking=True

        records.append({
            "findingId":_finding_id("ORPHAN",rel),
            "findingClass":"ORPHAN",
            "surfacePath":rel,
            "symbol":"",
            "lineNumber":0,
            "detectionRule":"ZERO_STATIC_IMPORT_CALIBRATED",
            "staticImporters":ev["staticImporters"],
            "dynamicRegistrationEvidence":ev["registrationReferences"],
            "runtimeAttachmentEvidence":ev["runtimeReferences"],
            "historicalGenesisEvidence":[x for x in signals if "HISTORICAL" in x or "LEGACY" in x],
            "declaredOwner":"UNRESOLVED",
            "observedOwner":"LIFECYCLE_OR_RUNTIME_EVIDENCE" if not blocking else "UNRESOLVED",
            "authorityOperation":False,
            "authorityKind":"NONE",
            "constitutionalBoundary":"Platform Surface Reachability",
            "disposition":disposition,
            "confidence":confidence,
            "rationale":rationale,
            "blocking":blocking,
            "requiresSourceChange":False,
            "evidenceSignals":sorted(set(signals)),
            "referenceEvidence":ev,
        })

    # Mammoth persistence bypass adjudication
    for finding in calibration.get("blockingEvidence",[]):
        if finding.get("class")!="MAMMOTH_BYPASS":
            continue
        rel=finding.get("path","")
        text=scan.get("texts",{}).get(rel,"")
        ev=_reference_evidence(scan,rel)
        line=_line_for_pattern(text,["sqlite3.connect(","shelve.open("])
        has_gateway=("aletheus.mammoth" in text or "mammoth.gateway" in text.lower())
        versioned=VERSIONED_LEGACY_RE.search("/"+rel) is not None
        inactive=versioned and not ev["staticImporters"] and not ev["runtimeReferences"] and not ev["registrationReferences"]

        if has_gateway:
            disposition=core.SurfaceDisposition.REUSE.value
            blocking=False; requires=False; confidence=.91
            rationale="The durable-I/O candidate contains explicit Mammoth mediation evidence in the bounded surface."
        elif inactive:
            disposition=core.SurfaceDisposition.PRESERVE_DORMANT.value
            blocking=False; requires=False; confidence=.94
            rationale="Direct durable I/O is confined to an evidence-inactive versioned legacy surface; preserve dormant and prohibit canonical attachment."
        else:
            disposition=core.SurfaceDisposition.REFACTOR.value
            blocking=True; requires=True; confidence=.98
            rationale="Active or insufficiently dormant direct durable I/O lacks proven Mammoth gateway mediation."

        records.append({
            "findingId":_finding_id("MAMMOTH_BYPASS",rel),
            "findingClass":"MAMMOTH_BYPASS",
            "surfacePath":rel,
            "symbol":"",
            "lineNumber":line,
            "detectionRule":"DIRECT_DURABLE_IO_OUTSIDE_MAMMOTH",
            "staticImporters":ev["staticImporters"],
            "dynamicRegistrationEvidence":ev["registrationReferences"],
            "runtimeAttachmentEvidence":ev["runtimeReferences"],
            "declaredOwner":"MAMMOTH",
            "observedOwner":"LEGACY_SURFACE" if inactive else "DIRECT_IO_CALLER",
            "authorityOperation":True,
            "authorityKind":"PERSISTENCE",
            "persistencePath":"EVIDENCE_DERIVED_CALLSITE",
            "mammothGatewayEvidence":"PRESENT" if has_gateway else "NONE",
            "constitutionalBoundary":"Mammoth Durable Persistence",
            "disposition":disposition,
            "confidence":confidence,
            "rationale":rationale,
            "blocking":blocking,
            "requiresSourceChange":requires,
            "referenceEvidence":ev,
        })

    # RAF / RSF final-authority provenance adjudication
    for finding in calibration.get("unresolvedAbstentionLedger",[]):
        if finding.get("class")!="FINAL_RAF_AUTHORITY_PROVENANCE":
            continue
        rel=finding.get("path","")
        symbol=finding.get("symbol","")
        ev=_reference_evidence(scan,rel)
        symrec=next((
            x for x in calibration.get("certificationAuthorityLedger",[])
            if x.get("path")==rel and x.get("symbol")==symbol
        ),None)
        kind=(symrec or {}).get("authorityKind") or core._classify_cert_symbol(symbol,"FunctionDef")
        under_rsf="/rsf/" in rel.lower()
        under_raf="/raf/" in rel.lower()
        historical=bool(
            core.HISTORICAL_MASTER_RE.search(rel)
            or core.INTEGRATION_MASTER_RE.search(rel)
            or "/platform_service_fabric/genesis_112_21_master/" in rel
        )
        final_op=kind=="FINAL_RELEASE_AUTHORITY"
        dormant=historical and not ev["runtimeReferences"] and not ev["registrationReferences"]

        if dormant:
            disposition=core.SurfaceDisposition.PRESERVE_DORMANT.value
            blocking=False; requires=False; confidence=.95
            rationale="Historical certification lineage is not attached to live runtime authority; preserve as evidence-bearing dormant surface."
        elif under_raf and final_op:
            disposition=core.SurfaceDisposition.CANONICAL.value
            blocking=False; requires=False; confidence=.98
            rationale="Final release authority operation resides within the RAF authority boundary."
        elif not final_op:
            disposition=core.SurfaceDisposition.REUSE.value
            blocking=False; requires=False; confidence=.95
            rationale="Certification-related behavior is evidence/check/assurance behavior, not final release issuance authority."
        else:
            disposition=core.SurfaceDisposition.REFUSE.value
            blocking=True; requires=True; confidence=.99
            rationale="Final release authority-like operation remains outside RAF and is not proven dormant."

        records.append({
            "findingId":_finding_id("RSF_AUTHORITY" if under_rsf else "RAF_AUTHORITY",rel,symbol),
            "findingClass":"RSF_AUTHORITY" if under_rsf else "RAF_AUTHORITY",
            "surfacePath":rel,
            "symbol":symbol,
            "lineNumber":(symrec or {}).get("line",0),
            "detectionRule":"FINAL_RAF_AUTHORITY_PROVENANCE",
            "staticImporters":ev["staticImporters"],
            "dynamicRegistrationEvidence":ev["registrationReferences"],
            "runtimeAttachmentEvidence":ev["runtimeReferences"],
            "historicalGenesisEvidence":"HISTORICAL_CERTIFICATION_LINEAGE" if dormant else "",
            "declaredOwner":"RAF" if under_raf else ("RSF" if under_rsf else "EXTERNAL_RAF_REQUIRED"),
            "observedOwner":"RAF" if under_raf else ("RSF" if under_rsf else "NON_RAF_SURFACE"),
            "authorityOperation":final_op,
            "authorityKind":kind,
            "rsfEvidenceRole":"RELIABILITY_EVIDENCE_ONLY" if under_rsf and not final_op else "",
            "rafEvidenceRole":"FINAL_RELEASE_AUTHORITY" if under_raf and final_op else "ASSURANCE_PARTICIPANT",
            "constitutionalBoundary":"RAF ↔ RSF Authority Separation",
            "disposition":disposition,
            "confidence":confidence,
            "rationale":rationale,
            "blocking":blocking,
            "requiresSourceChange":requires,
            "referenceEvidence":ev,
        })

    # Runtime-core leakage is always retained.
    for finding in calibration.get("blockingEvidence",[]):
        if finding.get("class")!="RUNTIME_CORE_LEAKAGE":
            continue
        rel=finding.get("path","")
        records.append({
            "findingId":_finding_id("GENERAL_DRIFT",rel,str(finding.get("import",""))),
            "findingClass":"GENERAL_DRIFT",
            "surfacePath":rel,
            "symbol":"",
            "lineNumber":0,
            "detectionRule":"RUNTIME_CORE_DIRECT_FABRIC_ATTACHMENT",
            "staticImporters":[],
            "declaredOwner":"Runtime Composition Root",
            "observedOwner":"Direct Fabric Attachment",
            "authorityOperation":False,
            "authorityKind":"BOUNDARY_LEAK",
            "constitutionalBoundary":"Runtime Core Composition Root",
            "disposition":core.SurfaceDisposition.REFACTOR.value,
            "confidence":.99,
            "rationale":"Runtime core directly imports a higher-order fabric surface.",
            "blocking":True,
            "requiresSourceChange":True,
        })

    cleared=sum(1 for r in records if not r["blocking"])
    defects=sum(1 for r in records if r["blocking"] and r["disposition"] in (
        core.SurfaceDisposition.REFACTOR.value,core.SurfaceDisposition.REFUSE.value
    ))
    abstentions=sum(1 for r in records if r["blocking"] and r["disposition"]==core.SurfaceDisposition.ABSTAIN.value)

    if defects==0 and abstentions==0:
        status="CALIBRATED_ADJUDICATION_COMPLETE"
    elif defects and abstentions:
        status="CALIBRATED_ADJUDICATION_COMPLETE_WITH_DEFECTS_AND_ABSTENTIONS"
    elif defects:
        status="CALIBRATED_ADJUDICATION_COMPLETE_WITH_DEFECTS"
    else:
        status="CALIBRATED_ADJUDICATION_COMPLETE_WITH_ABSTENTIONS"

    report={
        "schemaVersion":"1.0.0",
        "standard":"ALETHEUSOS-GENESIS-112.29.3.2-CALIBRATED-ADJUDICATION",
        "phase":"112.29.3.2",
        "predecessor1122931Proven":calibration.get("phase")=="112.29.3.1",
        "predecessor1122931EvidenceDigest":calibration.get("evidenceDigest"),
        "totalAdjudicated":len(records),
        "clearedCount":cleared,
        "defectsRetainedCount":defects,
        "abstentionsCount":abstentions,
        "blockingFindings":defects+abstentions,
        "adjudicatedFindings":records,
        "sourceMutationAuthorized":False,
        "deletionAuthorized":False,
        "canonicalPromotionAuthorized":False,
        "adjudicationStatus":status,
    }
    report["evidenceDigest"]=core.digest(report)
    return report

def phase_reports_full(adversarial:dict, calibration:dict, adjudication:dict)->dict:
    f=calibration["calibratedFindings"]
    collision={
        "phase":"112.29.4",
        "calibrationEvidenceDigest":calibration["evidenceDigest"],
        "adjudicationEvidenceDigest":adjudication["evidenceDigest"],
        "status":"CANONICAL_AUTHORITY_OWNERSHIP_RESOLVED" if f["authorityCollisions"]==0 else "COLLISION_RESOLUTION_BLOCKED",
        "authorityCollisions":f["authorityCollisions"],
        "automaticMutationAuthorized":False,
        "dispositions":[x.value for x in core.SurfaceDisposition],
    }
    mesh={
        "phase":"112.29.5",
        "status":"CONNECTION_MESH_VERIFIED" if f["dependencyViolations"]==0 else "CONNECTION_MESH_BLOCKED",
        "dependencyViolations":f["dependencyViolations"],
    }
    boundary_blockers=[
        r for r in adjudication["adjudicatedFindings"]
        if r["blocking"] and r["findingClass"] in ("RAF_AUTHORITY","RSF_AUTHORITY","GENERAL_DRIFT")
    ]
    penetration={
        "phase":"112.29.6",
        "status":"BOUNDARY_PENETRATION_PASS" if not boundary_blockers else "BOUNDARY_PENETRATION_BLOCKED",
        "blockingFindingIds":[r["findingId"] for r in boundary_blockers],
    }
    continuity_blockers=[
        r for r in adjudication["adjudicatedFindings"]
        if r["blocking"] and r["findingClass"] in ("MAMMOTH_BYPASS","RSF_AUTHORITY")
    ]
    continuity={
        "phase":"112.29.7",
        "status":"CONTINUITY_VALIDATION_PASS" if not continuity_blockers else "CONTINUITY_VALIDATION_BLOCKED",
        "mammothAuthority":"MAMMOTH",
        "reliabilityAuthority":"RSF",
        "blockingFindingIds":[r["findingId"] for r in continuity_blockers],
    }
    constitutional_ok=(
        penetration["status"].endswith("PASS")
        and continuity["status"].endswith("PASS")
        and adjudication["blockingFindings"]==0
    )
    constitutional={
        "phase":"112.29.8",
        "status":"WHOLE_SYSTEM_CONSTITUTIONAL_VALIDATION_PASS" if constitutional_ok else "WHOLE_SYSTEM_CONSTITUTIONAL_VALIDATION_BLOCKED",
        "externalRAFFinalAuthorityRequired":True,
    }
    closure={
        "phase":"112.29.9",
        "status":"GENESIS_112_UNIFIED_PLATFORM_MASTER_CLOSURE_EVIDENCE_COMPLETE"
        if constitutional_ok and collision["status"].endswith("RESOLVED") and mesh["status"].endswith("VERIFIED")
        else "MASTER_CLOSURE_BLOCKED",
        "blockingFindings":adjudication["blockingFindings"],
        "selfCertificationPermitted":False,
    }
    for x in (collision,mesh,penetration,continuity,constitutional,closure):
        x["evidenceDigest"]=core.digest(x)
    return {x["phase"]:x for x in (collision,mesh,penetration,continuity,constitutional,closure)}

def external_raf_full(adversarial:dict, calibration:dict, adjudication:dict, phases:dict)->dict:
    closure=phases["112.29.9"]
    eligible=(
        closure["status"]=="GENESIS_112_UNIFIED_PLATFORM_MASTER_CLOSURE_EVIDENCE_COMPLETE"
        and adversarial.get("predecessor112292Proven") is True
        and adjudication.get("adjudicationStatus")=="CALIBRATED_ADJUDICATION_COMPLETE"
    )
    result={
        "schemaVersion":"1.2.0",
        "standard":"ALETHEUSOS-EXTERNAL-RAF-INDEPENDENT-GOLD-SEAL",
        "phase":"112.29.9.1",
        "independentExternalRAFAuthority":True,
        "scannerCalibrationEvidenceDigest":calibration["evidenceDigest"],
        "adjudicationEvidenceDigest":adjudication["evidenceDigest"],
        "mammothPersistenceAuthorityPreserved":not any(
            x["blocking"] and x["findingClass"]=="MAMMOTH_BYPASS"
            for x in adjudication["adjudicatedFindings"]
        ),
        "rsfReliabilityAuthorityPreserved":not any(
            x["blocking"] and x["findingClass"]=="RSF_AUTHORITY"
            for x in adjudication["adjudicatedFindings"]
        ),
        "runtimeCoreCompositionRootPreserved":not any(
            x["blocking"] and x["findingClass"]=="GENERAL_DRIFT"
            for x in adjudication["adjudicatedFindings"]
        ),
        "masterClosureEvidenceDigest":closure["evidenceDigest"],
        "status":core.FINAL_STATUS if eligible else "EXTERNAL_RAF_CERTIFICATION_REFUSED",
    }
    result["certificationDigest"]=core.digest(result)
    return result

def write_adjudication_dossier(root:str|Path, report:dict)->Path:
    root=Path(root)
    out=root/"reports/unified-platform-integration/112.29.3.2-adjudication"
    out.mkdir(parents=True,exist_ok=True)
    records=report["adjudicatedFindings"]
    artifacts={
        "calibrated-finding-adjudication-report.json":report,
        "cleared-findings-ledger.json":[r for r in records if not r["blocking"]],
        "retained-defects-ledger.json":[
            r for r in records if r["blocking"] and r["disposition"] in ("REFACTOR","REFUSE")
        ],
        "remaining-abstentions-ledger.json":[
            r for r in records if r["blocking"] and r["disposition"]=="ABSTAIN"
        ],
        "mammoth-persistence-adjudication.json":[r for r in records if r["findingClass"]=="MAMMOTH_BYPASS"],
        "rsf-authority-adjudication.json":[r for r in records if r["findingClass"]=="RSF_AUTHORITY"],
        "raf-authority-adjudication.json":[r for r in records if r["findingClass"]=="RAF_AUTHORITY"],
        "orphan-reachability-adjudication.json":[r for r in records if r["findingClass"]=="ORPHAN"],
        "source-remediation-requirements.json":[r for r in records if r["requiresSourceChange"]],
        "predecessor-evidence.json":{
            "phase":"112.29.3.1",
            "evidenceDigest":report["predecessor1122931EvidenceDigest"],
        },
    }
    for name,value in artifacts.items():
        (out/name).write_text(json.dumps(value,indent=2,sort_keys=True)+"\n")
    manifest={
        name:"sha256:"+hashlib.sha256((out/name).read_bytes()).hexdigest()
        for name in artifacts
    }
    (out/"evidence-manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    (out/"evidence-digest.sha256").write_text(report["evidenceDigest"]+"\n")
    return out
