from dataclasses import dataclass, field

from aletheus.time_utils import utc_now_iso


@dataclass
class BootReport:
    """
    Runtime Boot Report™

    Captures the phases executed during runtime startup.
    """

    started_at: str = field(default_factory=lambda: utc_now_iso())
    phases: list[str] = field(default_factory=list)
    completed: bool = False

    def record(self, phase_name: str):
        self.phases.append(phase_name)

    def finish(self):
        self.completed = True
