from .models import RuntimeState, LifecycleTransition


class RuntimeLifecycleManager:
    """
    Runtime Lifecycle Manager™

    Owns runtime state transitions.

    The Executive Kernel decides.
    The Lifecycle Manager performs the transition.
    """

    VALID_STATES = [
        "created",
        "booting",
        "ready",
        "running",
        "paused",
        "recovering",
        "stopping",
        "stopped",
    ]

    def __init__(self):
        self.state = RuntimeState("created")
        self.history = []

    def transition(self, state: str, reason: str = ""):
        if state not in self.VALID_STATES:
            raise ValueError(f"Unknown runtime state: {state}")

        transition = LifecycleTransition(
            previous=self.state.name,
            current=state,
            reason=reason,
        )

        self.history.append(transition)
        self.state = RuntimeState(state)

        return transition

    def health(self):
        return {
            "current_state": self.state.name,
            "transition_count": len(self.history),
            "history": [
                {
                    "from": t.previous,
                    "to": t.current,
                    "reason": t.reason,
                }
                for t in self.history
            ],
        }
