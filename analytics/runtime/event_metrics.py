import json
from collections import Counter
from pathlib import Path

LOG = Path("logs/events.jsonl")


def metrics():

    counts = Counter()

    if LOG.exists():
        with LOG.open() as fp:
            for line in fp:
                try:
                    event = json.loads(line)

                    counts[event.get("event", "unknown")] += 1

                except Exception:
                    pass

    return counts
