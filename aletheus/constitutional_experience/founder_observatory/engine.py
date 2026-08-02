from collections import Counter

from ..constitutional_isolation.engine import Engine as Isolation
from ..models import ExperienceView


class Engine:
    def summarize(self, events, *, view: ExperienceView, root_attested: bool):
        d = Isolation().authorize(view, "platform_omniscience", root_attested)
        if not d.allowed:
            raise PermissionError(d.reason)
        actors = Counter(str(e.get("actor_type", "unknown")) for e in events)
        actions = Counter(str(e.get("action", "unknown")) for e in events)
        return {
            "actor_activity": dict(sorted(actors.items())),
            "top_actions": actions.most_common(10),
            "visibility": "ecosystem-totality",
            "authority": d.reason,
        }
