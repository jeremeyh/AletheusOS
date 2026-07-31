from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID, uuid4

from aletheus.core import Result


@dataclass(frozen=True, slots=True)
class MissionContext:
    events: object
    memory: object
    correlation_id: UUID


class Mission(ABC):
    key: str
    name: str

    @abstractmethod
    def execute(self, context) -> Result[dict]:
        raise NotImplementedError

    @staticmethod
    def new_correlation_id():
        return uuid4()
