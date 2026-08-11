from __future__ import annotations
import ast, hashlib, json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXPECTED_RSF_EVIDENCE_DIGEST = "sha256:88d55ee7b20279db0cdb9c1d8aee465705ae0db1c3eb045ad13c027adfc47424"
FINAL_STATUS = "GENESIS_112_20_RSF_PROJECT_CERTIFIED"

class ExternalRAFCertificationError(RuntimeError): pass

def _utc(): return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def _canonical(v: Any)->bytes: return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def _digest(v: Any)->str: return "sha256:"+hashlib.sha256(_canonical(v)).hexdigest()
def _file_digest(p:Path)->str: return "sha256:"+hashlib.sha256(p.read_bytes()).hexdigest()

@dataclass(frozen=True)
class Finding:
    path:str; line:int; rule_id:str; detail:str

class ExternalRAFProjectCertifier:
    RSF_EVIDENCE_REL=Path("reports/rsf/genesis-112.20-project-assurance/rsf-master-closure-evidence.json")
    MAMMOTH_CERT_REL=Path("reports/mammoth/genesis-113.9-project-certification/mammoth-project-certification.json")
    REQUIRED_RSF=("contracts.py","invariants.py","recovery.py","observation.py","bridge.py","persistence.py","adversarial.py","boundary.py","closure.py")
    RSF_FORBIDDEN={"sign_release","issue_release_certificate","publish_release_certificate","certify_release"}
    HARDCODED={"certified","all_checks_passed","boundary_clean","assurance_pass","release_certified"}

    @classmethod
    def _verify_rsf_evidence(cls, project:Path):
        p=project/cls.RSF_EVIDENCE_REL
        if not p.is_file(): return False,[Finding(str(cls.RSF_EVIDENCE_REL),0,"RSF_EVIDENCE_MISSING","master closure evidence not found")],None
        try: doc=json.loads(p.read_text())
        except Exception as e: return False,[Finding(str(cls.RSF_EVIDENCE_REL),0,"RSF_EVIDENCE_PARSE",str(e))],None
        embedded=doc.get("evidenceDigest")
        body=dict(doc); body.pop("evidenceDigest",None)
        recomputed=_digest(body)
        f=[]
        if embedded!=recomputed: f.append(Finding(str(cls.RSF_EVIDENCE_REL),0,"RSF_EVIDENCE_DIGEST_INVALID",f"embedded={embedded} recomputed={recomputed}"))
        if recomputed!=EXPECTED_RSF_EVIDENCE_DIGEST: f.append(Finding(str(cls.RSF_EVIDENCE_REL),0,"RSF_EVIDENCE_ANCESTRY_MISMATCH",f"expected={EXPECTED_RSF_EVIDENCE_DIGEST} actual={recomputed}"))
        if doc.get("status")!="RSF_MASTER_CLOSURE_EVIDENCE_COMPLETE": f.append(Finding(str(cls.RSF_EVIDENCE_REL),0,"RSF_CLOSURE_INCOMPLETE",str(doc.get("status"))))
        auth=doc.get("authorityBoundary",{})
        if auth.get("rsfMaySelfIssueRAFCertificate") is not False or auth.get("externalRAFCertificationRequired") is not True:
            f.append(Finding(str(cls.RSF_EVIDENCE_REL),0,"RSF_AUTHORITY_BOUNDARY_INVALID",str(auth)))
        return not f,f,doc

    @classmethod
    def _scan_boundary(cls,project:Path):
        findings=[]; files=0
        for relroot,kind in (("aletheus/rsf","RSF"),("aletheus/reliability","RSF"),("aletheus/raf","RAF"),("aletheus/release","RAF")):
            root=project/relroot
            if not root.exists(): continue
            for p in sorted(root.rglob("*.py")):
                # External certifier is policy authority, not a target of its own RSF/RAF leakage rules.
                if "genesis_112_20_9_1" in p.parts: continue
                files+=1; rel=str(p.relative_to(project))
                try: tree=ast.parse(p.read_text(encoding="utf-8"))
                except Exception as e: findings.append(Finding(rel,0,"PARSE_FAILURE",str(e))); continue
                for n in ast.walk(tree):
                    if kind=="RSF" and isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in cls.RSF_FORBIDDEN:
                        findings.append(Finding(rel,n.lineno,"RSF_RELEASE_AUTHORITY_LEAK",n.name))
                    if isinstance(n,(ast.Assign,ast.AnnAssign)):
                        targets=n.targets if isinstance(n,ast.Assign) else [n.target]
                        val=n.value
                        for t in targets:
                            if isinstance(t,ast.Name) and t.id.lower() in cls.HARDCODED and isinstance(val,ast.Constant) and val.value is True:
                                findings.append(Finding(rel,getattr(n,"lineno",0),"HARDCODED_PASS_STATE",t.id))
        return not findings,files,findings

    @classmethod
    def _verify_mammoth_integration(cls,project:Path):
        findings=[]
        cert=project/cls.MAMMOTH_CERT_REL
        if not cert.is_file(): findings.append(Finding(str(cls.MAMMOTH_CERT_REL),0,"MAMMOTH_CERTIFICATION_MISSING","certified Mammoth substrate evidence required"))
        else:
            try:
                d=json.loads(cert.read_text())
                if d.get("status")!="CERTIFIED": findings.append(Finding(str(cls.MAMMOTH_CERT_REL),0,"MAMMOTH_NOT_CERTIFIED",str(d.get("status"))))
            except Exception as e: findings.append(Finding(str(cls.MAMMOTH_CERT_REL),0,"MAMMOTH_CERT_PARSE",str(e)))
        gw=project/"aletheus/mammoth/gateway/service.py"
        if not gw.is_file(): findings.append(Finding("aletheus/mammoth/gateway/service.py",0,"MAMMOTH_GATEWAY_MISSING","canonical consumption gateway absent"))
        rsf=project/"aletheus/rsf/genesis_112_20/persistence.py"
        if not rsf.is_file(): findings.append(Finding(str(rsf.relative_to(project)),0,"RSF_PERSISTENCE_INTEGRATION_MISSING","112.20.6 surface absent")); return False,findings
        try: tree=ast.parse(rsf.read_text())
        except Exception as e: findings.append(Finding(str(rsf.relative_to(project)),0,"RSF_PERSISTENCE_PARSE",str(e))); return False,findings
        has_gateway=False; namespace=False
        for n in ast.walk(tree):
            if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="persist": has_gateway=True
            if isinstance(n,ast.Constant) and n.value=="system.assurance.rsf": namespace=True
            if isinstance(n,ast.Call):
                fn=n.func
                if isinstance(fn,ast.Name) and fn.id in {"open"}: findings.append(Finding(str(rsf.relative_to(project)),n.lineno,"PERSISTENCE_BYPASS","open"))
                if isinstance(fn,ast.Attribute) and fn.attr in {"write_text","write_bytes"}: findings.append(Finding(str(rsf.relative_to(project)),n.lineno,"PERSISTENCE_BYPASS",fn.attr))
        if not has_gateway: findings.append(Finding(str(rsf.relative_to(project)),0,"MAMMOTH_GATEWAY_NOT_CONSUMED","gateway.persist call absent"))
        if not namespace: findings.append(Finding(str(rsf.relative_to(project)),0,"RSF_NAMESPACE_NOT_CANONICAL","system.assurance.rsf absent"))
        return not findings,findings

    @classmethod
    def certify(cls,project_root:str|Path,output_directory:str|Path):
        project=Path(project_root).resolve(); out=Path(output_directory).resolve(); out.mkdir(parents=True,exist_ok=True)
        findings=[]
        rsf_root=project/"aletheus/rsf/genesis_112_20"
        for name in cls.REQUIRED_RSF:
            if not (rsf_root/name).is_file(): findings.append(Finding(str((rsf_root/name).relative_to(project)),0,"REQUIRED_RSF_SURFACE_MISSING",name))
        evidence_ok,ef,evidence=cls._verify_rsf_evidence(project); findings+=ef
        boundary_ok,files,bf=cls._scan_boundary(project); findings+=bf
        mammoth_ok,mf=cls._verify_mammoth_integration(project); findings+=mf
        checks={
          "rsfClosureEvidenceDigestVerified":evidence_ok,
          "installedRSFSurfacesPresent":not any(x.rule_id=="REQUIRED_RSF_SURFACE_MISSING" for x in findings),
          "rafRsfConstitutionalBoundaryClean":boundary_ok,
          "noHardcodedPassOrSelfCertificationDetected":not any(x.rule_id in {"HARDCODED_PASS_STATE","RSF_RELEASE_AUTHORITY_LEAK"} for x in findings),
          "mammothBackedPersistenceIntegrationVerified":mammoth_ok,
          "externalRAFIsFinalAuthority":True,
        }
        certified=all(checks.values()) and not findings
        body={"schemaVersion":"1.0.0","standard":"ALETHEUSOS-RAF-EXTERNAL-RSF-PROJECT-CERTIFICATION","genesis":"112.20.9.1","status":FINAL_STATUS if certified else "REFUSED","sourceRSFEvidenceDigest":EXPECTED_RSF_EVIDENCE_DIGEST,"checks":checks,"filesScanned":files,"findings":[asdict(x) for x in findings],"certifiedAtIso":_utc() if certified else None,"authority":{"issuer":"EXTERNAL_RAF_PROJECT_CERTIFICATION_GATE","rsfSelfCertificationAccepted":False}}
        cert_digest=_digest(body); result={**body,"certificationDigest":cert_digest}
        p=out/"genesis-112.20.9.1-external-raf-gold-seal.json"; p.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
        return result,p
