from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timezone


class GenesisClassification(str, Enum):
    FOUNDATION = "foundation"
    PLATFORM = "platform"
    AUTHORITY = "authority"
    SERVICE = "service"
    CAPABILITY = "capability"
    APPLICATION = "application"
    HOTFIX = "hotfix"
    MIGRATION = "migration"
    EXPERIMENTAL = "experimental"


class GenesisRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class GenesisPackageSpec:
    gp_id: str
    title: str
    classification: GenesisClassification
    authority: str
    family: str
    package_name: str
    summary: str
    risk: GenesisRisk = GenesisRisk.LOW
    depends_on: List[str] = field(default_factory=list)
    files_to_add: List[str] = field(default_factory=list)
    files_to_modify: List[str] = field(default_factory=list)
    files_to_delete: List[str] = field(default_factory=list)
    adr: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class GenesisPackagePlan:
    spec: GenesisPackageSpec
    manifest: Dict[str, object]
    verification_steps: List[str]
    rollback_steps: List[str]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class GenesisPackageResult:
    spec: GenesisPackageSpec
    output_dir: Path
    files_created: List[Path]
    ready: bool = True
    notes: List[str] = field(default_factory=list)
