from __future__ import annotations

from dataclasses import dataclass, field

from .models import OntologyEntity, OntologyEntityType, OntologyStatus, RelationshipType
from .registry import OntologyRegistry, ontology_registry


@dataclass
class OntologyValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class OntologyValidator:
    """
    Validates ontology integrity and core AletheusOS doctrine.

    Initial rules focus on authority sentences, sovereign ownership,
    retired naming, and relationship referential integrity.
    """

    def __init__(self, registry: OntologyRegistry = ontology_registry) -> None:
        self.registry = registry

    def validate_entity(self, entity: OntologyEntity) -> OntologyValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        if not entity.entity_id:
            errors.append("entity_id is required")
        if not entity.name:
            errors.append("name is required")

        if entity.entity_type == OntologyEntityType.AUTHORITY:
            if not entity.authority_sentence:
                errors.append("authority_sentence is required for Authority entities")
            if entity.status == OntologyStatus.CANONICAL and not entity.family:
                warnings.append("canonical authority should belong to a family")

        if "aletheum" in entity.name.lower() and entity.status not in {
            OntologyStatus.ARCHIVED,
            OntologyStatus.HISTORICAL,
            OntologyStatus.SUPERSEDED,
        }:
            errors.append("Aletheum naming is retired and must remain archived unless explicitly revived")

        return OntologyValidationResult(
            valid=not errors,
            errors=errors,
            warnings=warnings,
        )

    def validate_registry(self) -> OntologyValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        entity_ids = {entity.entity_id for entity in self.registry.all_entities()}

        for relationship in self.registry.all_relationships():
            if relationship.source_entity_id not in entity_ids:
                errors.append(
                    f"relationship {relationship.relationship_id} has missing source {relationship.source_entity_id}"
                )
            if relationship.target_entity_id not in entity_ids:
                errors.append(
                    f"relationship {relationship.relationship_id} has missing target {relationship.target_entity_id}"
                )

        for entity in self.registry.all_entities():
            result = self.validate_entity(entity)
            errors.extend(result.errors)
            warnings.extend(result.warnings)

        self._validate_authority_sovereignty(errors, warnings)

        return OntologyValidationResult(
            valid=not errors,
            errors=errors,
            warnings=warnings,
        )

    def _validate_authority_sovereignty(
        self,
        errors: list[str],
        warnings: list[str],
    ) -> None:
        owners_by_target = {}
        for relationship in self.registry.all_relationships():
            if relationship.relationship_type != RelationshipType.OWNS:
                continue
            owners_by_target.setdefault(
                relationship.target_entity_id,
                [],
            ).append(relationship.source_entity_id)

        for target_id, owner_ids in owners_by_target.items():
            if len(set(owner_ids)) > 1:
                errors.append(
                    f"authority sovereignty violation: {target_id} has multiple owners {sorted(set(owner_ids))}"
                )
