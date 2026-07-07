from dataclasses import dataclass, field
from time import perf_counter


@dataclass
class BootTiming:

    phase: str
    started: float = field(default_factory=perf_counter)
    finished: float | None = None

    def stop(self):
        self.finished = perf_counter()

    @property
    def milliseconds(self):
        if self.finished is None:
            return 0.0
        return (self.finished - self.started) * 1000.0
