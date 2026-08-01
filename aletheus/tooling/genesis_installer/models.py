from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ReleaseManifest:
    release_id: str
    version: str
    title: str
    commit_message: str
    package_root: Path
    targets: list[str]
    dependencies: list[str] = field(default_factory=list)
    validation_commands: list[list[str]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
