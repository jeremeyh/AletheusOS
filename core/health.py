"""
CardHawk OS™
Health Checks
"""

from core.container import container
from core.scheduler import scheduler


class Health:
    def report(self):

        return {
            "status": "healthy",
            "services": len(container.snapshot()["services"]),
            "engines": len(container.snapshot()["engines"]),
            "providers": len(container.snapshot()["providers"]),
            "jobs": len(scheduler.snapshot()),
        }


health = Health()
