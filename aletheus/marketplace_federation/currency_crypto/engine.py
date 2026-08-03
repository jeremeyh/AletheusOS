from __future__ import annotations


class Engine:
    def convert(self, amount: float, rate: float, fee: float = 0.0) -> dict[str, float]:
        if amount < 0 or rate <= 0 or fee < 0:
            raise ValueError("invalid conversion")
        gross = amount * rate
        return {
            "gross": round(gross, 8),
            "fee": round(fee, 8),
            "net": round(gross - fee, 8),
        }
