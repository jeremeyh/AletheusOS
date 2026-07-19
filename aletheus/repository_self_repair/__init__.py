"""AletheusOS Repository Self-Repair subsystem.

Safe-by-default repository diagnosis, normalization, convergence, archival,
and known-orphan remediation.
"""

from .engine import RepositorySelfRepairEngine
from .models import Action, ActionKind, RepairPlan, ScanManifest
from .policy import RepairPolicy

__all__ = [
    "Action",
    "ActionKind",
    "RepairPlan",
    "RepairPolicy",
    "RepositorySelfRepairEngine",
    "ScanManifest",
]
