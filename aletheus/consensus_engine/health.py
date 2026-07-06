from .core import consensus_engine


def health():
    return consensus_engine.health()
