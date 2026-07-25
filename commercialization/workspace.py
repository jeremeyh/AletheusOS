import uuid
from dataclasses import dataclass, field


@dataclass
class Workspace:
    name: str
    plan: str = "internal"
    workspace_id: str = field(default_factory=lambda: f"WS-{uuid.uuid4().hex[:10].upper()}")
