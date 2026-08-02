from __future__ import annotations

from typing import Any


class Engine:
    def authorize(self, price: float, payment: float) -> dict[str, Any]:
        if price <= 0 or payment <= 0:
            raise ValueError("amounts must be positive")
        return {
            "status": "AUTHORIZED" if payment >= price else "INSUFFICIENT_FUNDS",
            "escrowRequired": True,
        }
