from __future__ import annotations

from .models import OntologyEntity, OntologyRelationship
from .registry import OntologyRegistry, ontology_registry
from .resolver import OntologyResolver
from .validator import OntologyValidationResult, OntologyValidator


class OntologyService:
    """Facade for registering and validating AletheusOS ontology objects."""

    def __init__(self, registry: OntologyRegistry = ontology_registry) -> None:
        self.registry = registry
        self.resolver = OntologyResolver(registry)
        self.validator = OntologyValidator(registry)

    def register_entity(self, entity: OntologyEntity) -> OntologyValidationResult:
        result = self.validator.validate_entity(entity)
        if result.valid:
            self.registry.register_entity(entity)
        return result

    def register_relationship(
        self,
        relationship: OntologyRelationship,
    ) -> OntologyValidationResult:
        self.registry.register_relationship(relationship)
        return self.validator.validate_registry()

    def health(self):
        return self.registry.health()


ontology_service = OntologyService()
