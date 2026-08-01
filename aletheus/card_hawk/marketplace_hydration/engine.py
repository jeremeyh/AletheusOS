from __future__ import annotations

from statistics import median
from typing import Any

from .models import MarketObservation


class Engine:
    def hydrate(
        self,
        observations: tuple[MarketObservation, ...],
    ) -> dict[str, Any]:
        verified_sales = [
            item.amount
            for item in observations
            if item.verified
            and item.observation_type == "SOLD"
            and item.amount is not None
        ]
        listings = [
            item.amount
            for item in observations
            if item.observation_type == "LISTING" and item.amount is not None
        ]
        return {
            "verifiedSaleCount": len(verified_sales),
            "listingCount": len(listings),
            "medianVerifiedSale": median(verified_sales) if verified_sales else None,
            "medianListing": median(listings) if listings else None,
            "sources": sorted({item.source_id for item in observations}),
            "hydrationStatus": "COMPLETE",
        }
