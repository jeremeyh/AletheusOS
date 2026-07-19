from dataclasses import dataclass


@dataclass(frozen=True)
class OwnershipEvent:
    owner: str
    source: str = "manual"

    def __post_init__(self):
        if not self.owner.strip():
            raise ValueError("owner is required")
