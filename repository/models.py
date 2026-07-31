from dataclasses import dataclass
from enum import StrEnum


class RepositoryDomain(StrEnum):
    SOURCE = "source"
    UNKNOWN = "unknown"


@dataclass
class FileRecord:
    path: str
    domain: RepositoryDomain
