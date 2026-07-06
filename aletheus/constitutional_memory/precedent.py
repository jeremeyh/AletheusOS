from __future__ import annotations


class ConstitutionalPrecedentEngine:
    GENESIS = "19.5"
    VERSION = "0.1.0"

    PRECEDENT_ORDER = {
        "NONE": 0,
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CANONICAL": 4,
    }

    def strongest(self, records: list[dict]):
        if not records:
            return None

        return max(
            records,
            key=lambda record: self.PRECEDENT_ORDER.get(
                record.get("precedent_weight", "NONE"),
                0,
            ),
        )

    def filter_by_weight(self, records: list[dict], minimum: str = "LOW"):
        minimum_rank = self.PRECEDENT_ORDER.get(minimum, 1)

        return [
            record
            for record in records
            if self.PRECEDENT_ORDER.get(
                record.get("precedent_weight", "NONE"),
                0,
            )
            >= minimum_rank
        ]


constitutional_precedent_engine = ConstitutionalPrecedentEngine()
