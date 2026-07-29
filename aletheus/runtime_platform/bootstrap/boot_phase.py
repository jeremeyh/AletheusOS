from __future__ import annotations

from enum import Enum


class BootPhase(str, Enum):
    CREATED = "created"
    BOOTSTRAP = "bootstrap"
    COMPOSE = "compose"
    REGISTER = "register"
    RESOLVE_DEPENDENCIES = "resolve_dependencies"
    VALIDATE = "validate"
    ACTIVATE = "activate"
    CERTIFY = "certify"
    READY = "ready"
    FAILED = "failed"
    STOPPING = "stopping"
    STOPPED = "stopped"
