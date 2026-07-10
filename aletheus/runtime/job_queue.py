from __future__ import annotations

from aletheus.time_utils import utc_now, utc_now_iso
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List
import uuid
@dataclass
class RuntimeJob:
    command: str
    payload: Dict[str, Any]
    application: str = 'system'
    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = 'queued'
    created_at: str = field(default_factory=lambda: utc_now_iso())
    completed_at: str | None = None
    result: Dict[str, Any] | None = None
    def to_dict(self) -> Dict[str, Any]: return {'job_id': self.job_id, 'command': self.command, 'payload': self.payload, 'application': self.application, 'status': self.status, 'created_at': self.created_at, 'completed_at': self.completed_at, 'result': self.result}
class JobQueue:
    def __init__(self, runtime: Any) -> None:
        self.runtime = runtime; self.jobs: List[RuntimeJob] = []
    def enqueue(self, command: str, payload: Dict[str, Any] | None = None, application: str = 'system') -> RuntimeJob:
        job = RuntimeJob(command=command, payload=payload or {}, application=application); self.jobs.append(job); return job
    def run_next(self) -> RuntimeJob | None:
        queued = [job for job in self.jobs if job.status == 'queued']
        if not queued: return None
        job = queued[0]; job.status = 'running'
        context = self.runtime.commands.dispatch(job.command, job.payload, application=job.application)
        job.result = context.to_dict(); job.status = 'failed' if context.errors else 'completed'; job.completed_at = utc_now_iso(); return job
    def list(self) -> List[Dict[str, Any]]: return [job.to_dict() for job in self.jobs]
