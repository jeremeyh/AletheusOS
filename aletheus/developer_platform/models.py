"""
Developer Platform Models

Genesis 13.46
"""

from dataclasses import dataclass, field



@dataclass
class ExtensionManifest:


    name: str

    version: str

    extension_type: str

    permissions: list = field(
        default_factory=list
    )

    status: str = "pending"

