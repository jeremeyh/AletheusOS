from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class RuntimeLifecycleEvent:
    """
    Runtime Lifecycle Event™

    Canonical lifecycle event emitted by the Runtime Lifecycle Manager.
    """

    state: str
    timestamp: str = field(
        default_factory=lambda: datetime.now().astimezone().isoformat()
    )
