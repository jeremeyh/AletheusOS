from __future__ import annotations
from collections import Counter
from pathlib import Path
from typing import Any, ClassVar
from .helpers import bounded, packages, python_files, stable_digest
class Engine:
    VERSION:ClassVar[str]="36.20.0"
    GENESIS:ClassVar[str]="36.20"
    CAPABILITY:ClassVar[str]="Repository Intelligence"
    def analyze(self,repository_root:str|Path,context:dict[str,Any]|None=None)->dict[str,Any]:
        root=Path(repository_root).expanduser().resolve()
        if not root.exists(): raise FileNotFoundError(root)
        files=python_files(root); pkgs=packages(root); stems=Counter(p.stem for p in files)
        repeated=sum(1 for n in stems.values() if n>1)
        result={"capability":self.CAPABILITY,"genesis":self.GENESIS,"metrics":{"moduleCount":float(len(files)),"packageCount":float(len(pkgs)),"repeatedModuleStemCount":float(repeated),"repositoryHealth":bounded(100.0-min(repeated/max(len(files),1)*20.0,20.0)),"canonicalCoverage":bounded(100.0 if pkgs else 0.0)},"findings":[],"context":context or {},"humanAuthority":"PRESERVED","executionAuthorized":False}
        result["digest"]=stable_digest(result); return result
