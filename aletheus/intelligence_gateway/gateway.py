"""
Universal Intelligence Gateway

Genesis 13.43
"""

from .audit import AuditEngine
from .auth import GatewayAuthentication
from .permissions import PermissionEngine
from .registry import APICapabilityRegistry


class IntelligenceGateway:
    def __init__(self):

        self.auth = GatewayAuthentication()

        self.permissions = PermissionEngine()

        self.audit = AuditEngine()

        self.registry = APICapabilityRegistry()

    def execute(self, identity, capability, payload):

        if not self.auth.authenticate(identity):
            return {"error": "unauthorized"}

        permission = self.permissions.authorize(identity, capability)

        if not permission["allowed"]:
            return {"error": "forbidden"}

        return {"capability": capability, "status": "executed"}
