from enum import Enum


class MissionState(str, Enum):
    CREATED = "created"
    VALIDATED = "validated"
    PLANNED = "planned"
    APPROVED = "approved"
    EXECUTING = "executing"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"
