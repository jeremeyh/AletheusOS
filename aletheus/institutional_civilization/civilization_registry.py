"""Canonical registry for AletheusOS Civilizations."""

from __future__ import annotations

from collections.abc import Iterable

from .civilization_models import (
    CivilizationRecord,
    CivilizationStatus,
)
from .civilization_validation import validate_civilization


class DuplicateCivilizationError(ValueError):
    """Raised when a canonical Civilization identity is duplicated."""


class CivilizationRegistry:
    """Registry of constitutional civilization domains."""

    def __init__(self) -> None:
        self._records: dict[str, CivilizationRecord] = {}
        self._names: dict[str, str] = {}

    def register(
        self,
        record: CivilizationRecord,
        *,
        replace: bool = False,
    ) -> CivilizationRecord:
        validated = validate_civilization(record)
        normalized_name = validated.canonical_name.strip().casefold()

        existing_id = self._names.get(normalized_name)

        if existing_id is not None and existing_id != validated.civilization_id:
            raise DuplicateCivilizationError(
                f"Civilization name "
                f"{validated.canonical_name!r} is already registered "
                f"as {existing_id!r}."
            )

        if validated.civilization_id in self._records and not replace:
            raise DuplicateCivilizationError(
                f"Civilization {validated.civilization_id!r} is already registered."
            )

        previous = self._records.get(validated.civilization_id)

        if previous is not None:
            self._names.pop(
                previous.canonical_name.strip().casefold(),
                None,
            )

        self._records[validated.civilization_id] = validated
        self._names[normalized_name] = validated.civilization_id
        return validated

    def register_many(
        self,
        records: Iterable[CivilizationRecord],
        *,
        replace: bool = False,
    ) -> tuple[CivilizationRecord, ...]:
        return tuple(self.register(record, replace=replace) for record in records)

    def get(
        self,
        civilization_id: str,
    ) -> CivilizationRecord | None:
        return self._records.get(civilization_id)

    def require(
        self,
        civilization_id: str,
    ) -> CivilizationRecord:
        record = self.get(civilization_id)

        if record is None:
            raise KeyError(f"Unknown civilization: {civilization_id}")

        return record

    def by_name(
        self,
        canonical_name: str,
    ) -> CivilizationRecord | None:
        civilization_id = self._names.get(canonical_name.strip().casefold())

        return self.get(civilization_id) if civilization_id is not None else None

    def list(self) -> tuple[CivilizationRecord, ...]:
        return tuple(
            sorted(
                self._records.values(),
                key=lambda record: record.civilization_id,
            )
        )

    def containing_institution(
        self,
        institution_id: str,
    ) -> tuple[CivilizationRecord, ...]:
        return tuple(
            record for record in self.list() if institution_id in record.institution_ids
        )

    def by_status(
        self,
        status: CivilizationStatus,
    ) -> tuple[CivilizationRecord, ...]:
        return tuple(record for record in self.list() if record.status == status)

    def statistics(self) -> dict:
        institution_memberships = sum(
            len(record.institution_ids) for record in self._records.values()
        )

        return {
            "civilizations": len(self._records),
            "institution_memberships": institution_memberships,
            "civilization_ids": sorted(self._records),
            "statuses": {
                status.value: len(self.by_status(status))
                for status in CivilizationStatus
            },
        }

    def health(self) -> dict:
        return {
            "name": "AletheusOS Civilization Registry",
            "status": "online",
            **self.statistics(),
        }
