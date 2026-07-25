from dataclasses import dataclass


@dataclass
class RuntimeContract:

    name: str

    version: str

    capabilities: list[str]
