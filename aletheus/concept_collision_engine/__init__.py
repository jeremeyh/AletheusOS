"""
AletheusOS Concept Collision Engine™

Detects semantic duplication, authority overlap, responsibility creep,
historical supersession, and conceptual drift before new architecture enters
the Super-Mesh.
"""

from .models import (
    CollisionSeverity,
    CollisionType,
    CollisionOutcome,
    ConceptSignature,
    CollisionFinding,
    CollisionReport,
)
from .engine import ConceptCollisionEngine
from .service import ConceptCollisionService

__all__ = [
    "CollisionSeverity",
    "CollisionType",
    "CollisionOutcome",
    "ConceptSignature",
    "CollisionFinding",
    "CollisionReport",
    "ConceptCollisionEngine",
    "ConceptCollisionService",
]
