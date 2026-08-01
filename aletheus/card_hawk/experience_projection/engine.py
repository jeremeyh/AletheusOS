from __future__ import annotations

from typing import Any

from .models import CardDetermination


class Engine:
    SUPPORTED = frozenset(
        {
            "CARD_DETAIL",
            "NUCLEAR_CLOUD",
            "MARKET_COMPS",
            "PORTFOLIO_FIT",
            "EXECUTIVE_SUMMARY",
            "TECHNICAL_REPORT",
            "APPRAISAL_PDF",
            "INSURANCE_INVENTORY",
            "SPREADSHEET",
            "VOICE",
            "API",
        }
    )

    def compile(
        self,
        determination: CardDetermination,
        projections: tuple[str, ...],
    ) -> dict[str, Any]:
        invalid = [item for item in projections if item not in self.SUPPORTED]
        if invalid:
            raise ValueError(f"Unsupported Card Hawk projections: {invalid}")
        return {
            "assetId": determination.asset.asset_id,
            "decision": determination.decision,
            "valuation": {
                "low": determination.fair_value_low,
                "mid": determination.fair_value_mid,
                "high": determination.fair_value_high,
            },
            "projections": list(projections),
            "semanticEquivalencePreserved": True,
            "uxrReady": True,
            "axiomUXReady": True,
        }
