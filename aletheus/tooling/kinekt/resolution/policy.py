"""Resolution policy for Kinekt™ findings."""

from __future__ import annotations

from dataclasses import dataclass

SUPPRESSED_PATH_PARTS = frozenset(
    {
        ".aletheus_backups",
        ".repository_backups",
        "archive",
        "archives",
        "backup",
        "backups",
        "build",
        "dist",
        "legacy_backup",
        "migrations",
        "node_modules",
        "reports",
        "runtime_state",
        "site-packages",
    }
)

NON_CANONICAL_TOP_LEVEL = frozenset(
    {
        "AletheusOS_Genesis10_Updates",
        "Genesis-012B-SPAN-Runtime-Integration",
        "Genesis10_Work_Organization",
        "Genesis14_SPAN_Constitutional_Intelligence",
        "aletheusos_kernel_sprint1",
    }
)


@dataclass(frozen=True, slots=True)
class ResolutionPolicy:
    suppressed_path_parts: frozenset[str] = SUPPRESSED_PATH_PARTS
    non_canonical_top_level: frozenset[str] = NON_CANONICAL_TOP_LEVEL

    def path_is_suppressed(self, path: str) -> bool:
        normalized = path.replace("\\", "/").lstrip("./")
        parts = tuple(part for part in normalized.split("/") if part)
        if not parts:
            return False
        if parts[0] in self.non_canonical_top_level:
            return True
        return any(part in self.suppressed_path_parts for part in parts)
