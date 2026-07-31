import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Offer:
    asset_title: str
    ask_price: float
    offer_price: float
    platform: str = ""
    seller: str = ""
    status: str = "Submitted"
    notes: str = ""
    offer_id: str = field(
        default_factory=lambda: f"OFF-{uuid.uuid4().hex[:10].upper()}"
    )
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class OfferTracker:
    """Offer Tracker™ for acquisition negotiation history."""

    _offers = []

    @classmethod
    def add_offer(
        cls, asset_title, ask_price, offer_price, platform="", seller="", notes=""
    ):
        offer = Offer(
            asset_title, ask_price, offer_price, platform, seller, "Submitted", notes
        )
        cls._offers.append(offer)
        return offer

    @classmethod
    def update_status(cls, offer_id, status):
        for offer in cls._offers:
            if offer.offer_id == offer_id:
                offer.status = status
                return offer
        return None

    @classmethod
    def all(cls):
        return cls._offers

    @classmethod
    def stats(cls):
        total = len(cls._offers)
        accepted = len([o for o in cls._offers if o.status.lower() == "accepted"])
        savings = sum(max(o.ask_price - o.offer_price, 0) for o in cls._offers)
        return {
            "total": total,
            "accepted": accepted,
            "win_rate": (accepted / total * 100) if total else 0,
            "estimated_savings": savings,
        }
