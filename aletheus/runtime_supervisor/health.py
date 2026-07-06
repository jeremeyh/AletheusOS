from .core import runtime_supervisor


def health():
    return runtime_supervisor.health()
