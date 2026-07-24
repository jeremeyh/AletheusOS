"""
Aletheus Universal Intelligence Institutional Civilization Core

Compatibility implementation for the Genesis institutional framework.
"""

from __future__ import annotations

from .models import InstitutionRecord
from .registry import InstitutionRegistry


class InstitutionalCivilizationEngine:
    def __init__(self):
        self._legacy_records = []
        self._registry = InstitutionRegistry()

    def initialize(self):
        return {
            "system": "aletheus_institutional_civilization",
            "range": "2651-2750",
            "status": "operational",
        }

    def create_institution(self, institution):
        #
        # Legacy interface
        #
        if isinstance(institution, str):
            record = {
                "institution": institution,
                "status": "established_legacy",
                "constitutional": False,
            }

            self._legacy_records.append(record)
            return record

        #
        # Constitutional interface
        #
        if isinstance(institution, InstitutionRecord):
            return self._registry.register(institution)

        raise TypeError(
            f"Unsupported institution type: {type(institution)!r}"
        )

    def get_institution(self, institution_id):
        return self._registry.get(institution_id)

    def statistics(self):
        return {
            "legacy_records": len(self._legacy_records),
            "institutions": self._registry.statistics()["institutions"],
        }

    def health(self):
        return {
            "institutions": self._registry.statistics()["institutions"],
            "legacy_records": len(self._legacy_records),
            "status": "healthy",
        }

    def list_institutions(self):
        return self._legacy_records
