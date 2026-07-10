"""
Card Hawk Runtime Lifecycle

Genesis 13.13
"""


class CardHawkLifecycle:


    def __init__(
        self
    ):

        self.status = "created"



    def start(
        self
    ):

        self.status = "running"

        return self.status



    def stop(
        self
    ):

        self.status = "stopped"

        return self.status



    def health(
        self
    ):

        return {

            "status":
                self.status

        }

