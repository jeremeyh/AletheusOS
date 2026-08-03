from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass(frozen=True,slots=True)
class RepositoryFinding:
    finding_id:str
    category:str
    severity:str
    summary:str
    evidence:tuple[str,...]=()
    recommendation:str|None=None
@dataclass(frozen=True,slots=True)
class PackageRecord:
    package_id:str
    path:str
    status:str
    generation:int|None=None
    metadata:dict[str,Any]=field(default_factory=dict)
