class ConclaveDecoy:
    def blank(self):
        return {
            "status": "shielded",
            "data": {},
            "message": "No sensitive data available.",
        }

    def anonymous(self):
        return {
            "status": "shielded",
            "data": {
                "user": "anonymous",
                "records": [],
                "secrets": None,
            },
            "message": "Anonymous decoy response issued.",
        }

    def canary(self):
        return {
            "status": "shielded",
            "data": {
                "canary": "CONCLAVE-CANARY-RESPONSE",
                "records": [],
            },
            "message": "Canary decoy response issued.",
        }
