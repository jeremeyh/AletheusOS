"""Aggregated canonical Institution catalog for AletheusOS."""

from __future__ import annotations

from .catalog import canonical_institutions as core_institutions
from .models import InstitutionRecord
from .security_catalog import canonical_security_institutions


def canonical_institutions() -> tuple[InstitutionRecord, ...]:
    """
    Return every canonical AletheusOS institution.

    Core and security catalogs remain bounded source modules while this
    function provides the single public catalog consumed by bootstrapping,
    projection, tests, and future constitutional manifests.
    """

    records = (
        *core_institutions(),
        *canonical_security_institutions(),
    )

    institution_ids = [
        record.institution_id
        for record in records
    ]

    if len(institution_ids) != len(set(institution_ids)):
        duplicates = sorted({
            institution_id
            for institution_id in institution_ids
            if institution_ids.count(institution_id) > 1
        })

        raise ValueError(
            "Duplicate canonical institution IDs: "
            + ", ".join(duplicates)
        )

    return tuple(records)
