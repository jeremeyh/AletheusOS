class Permissions:
    ROLE_PERMISSIONS = {
        "owner": ["*"],
        "admin": ["read", "write", "export"],
        "viewer": ["read"],
    }

    @staticmethod
    def can(role, action):
        perms = Permissions.ROLE_PERMISSIONS.get(role, [])
        return "*" in perms or action in perms
