from aletheus.time_utils import utc_now, utc_now_iso
from datetime import datetime


class HeartbeatService:

    version = "2.0.0-e"

    def pulse(self):

        return {

            "status": "alive",

            "timestamp": utc_now_iso()

        }


heartbeat_service = HeartbeatService()
