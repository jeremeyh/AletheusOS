from engine.def_engine import decide
from engine.thorx.scoring import score_asset
from engine.thorx.confidence import confidence_score
from engine.thorx.q_def import quick_def
from engine.thorx.d_def import deep_def
from engine.thorx.strike_zone import strike_zone
from engine.thorx.projections import project
from engine.thorx.nuclear_cloud import nuclear_cloud

def evaluate_asset(asset: dict) -> dict:
    score_payload = score_asset(asset)
    score = score_payload["score"]
    confidence = confidence_score(score_payload)
    return {
        "asset": asset,
        "score": score,
        "confidence": confidence,
        "recommendation": decide(score, confidence),
        "q_def": quick_def(asset, score),
        "d_def": deep_def(asset, score),
        "strike_zone": strike_zone(asset, score),
        "projections": project(asset, score),
        "nuclear_cloud": nuclear_cloud(asset, score),
    }
