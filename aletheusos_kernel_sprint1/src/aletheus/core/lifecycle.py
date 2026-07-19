from enum import StrEnum
class LifecycleState(StrEnum):
    DORMANT="dormant"
    GENESIS="genesis"
    BOOTSTRAP="bootstrap"
    COMPOSE="compose"
    OPERATIONAL="operational"
    ADAPTIVE="adaptive"
    REFLECTIVE="reflective"
    STEWARDSHIP="stewardship"
    REST="rest"
