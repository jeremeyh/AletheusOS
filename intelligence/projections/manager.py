"""
Projection Manager
"""

from core.event_bus import event_bus

class ProjectionManager:

    def __init__(self):
        self.projections = []

    def register(self, projection):

        self.projections.append(projection)

        for event in projection.events:

            event_bus.subscribe(
                event,
                lambda payload, e=event, p=projection: p.handle(e, payload)
            )

    def list(self):

        return [p.name for p in self.projections]


projection_manager = ProjectionManager()
