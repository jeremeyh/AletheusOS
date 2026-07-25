"""
CardHawk OS™
Universal Scheduler
"""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScheduledJob:
    name: str
    interval: str
    callback: Callable
    enabled: bool = True
    last_run: str | None = None


class Scheduler:

    def __init__(self):
        self.jobs = {}

    def register(self, name, interval, callback):
        self.jobs[name] = ScheduledJob(
            name=name,
            interval=interval,
            callback=callback,
        )

    def run(self, name):

        if name not in self.jobs:
            return False

        job = self.jobs[name]

        if not job.enabled:
            return False

        job.callback()

        job.last_run = datetime.utcnow().isoformat()

        return True

    def snapshot(self):

        return {
            name: {
                "interval": job.interval,
                "enabled": job.enabled,
                "last_run": job.last_run,
            }
            for name, job in self.jobs.items()
        }


scheduler = Scheduler()
