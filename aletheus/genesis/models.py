from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path


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
    depends_on: list[str] = field(default_factory=list)
    files_to_add: list[str] = field(default_factory=list)
    files_to_modify: list[str] = field(default_factory=list)
    files_to_delete: list[str] = field(default_factory=list)
    adr: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class GenesisPackagePlan:
    spec: GenesisPackageSpec
    manifest: dict[str, object]
    verification_steps: list[str]
    rollback_steps: list[str]
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass
class GenesisPackageResult:
    spec: GenesisPackageSpec
    output_dir: Path
    files_created: list[Path]
    ready: bool = True
    notes: list[str] = field(default_factory=list)
