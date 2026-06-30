class MeshProtocol:

    version = "2.0.0-e"

    def broadcast(self, message):

        return {

            "status": "broadcast",

            "message": message

        }

    def route(self, destination, message):

        return {

            "status": "sent",

            "destination": destination,

            "message": message

        }


mesh_protocol = MeshProtocol()
