from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from .loader import load_object
from .models import Mission, MissionControlReport
from .reporting import write_reports


class MissionControlEngine:
    def __init__(
        self,
        observatory: Path,
        orchestration: Path,
        output: Path,
    ) -> None:
        self.observatory = observatory.resolve()
        self.orchestration = orchestration.resolve()
        self.output = output.resolve()

    def plan(self) -> MissionControlReport:
        observatory = load_object(self.observatory)
        orchestration = load_object(self.orchestration)
        readiness = str(observatory.get("readiness", "unknown"))
        units = orchestration.get("units", [])
        if not isinstance(units, list):
            raise TypeError("Orchestration units must be a list.")

        missions: list[Mission] = []
        blocked: list[str] = []
        for index, unit in enumerate(units):
            if not isinstance(unit, dict):
                continue
            unit_id = str(unit.get("unit_id", f"unit-{index}"))
            missions.append(
                Mission(
                    mission_id=f"mission-{unit_id}",
                    title=str(unit.get("title", unit_id)),
                    status="awaiting_approval",
                    approval_required=True,
                    execution_units=(unit_id,),
                    preconditions=tuple(
                        str(value)
                        for value in unit.get("preconditions", [])
                        if isinstance(value, str)
                    ),
                )
            )

        if readiness == "not_ready":
            blocked.append(
                "Platform readiness is not_ready; missions require Council approval."
            )

        report = MissionControlReport(
            generated_at=datetime.now(UTC).isoformat(),
            readiness=readiness,
            missions=missions,
            blocked_reasons=blocked,
        )
        write_reports(report, self.output)
        return report
