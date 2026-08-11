from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


def utc_now():
    return datetime.utcnow().isoformat()


# ============================================================
# Federation Node
# ============================================================


@dataclass
class FederationNode:
    node_id: str
    name: str
    address: str

    version: str = "3.4.0"

    capabilities: list[str] = field(default_factory=list)
    services: list[str] = field(default_factory=list)

    status: str = "online"

    last_seen: str = field(default_factory=utc_now)

    metadata: dict[str, Any] = field(default_factory=dict)


# ============================================================
# Federation
# ============================================================


@dataclass
class Federation:
    federation_id: str

    name: str

    created_at: str

    local_node: FederationNode

    remote_nodes: dict[str, FederationNode] = field(default_factory=dict)


# ============================================================
# Engine
# ============================================================


class AletheusFederationEngine:
    VERSION = "3.4.0"

    def __init__(self):

        self.federation: Federation | None = None

    @property
    def version(self):
        return self.VERSION

    # --------------------------------------------------------

    def bootstrap(self):

        if self.federation:
            return self.statistics()

        local = FederationNode(
            node_id=str(uuid.uuid4()),
            name="Local Runtime",
            address="localhost",
            capabilities=[
                "reasoning",
                "planning",
                "workflow",
                "memory",
                "plugins",
                "event_bus",
            ],
            services=[],
        )

        self.federation = Federation(
            federation_id=str(uuid.uuid4()),
            name="Aletheus Federation",
            created_at=utc_now(),
            local_node=local,
        )

        return self.statistics()

    # --------------------------------------------------------

    def join(
        self,
        name,
        address,
        capabilities=None,
        services=None,
    ):

        self.bootstrap()

        node = FederationNode(
            node_id=str(uuid.uuid4()),
            name=name,
            address=address,
            capabilities=capabilities or [],
            services=services or [],
        )

        self.federation.remote_nodes[node.node_id] = node

        return asdict(node)

    # --------------------------------------------------------

    def leave(self, node_id):

        self.bootstrap()

        node = self.federation.remote_nodes.pop(node_id)

        return asdict(node)

    # --------------------------------------------------------

    def discover(self):

        self.bootstrap()

        return [asdict(node) for node in self.federation.remote_nodes.values()]

    # --------------------------------------------------------

    def query(self):

        self.bootstrap()

        return {
            "local": asdict(self.federation.local_node),
            "remote": [asdict(node) for node in self.federation.remote_nodes.values()],
        }

    # --------------------------------------------------------

    def broadcast(self, message):

        self.bootstrap()

        return {
            "message": message,
            "recipients": len(self.federation.remote_nodes),
            "status": "broadcast",
        }

    # --------------------------------------------------------

    def statistics(self):

        if self.federation is None:
            return {
                "version": self.VERSION,
                "federation": None,
                "remote_nodes": 0,
                "health": "not_initialized",
            }

        return {
            "version": self.VERSION,
            "federation": self.federation.name,
            "remote_nodes": len(self.federation.remote_nodes),
            "health": "healthy",
        }


federation_core = AletheusFederationEngine()
