from dataclasses import dataclass, field


@dataclass
class CapabilityManifest:
    id: str
    name: str
    provider: str
    capability_type: str
    version: str = "1.0"
    status: str = "stable"
    interfaces: list[str] = field(default_factory=list)
    requires: list[str] = field(default_factory=list)
    provides: list[str] = field(default_factory=list)
    developer_visible: bool = True
    marketplace: bool = False
