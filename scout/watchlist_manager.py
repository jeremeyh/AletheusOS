from dataclasses import dataclass, field


@dataclass
class WatchTarget:
    query: str
    player: str = ""
    team: str = ""
    max_price: float | None = None
    min_thorx: float = 0.0
    tags: list[str] = field(default_factory=list)


class WatchlistManager:
    """Maintains Scout™ watch targets."""

    def __init__(self):
        self.targets: list[WatchTarget] = []

    def add_target(self, query: str, **kwargs):
        target = WatchTarget(query=query, **kwargs)
        self.targets.append(target)
        return target

    def remove_target(self, query: str):
        self.targets = [target for target in self.targets if target.query != query]

    def all_targets(self):
        return self.targets
