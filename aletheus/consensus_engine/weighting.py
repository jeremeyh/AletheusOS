from __future__ import annotations


class ConsensusWeighting:
    GENESIS = "17.3"
    VERSION = "0.1.0"

    DEFAULT_WEIGHT = 1.0

    def weight_for(self, engine_id: str, weights: dict[str, float] | None = None):
        if not weights:
            return self.DEFAULT_WEIGHT

        return float(weights.get(engine_id, self.DEFAULT_WEIGHT))


consensus_weighting = ConsensusWeighting()
