"""
AletheusOS Concept Collision Engine™

Detects semantic duplication, authority overlap, responsibility creep,
historical supersession, and conceptual drift before new architecture enters
the Super-Mesh.
"""

from .engine import ConceptCollisionEngine
from .models import (
    CollisionFinding,
    CollisionOutcome,
    CollisionReport,
    CollisionSeverity,
    CollisionType,
    ConceptSignature,
)
from .service import ConceptCollisionService

__all__ = [
    "CollisionFinding",
    "CollisionOutcome",
    "CollisionReport",
    "CollisionSeverity",
    "CollisionType",
    "ConceptCollisionEngine",
    "ConceptCollisionService",
    "ConceptSignature",
]
