"""Constitutional Case Registry."""

from __future__ import annotations

from .models import CaseStatus, ConstitutionalCase
from .validation import validate_case


class DuplicateCaseError(ValueError):
    pass


class ConstitutionalCaseRegistry:
    def __init__(self) -> None:
        self._cases: dict[str, ConstitutionalCase] = {}

    def register(
        self,
        case: ConstitutionalCase,
    ) -> ConstitutionalCase:
        validate_case(case)

        if case.case_id in self._cases:
            raise DuplicateCaseError(f"Case {case.case_id!r} already exists.")

        self._cases[case.case_id] = case
        return case

    def get(
        self,
        case_id: str,
    ) -> ConstitutionalCase | None:
        return self._cases.get(case_id)

    def require(
        self,
        case_id: str,
    ) -> ConstitutionalCase:
        case = self.get(case_id)

        if case is None:
            raise KeyError(f"Unknown case: {case_id}")

        return case

    def list(
        self,
    ) -> tuple[ConstitutionalCase, ...]:
        return tuple(self._cases.values())

    def by_status(
        self,
        status: CaseStatus,
    ) -> tuple[ConstitutionalCase, ...]:
        return tuple(case for case in self._cases.values() if case.status == status)

    def statistics(self) -> dict:
        return {
            "cases": len(self._cases),
            "statuses": {
                status.value: len(self.by_status(status)) for status in CaseStatus
            },
        }

    def health(self) -> dict:
        return {
            "name": "Constitutional Case Registry",
            "status": "online",
            **self.statistics(),
        }
