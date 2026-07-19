"""Canonical registry for AletheusOS constitutional institutions."""

from __future__ import annotations

from collections.abc import Iterable

from .models import (
    ConstitutionalLayer,
    ConstitutionalPillar,
    InstitutionRecord,
    InstitutionStatus,
)
from .validation import validate_institution


class DuplicateInstitutionError(ValueError):
    """Raised when a canonical institutional identity is duplicated."""


class InstitutionRegistry:
    """In-memory canonical registry of institutional definitions."""

    def __init__(self) -> None:
        self._records: dict[str, InstitutionRecord] = {}
        self._names: dict[str, str] = {}

    def register(
        self,
        record: InstitutionRecord,
        *,
        replace: bool = False,
    ) -> InstitutionRecord:
        validated = validate_institution(record)
        normalized_name = validated.canonical_name.strip().casefold()

        existing_id = self._names.get(normalized_name)
        if existing_id and existing_id != validated.institution_id:
            raise DuplicateInstitutionError(
                f"Canonical name {validated.canonical_name!r} is already "
                f"registered as {existing_id!r}."
            )

        if validated.institution_id in self._records and not replace:
            raise DuplicateInstitutionError(
                f"Institution {validated.institution_id!r} is already "
                "registered."
            )

        previous = self._records.get(validated.institution_id)
        if previous is not None:
            self._names.pop(previous.canonical_name.strip().casefold(), None)

        self._records[validated.institution_id] = validated
        self._names[normalized_name] = validated.institution_id
        return validated

    def register_many(
        self,
        records: Iterable[InstitutionRecord],
        *,
        replace: bool = False,
    ) -> tuple[InstitutionRecord, ...]:
        return tuple(
            self.register(record, replace=replace)
            for record in records
        )

    def unregister(self, institution_id: str) -> InstitutionRecord | None:
        record = self._records.pop(institution_id, None)
        if record is not None:
            self._names.pop(record.canonical_name.strip().casefold(), None)
        return record

    def get(self, institution_id: str) -> InstitutionRecord | None:
        return self._records.get(institution_id)

    def require(self, institution_id: str) -> InstitutionRecord:
        record = self.get(institution_id)
        if record is None:
            raise KeyError(f"Unknown institution: {institution_id}")
        return record

    def by_name(self, canonical_name: str) -> InstitutionRecord | None:
        institution_id = self._names.get(canonical_name.strip().casefold())
        return self.get(institution_id) if institution_id else None

    def list(self) -> tuple[InstitutionRecord, ...]:
        return tuple(
            sorted(
                self._records.values(),
                key=lambda record: record.institution_id,
            )
        )

    def by_pillar(
        self,
        pillar: ConstitutionalPillar,
    ) -> tuple[InstitutionRecord, ...]:
        return tuple(
            record
            for record in self.list()
            if record.pillar == pillar
        )

    def by_layer(
        self,
        layer: ConstitutionalLayer,
    ) -> tuple[InstitutionRecord, ...]:
        return tuple(
            record
            for record in self.list()
            if record.constitutional_layer == layer
        )

    def by_status(
        self,
        status: InstitutionStatus,
    ) -> tuple[InstitutionRecord, ...]:
        return tuple(
            record
            for record in self.list()
            if record.status == status
        )

    def statistics(self) -> dict:
        return {
            "institutions": len(self._records),
            "by_pillar": {
                pillar.value: len(self.by_pillar(pillar))
                for pillar in ConstitutionalPillar
            },
            "by_layer": {
                layer.value: len(self.by_layer(layer))
                for layer in ConstitutionalLayer
            },
            "by_status": {
                status.value: len(self.by_status(status))
                for status in InstitutionStatus
            },
            "institution_ids": sorted(self._records),
        }

    def health(self) -> dict:
        return {
            "name": "AletheusOS Institution Registry",
            "status": "online",
            **self.statistics(),
        }
