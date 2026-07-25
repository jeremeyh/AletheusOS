import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Job:
    name: str
    job_type: str
    payload: dict = field(default_factory=dict)
    status: str = "queued"
    result: dict = field(default_factory=dict)
    error: str = ""
    job_id: str = field(default_factory=lambda: f"JOB-{uuid.uuid4().hex[:10].upper()}")
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

class JobQueue:
    """In-process job queue for Alpha 2.3B."""

    _jobs = []

    @classmethod
    def enqueue(cls, name, job_type, payload=None):
        job = Job(name=name, job_type=job_type, payload=payload or {})
        cls._jobs.append(job)
        return job

    @classmethod
    def queued(cls):
        return [job for job in cls._jobs if job.status == "queued"]

    @classmethod
    def all(cls):
        return cls._jobs

    @classmethod
    def stats(cls):
        counts = {}
        for job in cls._jobs:
            counts[job.status] = counts.get(job.status, 0) + 1
        return counts
