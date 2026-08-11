from datetime import datetime

from background.job_queue import JobQueue


class RuntimeScheduler:
    """Runtime Scheduler™ registers jobs into the in-process queue."""

    DEFAULT_JOBS = [
        ("Refresh Portfolio Metrics", "portfolio_refresh"),
        ("Run Scout Scan", "scout_scan"),
        ("Generate Founder Brief", "founder_brief"),
        ("Sync Data Lake", "datalake_sync"),
    ]

    @staticmethod
    def schedule_defaults():
        jobs = []
        for name, job_type in RuntimeScheduler.DEFAULT_JOBS:
            jobs.append(
                JobQueue.enqueue(
                    name, job_type, {"scheduled_at": datetime.utcnow().isoformat()}
                )
            )
        return jobs
