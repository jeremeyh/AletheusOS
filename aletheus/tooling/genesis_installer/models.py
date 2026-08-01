from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class ReleaseTarget:
    source: str
    destination: str


@dataclass(frozen=True, slots=True)
class ReleaseManifest:
    release_id: str
    version: str
    title: str
    commit_message: str
    package_root: Path
    targets: tuple[ReleaseTarget, ...]
    dependencies: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
