"""Public Constitutional Case Surface."""

from __future__ import annotations

from aletheus.constitutional_cases import CaseStatus


class CaseSurface:
    """Stable read interface over the Constitutional Case Registry."""

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        case_engine,
    ) -> None:
        self._engine = case_engine

    def get(
        self,
        case_id: str,
    ):
        return self._engine.registry.get(case_id)

    def require(
        self,
        case_id: str,
    ):
        return self._engine.registry.require(case_id)

    def list(self):
        return self._engine.registry.list()

    def by_status(
        self,
        status: CaseStatus | str,
    ):
        resolved = status if isinstance(status, CaseStatus) else CaseStatus(status)

        return self._engine.registry.by_status(resolved)

    def history(
        self,
        case_id: str,
    ):
        return self._engine.history(case_id)

    def statistics(self) -> dict:
        return self._engine.registry.statistics()

    def health(self) -> dict:
        return self._engine.health()
