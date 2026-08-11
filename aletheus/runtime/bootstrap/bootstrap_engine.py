"""
Bootstrap Engine

Version 5.0.0
"""

from aletheus.runtime.managers import RegistrationManager


class BootstrapEngine:
    def __init__(self, runtime):

        self.runtime = runtime

        self.registration = RegistrationManager(runtime)

    def boot(self):

        self.registration.register_all()

        return True
