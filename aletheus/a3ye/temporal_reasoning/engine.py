from __future__ import annotations

from dataclasses import asdict

from .models import TemporalFrame


class Engine:
    def analyze(self, frame: TemporalFrame) -> dict[str, object]:
        return {
            "Tminus1": frame.historical,
            "T0": frame.present,
            "Tplus1": frame.projected,
            "unknownLayer": list(frame.unknowns),
            "futureIsProjection": True,
            "unknownsPreserved": True,
        }

    def compare(self, frame: TemporalFrame) -> dict[str, object]:
        payload = asdict(frame)
        payload["temporalDimensions"] = 4
        return payload
