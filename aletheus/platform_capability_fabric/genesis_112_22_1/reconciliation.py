from __future__ import annotations
import ast, hashlib, json
from pathlib import Path
from .contracts import PREDECESSOR_CERTIFICATION_DIGEST

CERT_REPORT = Path("reports/platform-service-fabric/genesis-112.21.9.1-external-raf-certification")

def _json_digest(obj):
    return "sha256:" + hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",",":")).encode()).hexdigest()

def inspect_repository(root: str):
    root = Path(root).resolve()
    certs = list((root / CERT_REPORT).glob("*.json")) if (root / CERT_REPORT).exists() else []
    predecessor = False
    for p in certs:
        try:
            data=json.loads(p.read_text())
            blob=json.dumps(data, sort_keys=True)
            if "GENESIS_112_21_PLATFORM_SERVICE_FABRIC_PROJECT_CERTIFIED" in blob and PREDECESSOR_CERTIFICATION_DIGEST.split(":",1)[1] in blob:
                predecessor=True
        except Exception:
            pass

    capability_surfaces=[]
    parse_errors=[]
    for p in (root/"aletheus").rglob("*.py") if (root/"aletheus").exists() else []:
        rel=str(p.relative_to(root))
        try:
            tree=ast.parse(p.read_text(errors="ignore"))
        except Exception as e:
            parse_errors.append({"path":rel,"error":type(e).__name__})
            continue
        names=[n.name for n in ast.walk(tree) if isinstance(n,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef))]
        low=rel.lower()
        if any(x in low for x in ("engine","security","spartan","perception","a3ye","a_3ye","framework","capabilit")):
            capability_surfaces.append({"path":rel,"symbols":names[:40]})
    report={
        "schemaVersion":"1.0.0",
        "standard":"ALETHEUSOS-PLATFORM-CAPABILITY-INTEGRATION-FABRIC-RECONNAISSANCE",
        "genesis":"112.22.1",
        "predecessorCertificationDigestExpected":PREDECESSOR_CERTIFICATION_DIGEST,
        "predecessorCertified":predecessor,
        "capabilitySurfacesDiscovered":capability_surfaces,
        "parseErrors":parse_errors,
        "sourceMutationAuthorized":False,
        "runtimeCoreMutationAuthorized":False,
        "canonicalPromotionAuthorized":False,
        "status":"CAPABILITY_RECONNAISSANCE_READY" if predecessor and not parse_errors else "REFUSED",
    }
    report["evidenceDigest"]=_json_digest(report)
    return report
