"""
Replay Engine
"""

from intelligence.projections.manager import projection_manager
from intelligence.replay.event_store import read_events


class ReplayEngine:

    def replay(self):

        events = read_events()

        count = 0

        for event in events:

            event_name = event.get("event")

            payload = event.get("payload", {})

            for projection in projection_manager.projections:

                if event_name in projection.events:

                    projection.handle(event_name, payload)

            count += 1

        return count


replay_engine = ReplayEngine()
