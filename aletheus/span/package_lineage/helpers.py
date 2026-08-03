from __future__ import annotations
from hashlib import sha256
from json import dumps
from pathlib import Path
from typing import Any
IGNORES={".git",".venv","__pycache__","archive","archives","backup","backups","build","dist","legacy_backup","logs","node_modules","reports","span_export","uploads","var"}
def stable_digest(payload: Any)->str:
    return sha256(dumps(payload,sort_keys=True,default=str).encode()).hexdigest()
def ignored(path:Path,root:Path)->bool:
    rel=path.relative_to(root)
    return any(part in IGNORES or part.endswith(".egg-info") for part in rel.parts)
def python_files(root:Path)->list[Path]:
    return sorted(p for p in root.rglob("*.py") if not ignored(p,root))
def packages(root:Path)->list[Path]:
    return sorted(p.parent for p in root.rglob("__init__.py") if not ignored(p,root))
def bounded(v:float)->float:
    return round(max(0.0,min(100.0,v)),4)
