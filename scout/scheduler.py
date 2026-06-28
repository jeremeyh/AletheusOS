from datetime import datetime


class ScoutScheduler:
    """
    Lightweight Scout™ scheduler placeholder.

    Real scheduling will later use cron/APScheduler/background jobs.
    """

    def __init__(self):
        self.jobs = []

    def add_job(self, name: str, query: str, cadence: str = "daily"):
        job = {
            "name": name,
            "query": query,
            "cadence": cadence,
            "created_at": datetime.utcnow().isoformat(),
            "enabled": True,
        }
        self.jobs.append(job)
        return job

    def enabled_jobs(self):
        return [job for job in self.jobs if job["enabled"]]
