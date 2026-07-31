"""
Application Anchor Circuit

Genesis 8

Used by bounded applications:

- Card Hawk
- Enterprise apps
- future products
"""

from .base import RuntimeAnchorCircuit


class ApplicationAnchorCircuit(RuntimeAnchorCircuit):
    def attach(self):

        self.connected = True

        self.runtime.application_anchor = self

        return self.status()

    def capabilities(self):

        return ["application_runtime", "product_extension"]
