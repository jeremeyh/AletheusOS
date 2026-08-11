from __future__ import annotations
import ast, json
from dataclasses import asdict, dataclass
from pathlib import Path
from .common import sha256_digest

@dataclass(frozen=True)
class ExistingSurface:
    path: str
    kind: str
    sha256: str

@dataclass(frozen=True)
class ReconciliationReport:
    project_root: str
    existing_surfaces: tuple[ExistingSurface, ...]
    rsf_existing: bool
    raf_existing: bool
    mammoth_existing: bool
    install_mode: str
    destructive_overwrite_required: bool
    report_digest: str

class RSFRAFReconciliationInspector:
    CANDIDATES = (
        ("aletheus/rsf","RSF"),
        ("aletheus/reliability","RELIABILITY"),
        ("aletheus/raf","RAF"),
        ("aletheus/release","RELEASE"),
        ("aletheus/mammoth","MAMMOTH"),
    )

    @classmethod
    def inspect(cls, project_root: str | Path) -> ReconciliationReport:
        project = Path(project_root).resolve()
        found = []
        for rel, kind in cls.CANDIDATES:
            p = project/rel
            if not p.exists():
                continue
            for f in sorted(p.rglob("*.py"))[:500]:
                found.append(ExistingSurface(
                    str(f.relative_to(project)),
                    kind,
                    sha256_digest(f.read_bytes())
                ))
        rsf = any(x.kind in {"RSF","RELIABILITY"} for x in found)
        raf = any(x.kind in {"RAF","RELEASE"} for x in found)
        mammoth = any(x.kind=="MAMMOTH" for x in found)
        body = {
            "projectRoot":str(project),
            "existingSurfaces":[asdict(x) for x in found],
            "rsfExisting":rsf,
            "rafExisting":raf,
            "mammothExisting":mammoth,
            "installMode":"BOUNDED_EXTENSION_UNDER_ALETHEUS_RSF_GENESIS_112_20",
            "destructiveOverwriteRequired":False,
        }
        return ReconciliationReport(
            str(project), tuple(found), rsf, raf, mammoth,
            "BOUNDED_EXTENSION_UNDER_ALETHEUS_RSF_GENESIS_112_20",
            False, sha256_digest(body)
        )
