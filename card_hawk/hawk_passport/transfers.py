from .ownership import OwnershipEvent


def create_transfer(owner: str, source: str = "manual") -> OwnershipEvent:
    return OwnershipEvent(owner=owner, source=source)
