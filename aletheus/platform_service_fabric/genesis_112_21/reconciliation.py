from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json

REQUIRED = {
    "mammoth": ("aletheus/mammoth", "reports/mammoth"),
    "rsf": ("aletheus/rsf", "reports/rsf"),
    "raf": ("aletheus/raf", "reports/rsf/genesis-112.20.9.1-external-raf-certification"),
}
COLLISION_SURFACES = (
    "aletheus/service_fabric",
    "aletheus/service_manager",
    "aletheus/foundation_service_bus",
    "aletheus/platform_registry",
    "aletheus/runtime_registry_v2",
)

def _exists_any(root: Path, paths) -> bool:
    return any((root/p).exists() for p in paths)

def _sha256(obj) -> str:
    raw=json.dumps(obj, sort_keys=True, separators=(",",":")).encode()
    return "sha256:"+hashlib.sha256(raw).hexdigest()

@dataclass(frozen=True)
class ReconciliationReport:
    schemaVersion: str
    standard: str
    timestampIso: str
    mode: str
    componentsDiscovered: dict
    collisionSurfaces: list
    constitutionalBoundaryVerified: bool
    reconstructionPermitted: bool
    reconciliationStatus: str
    evidenceDigest: str

class ReconciliationEngine:
    @staticmethod
    def perform(repository_root: str, write_report: bool=False) -> ReconciliationReport:
        root=Path(repository_root).resolve()
        discovered={k:_exists_any(root,v) for k,v in REQUIRED.items()}
        collisions=[p for p in COLLISION_SURFACES if (root/p).exists()]
        # Evidence-based boundary: external RAF certification artifact and RSF surface both exist.
        boundary=discovered["raf"] and discovered["rsf"]
        ready=all(discovered.values()) and boundary
        base={
            "schemaVersion":"1.0.1",
            "standard":"ALETHEUSOS-GENESIS-112.21-RECONCILIATION",
            "timestampIso":datetime.now(timezone.utc).isoformat(),
            "mode":"READ_ONLY_RECONNAISSANCE",
            "componentsDiscovered":discovered,
            "collisionSurfaces":collisions,
            "constitutionalBoundaryVerified":boundary,
            "reconstructionPermitted":ready,
            "reconciliationStatus":"RECONCILED_AND_READY" if ready else "REFUSED",
        }
        report=ReconciliationReport(**base, evidenceDigest=_sha256(base))
        if write_report:
            out=root/"reports/platform-service-fabric/genesis-112.21-reconciliation"
            out.mkdir(parents=True, exist_ok=True)
            (out/"reconciliation-report.json").write_text(json.dumps(asdict(report), indent=2)+"\n")
        return report
