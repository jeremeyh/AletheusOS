from services.asset_service import AssetService
from services.genome_service import GenomeService


class ThorxService:
    """
    THORᵡ™ Intelligence Service

    V1 scoring stub. This will later become the core intelligence engine.
    """

    @staticmethod
    def score_asset(asset) -> dict:
        scarcity = float(asset["scarcity_score"] or 0)
        visual = float(asset["visual_gravitas_score"] or asset["eye_appeal_score"] or 0)
        player = float(asset["player_thesis_score"] or 0)
        capital = float(asset["capital_efficiency_score"] or 0)
        time = float(asset["time_efficiency_score"] or 0)
        fit = float(asset["portfolio_fit_score"] or 0)

        inputs = [scarcity, visual, player, capital, time, fit]
        non_zero = [x for x in inputs if x > 0]

        if non_zero:
            thorx_score = sum(non_zero) / len(non_zero)
        else:
            # Basic fallback heuristic until D-DEF is implemented.
            thorx_score = 0
            if asset["rookie"]:
                thorx_score += 1.2
            if asset["autograph"]:
                thorx_score += 1.4
            if asset["memorabilia"] or asset["patch"]:
                thorx_score += 1.0
            if asset["serial_number"]:
                thorx_score += 1.3
            if asset["print_run"] and int(asset["print_run"] or 0) <= 25:
                thorx_score += 1.2
            thorx_score = min(10, thorx_score + 4.5)

        if thorx_score >= 9.5:
            classification = "THORᵡ Candidate"
            recommendation = "Aggressively Pursue"
        elif thorx_score >= 9.0:
            classification = "Qualified Kill Shot"
            recommendation = "Acquire"
        elif thorx_score >= 8.0:
            classification = "Cultivation Asset"
            recommendation = "Watch"
        elif thorx_score >= 7.0:
            classification = "Liquidity / Support Asset"
            recommendation = "Hold"
        else:
            classification = "Reject / Pass"
            recommendation = "Pass"

        ni_score = 5 if thorx_score >= 9.5 else 4 if thorx_score >= 9 else 3 if thorx_score >= 8 else 2

        return {
            "thorx_score": round(thorx_score, 2),
            "classification": classification,
            "recommendation": recommendation,
            "ni_score": ni_score,
            "qualification_gate": "Pass" if thorx_score >= 8 else "Fail",
            "strike_zone": 1 if thorx_score >= 9 else 0,
        }

    @staticmethod
    def score_and_update(asset_id: int):
        asset = AssetService.get_by_id(asset_id)
        if not asset:
            return None

        result = ThorxService.score_asset(asset)
        AssetService.update(asset_id, result)

        GenomeService.record_event(
            asset_id=asset_id,
            event_type="THORᵡ Scored",
            event_note=f"THORᵡ score updated to {result['thorx_score']}.",
            new_value=str(result),
            source="THORᵡ",
        )

        return result
