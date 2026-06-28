from datetime import datetime
from timeline.storage.store import store

TIMELINE = store.load()

class TimelineProjection:

    def project(self,event,payload):

        entry={

            "timestamp":datetime.utcnow().isoformat(),

            "event":event,

            "payload":payload

        }

        TIMELINE.append(entry)

        store.save(TIMELINE)

    def timeline(self):

        return TIMELINE

projection=TimelineProjection()
