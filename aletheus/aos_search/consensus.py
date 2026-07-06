from __future__ import annotations

from statistics import mean


class SearchConsensus:

    GENESIS = "21.8"
    VERSION = "1.0.0"

    def evaluate(self, provider_results: dict):

        values = []
        evidence = []

        for provider, result in provider_results.items():

            evidence.append(provider)

            if isinstance(result, dict):

                value = result.get("value")

                if isinstance(value, (int, float)):
                    values.append(float(value))

        consensus = {
            "providers": evidence,
            "confidence": 1.0 if evidence else 0.0,
            "reasoning": "",
        }

        if values:
            consensus["estimated_value"] = round(mean(values), 2)
            consensus["reasoning"] = (
                f"Consensus calculated from {len(values)} provider(s)."
            )
        else:
            consensus["reasoning"] = (
                "No numeric consensus available."
            )

        return consensus

    def health(self):

        return {
            "status": "healthy",
            "genesis": self.GENESIS,
            "version": self.VERSION,
        }


search_consensus = SearchConsensus()
