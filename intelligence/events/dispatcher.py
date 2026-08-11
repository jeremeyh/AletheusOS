"""
Intelligence Dispatcher
"""

from core.event_bus import event_bus
from intelligence.events.events import *


class Dispatcher:
    def asset_created(self, asset):

        event_bus.publish(ASSET_CREATED, {"asset": asset})

    def dna_completed(self, asset):

        event_bus.publish(DNA_COMPLETED, {"asset": asset})

    def thorx_completed(self, score):

        event_bus.publish(THORX_COMPLETED, score)


dispatcher = Dispatcher()
