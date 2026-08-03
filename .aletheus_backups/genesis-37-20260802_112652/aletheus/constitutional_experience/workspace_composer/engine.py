from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Instrument:
    instrument_id: str
    priority: float = 0.5


class Engine:
    def compose(self, instruments, max_visible: int = 8):
        if max_visible < 1:
            raise ValueError("max_visible must be positive")
        return [
            i.instrument_id
            for i in sorted(instruments, key=lambda x: (-x.priority, x.instrument_id))[
                :max_visible
            ]
        ]
