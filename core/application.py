"""
CardHawk OS™
Application Runtime
"""

from core.bootstrap import bootstrap
from core.engine_registry import engine_registry
from core.event_bus import event_bus
from core.scheduler import scheduler
from core.version import get_version


class Application:

    def __init__(self):

        self.container = bootstrap.boot()

    def info(self):

        return {

            "version": get_version(),

            "engines": list(engine_registry.all().keys()),

            "listeners": event_bus.listeners(),

            "jobs": scheduler.snapshot()

        }


app = Application()


if __name__ == "__main__":

    from pprint import pprint

    pprint(app.info())
