from enum import Enum


class RuntimeState(str, Enum):
    CREATED = "created"
    INITIALIZING = "initializing"
    KERNEL_READY = "kernel_ready"
    RUNTIME_READY = "runtime_ready"
    SERVICES_READY = "services_ready"
    APPLICATIONS_LOADED = "applications_loaded"
    OPERATIONAL = "operational"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"
    RECOVERY = "recovery"
    FAILED = "failed"
