from __future__ import annotations


class Engine:
    def balance(self, values: dict[str, float]) -> dict[str, float]:
        if len(values) < 2:
            raise ValueError("at least two parties required")
        avg = sum(values.values()) / len(values)
        return {k: round(avg - v, 6) for k, v in values.items()}
