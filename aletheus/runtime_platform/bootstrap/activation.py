from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RuntimeActivationResult:
    activated: bool
    certified: bool
    snapshot_version: str
