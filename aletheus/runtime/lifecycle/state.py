from enum import Enum


class RuntimeLifecycleState(str, Enum):
    """
    Runtime Lifecycle State™

    Canonical runtime execution states.
    """

    CREATED = "created"

    INITIALIZING = "initializing"

    BOOTING = "booting"

    ONLINE = "online"

    DEGRADED = "degraded"

    RECOVERING = "recovering"

    SHUTTING_DOWN = "shutting_down"

    OFFLINE = "offline"
