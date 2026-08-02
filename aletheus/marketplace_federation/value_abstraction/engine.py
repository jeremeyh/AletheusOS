from __future__ import annotations


class Engine:
    TYPES = frozenset({"FIAT", "CRYPTO", "STABLECOIN", "CREDIT", "ASSET"})

    def normalize(self, amount: float, unit: str, value_type: str) -> dict[str, object]:
        t = value_type.upper()
        if t not in self.TYPES:
            raise ValueError("unsupported value type")
        return {"amount": float(amount), "unit": unit.upper(), "valueType": t}
