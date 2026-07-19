from dataclasses import dataclass


@dataclass(frozen=True)
class Identity:
    asset_id: str
    label: str

    def __post_init__(self):
        if not self.asset_id.strip() or not self.label.strip():
            raise ValueError("asset_id and label are required")
