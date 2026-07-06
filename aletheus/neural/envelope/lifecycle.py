from __future__ import annotations


class Lifecycle:

    VERSION = "0.1.0"

    def __init__(self, brain):
        self.brain = brain

    def boot(self):

        self.brain.state.set("online")

        self.brain.bootstrap.run()

    def shutdown(self):

        self.brain.state.set("idle")

    def sleep(self):

        self.brain.state.set("dreaming")

    def wake(self):

        self.brain.state.set("online")
