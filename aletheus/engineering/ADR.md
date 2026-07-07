# ADR — GP-00036 Repository DNA ↔ Atlas Integration

Status: Proposed  
Authority: Repository DNA™ / Atlas™  
Classification: Patch-additive  

## Decision

Repository DNA becomes the source of repository inventory. Atlas consumes Repository DNA inventory to build architectural topology instead of independently rediscovering the same repository state.

## Rationale

This removes duplicate discovery responsibility and clarifies authority boundaries:

- Repository DNA knows what exists.
- Atlas knows how it connects.

## Boundary

Repository DNA does not own topology. Atlas does not own repository history.
