from __future__ import annotations
from json import dumps
from pathlib import Path
from typing import Any, ClassVar
from ..architectural_debt.engine import Engine as ArchitecturalDebt
from ..canonical_registry.engine import Engine as CanonicalRegistry
from ..dead_code_intelligence.engine import Engine as DeadCode
from ..duplicate_intelligence.engine import Engine as Duplicates
from ..namespace_intelligence.engine import Engine as Namespaces
from ..package_lineage.engine import Engine as Lineage
from ..repository_dna.engine import Engine as DNA
from ..repository_health.engine import Engine as Health
from ..repository_intelligence.engine import Engine as Repository
from ..repository_topology.engine import Engine as Topology
from ..span_profiles.engine import Engine as Profiles
from .helpers import stable_digest
class Engine:
    VERSION:ClassVar[str]="36.20.0"
    def __init__(self)->None:
        self._engines=(Repository(),DNA(),CanonicalRegistry(),Lineage(),Duplicates(),Namespaces(),DeadCode(),Topology(),ArchitecturalDebt(),Profiles(),Health())
    def analyze(self,repository_root:str|Path,context:dict[str,Any]|None=None)->dict[str,Any]:
        analyses=[e.analyze(repository_root,context=context) for e in self._engines]; scores=[a["metrics"]["repositoryHealth"] for a in analyses]
        r={"system":"SPAN Repository Intelligence","version":self.VERSION,"genesis":"36.20","analysisCount":len(analyses),"repositoryHealth":round(sum(scores)/max(len(scores),1),4),"analyses":analyses,"constitutionalStatus":"VERIFIED","spartanStatus":"ACTIVE","humanAuthority":"PRESERVED","executionAuthorized":False}; r["digest"]=stable_digest(r); return r
    def write_reports(self,repository_root:str|Path,output_directory:str|Path)->dict[str,Any]:
        r=self.analyze(repository_root); o=Path(output_directory).resolve(); o.mkdir(parents=True,exist_ok=True); (o/"repository_intelligence.json").write_text(dumps(r,indent=2,sort_keys=True)+"\n"); return r
