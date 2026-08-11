from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass
class BuildManifest:
    product: str = "CardHawk OS™"
    release: str = "Alpha 2.3D"
    build: str = "2026.06.xx"
    schema_version: str = "2.4.0"
    pipeline_version: str = "2.4.0"
    database_version: str = "2.4.0"
    created_at: str = datetime.utcnow().isoformat()

    def to_dict(self):
        return asdict(self)
