from dataclasses import dataclass, field

from .report import BootReport


@dataclass
class RuntimeBootContext:
    """
    Shared context passed through the boot pipeline.
    """

    report: BootReport = field(default_factory=BootReport)
    timings: dict[str, float] = field(default_factory=dict)
    executed: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
