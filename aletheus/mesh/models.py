from aletheus.time_utils import utc_now, utc_now_iso
from dataclasses import dataclass, field
from datetime import datetime
import uuid


def now():
    return utc_now_iso()


@dataclass
class MeshRuntime:

    runtime_name: str
    runtime_type: str

    status: str = "online"

    version: str = "2.0.0-e"

    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    heartbeat: str = field(default_factory=now)

    address: str = "localhost"

    port: int = 8080

    services: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    def ping(self):

        self.heartbeat = now()

    def to_dict(self):

        return self.__dict__
