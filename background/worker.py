from datetime import datetime
from background.job_queue import JobQueue

class BackgroundWorker:
    """
    Background Worker™

    Runs queued jobs synchronously for Alpha 2.3B.
    Later this can be replaced with Celery/RQ/APScheduler workers.
    """

    def __init__(self):
        self.handlers = {}

    def register(self, job_type, handler):
        self.handlers[job_type] = handler
        return handler

    def run_once(self):
        ran = []
        for job in JobQueue.queued():
            handler = self.handlers.get(job.job_type)
            if not handler:
                job.status = "skipped"
                job.error = f"No handler registered for {job.job_type}"
                job.updated_at = datetime.utcnow().isoformat()
                ran.append(job)
                continue

            try:
                job.status = "running"
                job.updated_at = datetime.utcnow().isoformat()
                job.result = handler(job.payload) or {}
                job.status = "complete"
            except Exception as exc:
                job.status = "failed"
                job.error = str(exc)

            job.updated_at = datetime.utcnow().isoformat()
            ran.append(job)

        return ran
