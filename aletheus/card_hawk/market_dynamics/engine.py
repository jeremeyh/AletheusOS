from __future__ import annotations

from math import exp
from typing import Any


class Engine:
    def evaluate(
        self,
        *,
        known_population: int | None,
        active_listings: int,
        sales_velocity_30d: int,
        price_change_90d: float,
        serial_limit: int | None = None,
    ) -> dict[str, Any]:
        denominator = serial_limit or known_population or max(active_listings, 1)
        scarcity = 1.0 - min(1.0, active_listings / max(denominator, 1))
        saturation = min(
            1.0,
            active_listings / max(sales_velocity_30d + active_listings, 1),
        )
        velocity = 1.0 - exp(-max(sales_velocity_30d, 0) / 10.0)
        trend = 1.0 / (1.0 + exp(-price_change_90d * 8.0))
        momentum = min(1.0, max(0.0, velocity * 0.55 + trend * 0.45))
        return {
            "scarcity": scarcity,
            "marketSaturationIndex": saturation,
            "momentum": momentum,
            "inputs": {
                "knownPopulation": known_population,
                "activeListings": active_listings,
                "salesVelocity30d": sales_velocity_30d,
                "priceChange90d": price_change_90d,
                "serialLimit": serial_limit,
            },
        }
