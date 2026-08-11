from __future__ import annotations
from pathlib import Path
import ast, re
from typing import Iterable, Tuple
from .models import TopologyNode, TopologyEdge

_CANONICAL_SURFACES = {
    "platform.service.discovery": (
        "aletheus/runtime/registries.py",
        "aletheus/runtime/services/service_registry.py",
    ),
    "platform.service.registration": (
        "aletheus/runtime/managers/registration_manager.py",
    ),
    "platform.engine.registration": (
        "aletheus/runtime/registries.py",
    ),
    "platform.lifecycle.coordination": (
        "aletheus/runtime/managers/lifecycle_manager.py",
    ),
    "platform.runtime.inspection": (
        "aletheus/runtime/inspector/runtime_inspector.py",
        "aletheus/runtime/managers/runtime_inspector.py",
    ),
    "platform.reliability.observation": (
        "aletheus/rsf/genesis_112_20/observation.py",
    ),
}

def _parse(path: Path):
    try:
        return ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None

def _capabilities(path: Path) -> tuple[str, ...]:
    tree = _parse(path)
    if tree is None:
        return ()
    caps = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
            caps.append(node.name)
    return tuple(sorted(set(caps)))

class RuntimeTopologyDiscovery:
    @classmethod
    def discover(cls, project_root: str | Path) -> tuple[tuple[TopologyNode,...], tuple[TopologyEdge,...], dict]:
        root = Path(project_root).resolve()
        nodes = []
        missing = []
        for node_id, rels in _CANONICAL_SURFACES.items():
            existing = [rel for rel in rels if (root/rel).exists()]
            if not existing:
                missing.append(node_id)
                continue
            caps = []
            for rel in existing:
                caps.extend(_capabilities(root/rel))
            owner = "RSF" if node_id == "platform.reliability.observation" else "AletheusOS Runtime"
            lifecycle = "RSF" if node_id == "platform.reliability.observation" else "LifecycleManager"
            nodes.append(TopologyNode(
                node_id=node_id,
                owner_domain=owner,
                implementation_ref="+".join(existing),
                capabilities=tuple(sorted(set(caps))),
                lifecycle_authority=lifecycle,
            ))

        # Declarative edges proven by prior canonical architecture.
        edges = [
            TopologyEdge("platform.service.registration","platform.service.discovery","DEPENDS_ON","AletheusOS Runtime"),
            TopologyEdge("platform.engine.registration","platform.service.registration","COORDINATED_BY","AletheusOS Runtime"),
            TopologyEdge("platform.lifecycle.coordination","platform.service.registration","GOVERNS","AletheusOS Runtime"),
            TopologyEdge("platform.runtime.inspection","platform.service.discovery","OBSERVES","AletheusOS Runtime"),
            TopologyEdge("platform.reliability.observation","platform.runtime.inspection","OBSERVES","RSF"),
        ]

        dormant = []
        rr = root/"aletheus/mesh/runtime_registry.py"
        if rr.exists():
            dormant.append("aletheus/mesh/runtime_registry.py")

        evidence = {
            "missingCanonicalNodes": sorted(missing),
            "dormantKnownSurfaces": dormant,
            "runtimeCoreInspected": (root/"aletheus/runtime/core.py").exists(),
            "automaticRuntimeCoreMutationPermitted": False,
            "sourceMutationPermitted": False,
        }
        return tuple(nodes), tuple(edges), evidence
