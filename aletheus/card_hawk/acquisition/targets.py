"""
Target Library

Genesis 13.6
"""


class AcquisitionTargetLibrary:


    def __init__(self):

        self.targets = {}



    def add(
        self,
        target
    ):

        self.targets[
            target.target_id
        ] = target



    def list(self):

        return list(
            self.targets.values()
        )



    def snapshot(self):

        return {

            "target_count":
                len(self.targets)

        }

