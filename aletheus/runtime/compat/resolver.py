from .registry import compatibility_registry


def resolve(alias):

    return compatibility_registry.resolve(alias)
