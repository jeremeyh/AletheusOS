from __future__ import annotations

from plugins.base_plugin import BasePlugin
from services.context import PipelineContext


class Plugin(BasePlugin):
    name = "STRIKE™"
    version = "1.0.0"
    description = "Deal scoring, urgency, confidence, and buy/pass decision layer."

    def execute(self, context: PipelineContext) -> PipelineContext:
        price = float(context.payload.get("price", 0) or 0)
        serial = str(context.payload.get("serial", ""))
        auto = bool(context.payload.get("auto", False))
        patch = bool(context.payload.get("patch", False))
        rookie = bool(context.payload.get("rookie", True))
        score = 50
        if rookie:
            score += 10
        if auto:
            score += 12
        if patch:
            score += 10
        if "/10" in serial or "1/1" in serial:
            score += 15
        elif "/25" in serial:
            score += 10
        elif "/50" in serial:
            score += 6
        if price and price <= 100:
            score += 5
        score = min(score, 99)
        decision = "BUY" if score >= 82 else "WATCH" if score >= 68 else "PASS"
        context.add_result(
            "STRIKE",
            {
                "strike_score": score,
                "decision": decision,
                "confidence": "high"
                if score >= 82
                else "medium"
                if score >= 68
                else "low",
                "urgency": "extreme"
                if score >= 90
                else "high"
                if score >= 82
                else "normal",
                "notes": "STRIKE scored the opportunity using scarcity, asset traits, and price posture.",
            },
        )
        return context
