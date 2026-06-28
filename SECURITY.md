# Security Policy

CardHawkOS is intended to handle collectible portfolio data, uploaded images,
marketplace data, API credentials, and private business records.

## Security Principles

- Never commit secrets or API keys.
- Store secrets in `.env` or a secure secret manager.
- Keep `.env` out of version control.
- Validate all uploads.
- Avoid storing unnecessary personal data.
- Log errors without exposing secrets.
- Use least-privilege access for external APIs.
- Maintain database backups.
- Separate production data from development data.

## Sensitive Files

The following should not be committed:

- `.env`
- API credentials
- private marketplace exports
- user uploads
- database backups
- logs containing private data

## Reporting Security Issues

Security issues should be treated as private and resolved before public disclosure.
