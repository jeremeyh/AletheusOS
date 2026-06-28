# Contributing to CardHawkOS

CardHawkOS is a proprietary Card Hawk Collectibles project.

## Development Standards

- Keep `app.py` thin.
- Put reusable UI in `components/`.
- Put page orchestration in `pages/`.
- Put internal business logic in `engine/`.
- Put external API adapters in `integrations/`.
- Put database, cache, auth, logging, and notifications in `services/`.
- Put shared data objects in `models/`.
- Put constants and paths in `config/`.
- Put helpers in `utils/`.

## Naming Standards

- Use lowercase Python filenames.
- Use underscores for multiword modules.
- Preserve product branding in user-facing text:
  - CardHawkOS
  - THORᵡ
  - DEF
  - Hawk A•eye™

## Pull Request Checklist

- Code runs locally.
- Imports are clean.
- No secrets committed.
- No large generated files committed.
- Relevant docs updated.
- Tests added where practical.
