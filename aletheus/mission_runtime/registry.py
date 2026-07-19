"""Registry of institution phase executors."""

from __future__ import annotations

from .contracts import InstitutionPhaseExecutor


class DuplicateInstitutionExecutorError(ValueError):
    pass


class InstitutionExecutorRegistry:
    def __init__(self) -> None:
        self._executors: dict[
            str,
            InstitutionPhaseExecutor,
        ] = {}

    def register(
        self,
        executor: InstitutionPhaseExecutor,
        *,
        replace: bool = False,
    ) -> InstitutionPhaseExecutor:
        institution_id = executor.institution_id

        if (
            institution_id in self._executors
            and not replace
        ):
            raise DuplicateInstitutionExecutorError(
                f"Executor for {institution_id!r} is already registered."
            )

        self._executors[institution_id] = executor
        return executor

    def get(
        self,
        institution_id: str,
    ) -> InstitutionPhaseExecutor | None:
        return self._executors.get(institution_id)

    def require(
        self,
        institution_id: str,
    ) -> InstitutionPhaseExecutor:
        executor = self.get(institution_id)

        if executor is None:
            raise KeyError(
                f"No executor registered for institution "
                f"{institution_id!r}."
            )

        return executor

    def list(
        self,
    ) -> tuple[InstitutionPhaseExecutor, ...]:
        return tuple(self._executors.values())

    def statistics(self) -> dict:
        return {
            "executors": len(self._executors),
            "institution_ids": sorted(self._executors),
        }

    def health(self) -> dict:
        return {
            "name": "Institution Executor Registry",
            "status": "online",
            **self.statistics(),
        }
