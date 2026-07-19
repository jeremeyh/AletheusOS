#!/bin/bash

set -e

echo "================================================"
echo " AletheusOS Registry Federation Service Registration"
echo " Genesis 12.6.1"
echo "================================================"


DIR="aletheus/runtime/services"

mkdir -p "$DIR"


cat > "$DIR/registry_federation_registration.py" <<'PY'
"""
AletheusOS Registry Federation Service Registration

Genesis 12.6.1

Registers federation capability into runtime services.
"""


from aletheus.runtime.services.registry_federation_service import (
    RegistryFederationService
)


def register_registry_federation(runtime):

    service = RegistryFederationService(
        runtime
    )

    service.initialize()


    if hasattr(runtime, "services"):

        runtime.services.register(
            "registry_federation",
            service
        )


    return service

PY


python3 -m compileall "$DIR/registry_federation_registration.py"


echo ""
echo "Registry Federation Registration Created"
echo "================================================"

