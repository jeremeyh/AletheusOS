"""
CardHawk OS™
Intelligence Event Journal
"""

import json
from datetime import datetime
from pathlib import Path

LOG = Path("logs/events.jsonl")

LOG.parent.mkdir(parents=True, exist_ok=True)


class EventJournal:

    def write(self, event, payload):

        record = {

            "timestamp": datetime.utcnow().isoformat(),

            "event": event,

            "payload": payload

        }

        with LOG.open("a") as fp:

            fp.write(json.dumps(record))

            fp.write("\n")

journal = EventJournal()
