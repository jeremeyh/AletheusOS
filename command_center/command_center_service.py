from datalake.intelligence_store import IntelligenceStore
from eventbus.event_bus import EventBus
from founder.dynamic_brief import DynamicFounderBrief
from negotiation.offer_tracker import OfferTracker


class CommandCenterService:
    """Command Center™ 2.0 data orchestration."""

    @staticmethod
    def build(assets):
        events = EventBus.latest(25)
        offers = OfferTracker.all()
        brief = DynamicFounderBrief.generate(assets, events, offers)
        lake_features = IntelligenceStore.features()

        return {
            "brief": brief,
            "events": events,
            "offers": offers,
            "offer_stats": OfferTracker.stats(),
            "lake_features": lake_features,
        }
