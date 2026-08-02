from __future__ import annotations

import math


class Engine:
    WEIGHTS = (0.2, 0.2, 0.2, 0.2, 0.1, 0.1)
    MAX_DELTA = 0.02
    AUTH_MIN = 0.95

    def inspect(self, manifest: tuple[float, ...], actual: tuple[float, ...]) -> dict[str, object]:
        if len(manifest) != 6 or len(actual) != 6:
            raise ValueError("six-dimensional vectors required")
        if actual[5] < self.AUTH_MIN:
            return {"status": "FAILED_COUNTERFEIT_RISK", "topology": "NEBULAR_PROBABILITY"}
        delta = math.sqrt(
            sum(w * ((a - b) ** 2) for w, a, b in zip(self.WEIGHTS, manifest, actual))
        )
        passed = delta <= self.MAX_DELTA
        return {
            "status": "VERIFIED_PASSED" if passed else "FAILED_CONDITION_MISMATCH",
            "delta": round(delta, 6),
            "topology": "CRYSTALLINE_SOLID" if passed else "NEBULAR_PROBABILITY",
        }
