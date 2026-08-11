from intelligence.projections.base import Projection
from timeline.engine.projection import projection


class TimelineProjection(Projection):
    name = "Timeline"

    events = [
        "asset.created",
        "dna.completed",
        "thorx.completed",
        "portfolio.updated",
        "founder.updated",
    ]

    def handle(self, event, payload):

        projection.project(event, payload)


TIMELINE_PROJECTION = TimelineProjection()
