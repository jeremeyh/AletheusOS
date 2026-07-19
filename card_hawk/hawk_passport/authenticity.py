AUTHENTICITY_STATES = frozenset({"unverified", "review", "verified", "rejected"})


def validate_authenticity_state(state: str) -> str:
    if state not in AUTHENTICITY_STATES:
        raise ValueError(f"unsupported authenticity state: {state}")
    return state
