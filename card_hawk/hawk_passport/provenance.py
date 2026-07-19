from dataclasses import dataclass


@dataclass(frozen=True)
class ProvenanceEvent:
    kind: str
    source: str
    note: str = ""

    def __post_init__(self):
        if not self.kind.strip() or not self.source.strip():
            raise ValueError("provenance kind and source are required")
