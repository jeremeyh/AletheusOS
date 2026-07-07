from __future__ import annotations

from .models import ConceptSignature
from .service import ConceptCollisionService


def bootstrap_collision_service() -> ConceptCollisionService:
    service = ConceptCollisionService()

    canonical = [
        ConceptSignature(
            name="Atlas™",
            authority="Atlas™",
            family="Platform Intelligence",
            knows="Architecture",
            owns="Architecture",
            purpose="Architectural knowledge, topology, dependencies, and structural relationships.",
            tags=["architecture", "topology", "dependency", "relationships"],
        ),
        ConceptSignature(
            name="Watch Tower™",
            authority="Watch Tower™",
            family="Platform Intelligence",
            knows="Repository Integrity",
            owns="Repository Integrity",
            purpose="Repository integrity, architectural drift, boundary validation, and collision detection.",
            tags=["repository", "integrity", "drift", "collision", "boundary"],
        ),
        ConceptSignature(
            name="Repository DNA™",
            authority="Repository DNA™",
            family="Platform Intelligence",
            knows="History",
            owns="Architectural History",
            purpose="Institutional memory, lineage, architectural genealogy, and evolution history.",
            tags=["history", "lineage", "genealogy", "memory"],
        ),
        ConceptSignature(
            name="Genesis™",
            authority="Genesis™",
            family="Creation",
            knows="Conformant Scaffolding",
            owns="Creation",
            purpose="Generates constitutionally conformant scaffolding and Genesis Packages.",
            tags=["generation", "scaffolding", "package", "creation"],
        ),
    ]

    service.register_many(canonical)
    return service
