"""
AletheusOS Developer SDK

Genesis 13.46
"""


from .certification import CertificationEngine
from .registry import ExtensionRegistry
from .sandbox import SandboxRuntime


class AletheusDeveloperSDK:


    def __init__(self):

        self.registry = ExtensionRegistry()

        self.sandbox = SandboxRuntime()

        self.certification = CertificationEngine()



    def install(
        self,
        extension
    ):


        review = self.certification.review(
            extension
        )


        return review

