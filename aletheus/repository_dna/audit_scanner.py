from __future__ import annotations

from pathlib import Path

from .audit_models import SubsystemRecord, SubsystemStatus


class RepositoryDNAScanner:
    """Scans the AletheusOS repository for top-level subsystem records."""

    def scan_subsystems(self, aletheus_root: Path) -> list[SubsystemRecord]:
        records: list[SubsystemRecord] = []

        for child in sorted(aletheus_root.iterdir()):
            if not child.is_dir() or child.name.startswith("__"):
                continue

            py_count = len(list(child.rglob("*.py")))
            records.append(
                SubsystemRecord(
                    name=child.name,
                    path=str(child),
                    python_files=py_count,
                    family=self._infer_family(child.name),
                    status=self._infer_status(child.name),
                    notes=[],
                )
            )

        return records

    def count_python_files(self, aletheus_root: Path) -> int:
        return len(list(aletheus_root.rglob("*.py")))

    def _infer_family(self, name: str) -> str:
        n = name.lower()
        if "runtime" in n:
            return "Execution"
        if "kernel" in n:
            return "Kernel"
        if "registry" in n:
            return "Registry"
        if "memory" in n or "knowledge" in n or "cognitive" in n or "neural" in n:
            return "Memory / Cognitive"
        if "constitutional" in n or "council" in n:
            return "Constitutional / Governance"
        if "security" in n or "guardian" in n or "conclave" in n or "identity" in n:
            return "Security / Identity"
        if "mesh" in n:
            return "Mesh"
        if "engine" in n:
            return "Engine"
        if (
            "atlas" in n
            or "oracle" in n
            or "watch" in n
            or "repository" in n
            or "genesis" in n
        ):
            return "Platform Intelligence"
        return "Unclassified"

    def _infer_status(self, name: str) -> SubsystemStatus:
        n = name.lower()
        if n.endswith(("_v2", "_v3")):
            return SubsystemStatus.TRANSITIONAL
        return SubsystemStatus.ACTIVE
