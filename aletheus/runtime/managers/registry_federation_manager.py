"""
AletheusOS Registry Federation Manager

Genesis 12.6.3

Runtime composition boundary for federation services.
"""


from aletheus.runtime.services.registry_federation_bootstrap import (
    RegistryFederationBootstrap
)


class RegistryFederationManager:


    def __init__(self, runtime):

        self.runtime = runtime

        self.bootstrap = (
            RegistryFederationBootstrap(
                runtime
            )
        )

        self.status = "created"



    def initialize(self):

        result = (
            self.bootstrap.initialize()
        )

        self.status = "active"

        return result



    def health(self):

        return self.bootstrap.health()

