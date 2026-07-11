# syntax=docker/dockerfile:1.7

FROM node:24-alpine AS frontend-builder

WORKDIR /workspace/nimble

COPY nimble/package.json nimble/package-lock.json ./

RUN npm ci

COPY nimble/ ./

RUN npm run typecheck \
    && npm run test -- --run \
    && npm run build


FROM python:3.14-slim AS runtime

ARG ALETHEUS_BUILD_VERSION="development"
ARG ALETHEUS_BUILD_REVISION="unknown"
ARG ALETHEUS_BUILD_CREATED="unknown"
ARG ALETHEUS_BUILD_SOURCE="local"
ARG ALETHEUS_BUILD_REF_NAME="development"

LABEL org.opencontainers.image.title="AletheusOS Nimble Experience Gateway" \
      org.opencontainers.image.description="Governed Nimble experience shell and AletheusOS Experience Gateway" \
      org.opencontainers.image.vendor="6th Dimension Multimedia" \
      org.opencontainers.image.version="${ALETHEUS_BUILD_VERSION}" \
      org.opencontainers.image.revision="${ALETHEUS_BUILD_REVISION}" \
      org.opencontainers.image.created="${ALETHEUS_BUILD_CREATED}" \
      org.opencontainers.image.source="${ALETHEUS_BUILD_SOURCE}" \
      org.opencontainers.image.ref.name="${ALETHEUS_BUILD_REF_NAME}" \
      org.opencontainers.image.licenses="Proprietary"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    ALETHEUS_AUTH_MODE=local \
    ALETHEUS_HOST=0.0.0.0 \
    ALETHEUS_PORT=8000

WORKDIR /app

RUN groupadd \
        --system \
        aletheus \
    && useradd \
        --system \
        --gid aletheus \
        --home-dir /app \
        --shell /usr/sbin/nologin \
        aletheus

COPY pyproject.toml ./
COPY aletheus/ ./aletheus/

RUN python -m pip install --upgrade pip \
    && python -m pip install .

COPY --from=frontend-builder \
    /workspace/nimble/apps/platform-shell/dist \
    /app/nimble/apps/platform-shell/dist

COPY nimble/governance/deployment/deployment-contract.json \
    /app/nimble/governance/deployment/deployment-contract.json

COPY nimble/governance/deployment/build-metadata.json \
    /app/nimble/governance/deployment/build-metadata.json

RUN chown -R aletheus:aletheus /app

USER aletheus

EXPOSE 8000

HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --start-period=10s \
    --retries=3 \
    CMD python -c \
    "import json, urllib.request; payload=json.load(urllib.request.urlopen('http://127.0.0.1:8000/readyz', timeout=3)); raise SystemExit(0 if payload.get('status') == 'ready' else 1)"

CMD [
  "python",
  "-m",
  "uvicorn",
  "aletheus.experience_gateway.fastapi_app:app",
  "--host",
  "0.0.0.0",
  "--port",
  "8000",
  "--no-access-log"
]
