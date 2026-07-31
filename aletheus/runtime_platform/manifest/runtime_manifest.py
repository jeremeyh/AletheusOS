from __future__ import annotations

from dataclasses import dataclass, field

from .models import ManifestEntry


@dataclass(frozen=True, slots=True)
class RuntimeManifest:
    name: str
    version: str
    entries: tuple[ManifestEntry, ...] = field(default_factory=tuple)
    metadata: dict[str, object] = field(default_factory=dict)

    def by_kind(
        self,
        kind: str,
    ) -> tuple[ManifestEntry, ...]:
        return tuple(entry for entry in self.entries if entry.kind == kind)

    def names(self) -> tuple[str, ...]:
        return tuple(entry.name for entry in self.entries)
