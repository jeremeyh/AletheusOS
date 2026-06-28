import json
from pathlib import Path
from collections import Counter

LOG = Path("logs/events.jsonl")

def metrics():

    counts = Counter()

    if LOG.exists():

        with LOG.open() as fp:

            for line in fp:

                try:

                    event = json.loads(line)

                    counts[event.get("event","unknown")] += 1

                except Exception:

                    pass

    return counts
