#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="${1:-$(pwd)}"
cd "$ROOT"

mkdir -p reports/span/backups/finding_contract_$(date -u +%Y%m%dT%H%M%SZ)
BACKUP=$(ls -dt reports/span/backups/finding_contract_* | head -1)
cp aletheus/span/finding.py "$BACKUP/finding.py"

cat > aletheus/span/finding.py <<'PY'
"""Canonical SPAN™ finding contracts and collections."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class Severity(str, Enum):
    INFO="info"
    LOW="low"
    MEDIUM="medium"
    HIGH="high"
    CRITICAL="critical"

    @classmethod
    def coerce(cls, value:"Severity|str")->"Severity":
        return value if isinstance(value, cls) else cls(str(value).strip().lower())


@dataclass(slots=True)
class Finding:
    id:str=""
    title:str=""
    category:str=""
    severity:Severity=Severity.INFO
    description:str=""
    summary:str=""
    analyzer:str|None=None
    confidence:float=1.0
    evidence:list[Any]=field(default_factory=list)
    recommendation:str=""
    tags:list[str]=field(default_factory=list)
    metadata:dict[str,Any]=field(default_factory=dict)

    def __post_init__(self)->None:
        self.severity=Severity.coerce(self.severity)
        if self.summary and not self.description:
            self.description=self.summary
        elif self.description and not self.summary:
            self.summary=self.description

        if not self.id:
            base=f"{self.category}:{self.title}:{self.analyzer or ''}"
            self.id=base

        if not self.title.strip():
            raise ValueError("finding title must not be empty")
        if not self.category.strip():
            raise ValueError("finding category must not be empty")
        if not 0.0<=float(self.confidence)<=1.0:
            raise ValueError("finding confidence must be between 0.0 and 1.0")

        self.confidence=float(self.confidence)
        self.evidence=list(self.evidence)
        self.tags=list(dict.fromkeys(map(str,self.tags)))
        self.metadata=dict(self.metadata)

    def to_dict(self)->dict[str,Any]:
        d=asdict(self)
        d["severity"]=self.severity.value
        return d


@dataclass(slots=True)
class FindingSet:
    findings:list[Finding]=field(default_factory=list)
    _ids:set[str]=field(default_factory=set,init=False,repr=False)

    def __post_init__(self):
        initial=list(self.findings)
        self.findings=[]
        self.extend(initial)

    def __iter__(self)->Iterator[Finding]: return iter(self.findings)
    def __len__(self)->int: return len(self.findings)
    def __bool__(self)->bool: return bool(self.findings)

    def add(self,f:Finding)->None:
        if f.id in self._ids:
            raise ValueError(f"duplicate finding id: {f.id}")
        self.findings.append(f); self._ids.add(f.id)

    def extend(self,fs:Iterable[Finding])->None:
        for f in fs: self.add(f)

    def summary(self)->dict[str,Any]:
        sev=Counter(f.severity.value for f in self.findings)
        cat=Counter(f.category for f in self.findings)
        return {
            "total":len(self.findings),
            "by_severity":{s.value:sev.get(s.value,0) for s in Severity},
            "by_category":dict(sorted(cat.items()))
        }

    def to_dict(self)->dict[str,Any]:
        return {"summary":self.summary(),"findings":[f.to_dict() for f in self.findings]}
PY

python -m py_compile aletheus/span/finding.py

python - <<'PY'
from aletheus.span.finding import Finding,Severity

f=Finding(
    analyzer="coupling",
    category="coupling",
    title="Test",
    summary="Legacy summary",
    severity=Severity.MEDIUM,
)
assert f.description=="Legacy summary"
assert f.summary=="Legacy summary"
assert f.id
print("Finding compatibility: OK")
print("Generated id:",f.id)
PY

echo "Genesis 13.2.3 Finding Contract rebuilt successfully."
