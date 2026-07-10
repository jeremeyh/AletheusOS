from __future__ import annotations

from aletheus.time_utils import utc_now, utc_now_iso
from datetime import datetime
from typing import Any, Callable, Dict
class Scheduler:
    def __init__(self) -> None: self.jobs: Dict[str, Dict[str, Any]] = {}
    def register(self, name: str, description: str, handler: Callable[[], Any]) -> None: self.jobs[name] = {'description': description, 'handler': handler, 'last_run': None, 'last_result': None}
    def run(self, name: str) -> Any:
        if name not in self.jobs: return {'error': f'Job not registered: {name}'}
        result = self.jobs[name]['handler'](); self.jobs[name]['last_run'] = utc_now_iso(); self.jobs[name]['last_result'] = result; return result
    def list(self) -> Dict[str, Any]: return {name: {'description': job['description'], 'last_run': job['last_run'], 'last_result': job['last_result']} for name, job in self.jobs.items()}
