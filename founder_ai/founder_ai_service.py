class FounderAIService:
    """Founder AI™ rule-based decision assistant for Alpha 2.0."""

    @staticmethod
    def answer(question, context=None):
        q = (question or "").lower()
        context = context or {}

        if "buy" in q:
            return "Review highest THORᵡ opportunities, then check capital allocation and walk-away price."
        if "sell" in q:
            return "Review Exit Strategy™ for assets with high ROI, declining thesis, or weak THORᵡ score."
        if "offer" in q:
            return "Use Negotiation AI™ to set an opening offer and walk-away price."
        if "portfolio" in q:
            return "Open Portfolio Digital Twin™ to simulate purchases and review exposure."
        return "Founder AI™ is online. Ask about buying, selling, offers, or portfolio impact."
