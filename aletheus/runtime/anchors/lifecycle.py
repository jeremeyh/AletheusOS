"""
Anchor Lifecycle Controller

Genesis 8.5

Controls bounded capability lifecycle.
"""


import time



class AnchorLifecycleController:


    def __init__(self, registry):

        self.registry = registry
        self.history = []



    def attach(self, name):

        anchor = self.registry.get(name)

        if not anchor:

            return {
                "success": False,
                "error": "Anchor not found"
            }


        result = anchor.attach()

        self.record(
            "attach",
            name
        )

        return result



    def detach(self, name):

        anchor = self.registry.get(name)

        if not anchor:

            return {
                "success": False,
                "error": "Anchor not found"
            }


        result = anchor.detach()

        self.record(
            "detach",
            name
        )

        return result



    def restart(self, name):

        self.detach(name)

        time.sleep(0.01)

        return self.attach(name)



    def health(self, name=None):

        if name:

            anchor = self.registry.get(name)

            return (
                anchor.health()
                if anchor
                else None
            )


        return {

            key:
                anchor.health()

            for key, anchor
            in self.registry.anchors.items()

        }



    def record(self, action, anchor):

        self.history.append({

            "action":
                action,

            "anchor":
                anchor,

            "timestamp":
                time.time()

        })



    def history_snapshot(self):

        return self.history
