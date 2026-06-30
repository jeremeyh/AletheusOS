from dataclasses import dataclass
from typing import List


@dataclass
class RuntimeContract:

    name: str

    version: str

    capabilities: List[str]
