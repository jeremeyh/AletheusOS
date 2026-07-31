class CapitalAllocator:
    """Capital Allocation Engine™."""

    @staticmethod
    def allocate(cash_available, opportunities):
        cash = float(cash_available or 0)
        ranked = sorted(opportunities, key=lambda x: x.get("score", 0), reverse=True)
        plan = []
        remaining = cash

        for opp in ranked:
            if remaining <= 0:
                break
            score = opp.get("score", 0)
            weight = 0.35 if score >= 9.5 else 0.25 if score >= 9 else 0.15
            amount = min(round(cash * weight, 2), remaining)
            plan.append({**opp, "recommended_allocation": amount})
            remaining -= amount

        return {
            "cash_available": cash,
            "deployments": plan,
            "reserve": round(remaining, 2),
        }
