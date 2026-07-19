"""
AletheusOS Repository Management Framework.

This package provides repository inventory, classification, policy validation,
health metrics, reporting, diagnostics, and controlled structural repair.
"""

from .classifier import (
    Classification,
    ClassificationRule,
    RepositoryClassifier,
    build_default_classifier,
)
from .inventory import InventoryEntry, RepositoryInventory
from .metrics import RepositoryMetrics, calculate_metrics
from .rules import PolicyViolation, RepositoryPolicy
from .steward import MoveOperation, RepositorySteward

__all__ = [
    "Classification",
    "ClassificationRule",
    "InventoryEntry",
    "MoveOperation",
    "PolicyViolation",
    "RepositoryClassifier",
    "RepositoryInventory",
    "RepositoryMetrics",
    "RepositoryPolicy",
    "RepositorySteward",
    "build_default_classifier",
    "calculate_metrics",
]
