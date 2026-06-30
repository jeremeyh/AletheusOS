class MeshEvents:

    version = "2.0.0-e"

    def publish(self, event):

        return {

            "published": True,

            "event": event

        }


mesh_events = MeshEvents()
