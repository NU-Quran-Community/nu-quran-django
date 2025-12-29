FROM ghcr.io/astral-sh/uv:alpine3.22 AS base

RUN adduser -Ds /usr/bin/bash watchtower

USER watchtower:watchtower

WORKDIR /home/watchtower

RUN uv venv -p 3.13 .venv

ENV VIRTUAL_ENV=/home/watchtower/.venv \
  PATH=/home/watchtower/.venv/bin:$PATH

FROM base AS build

WORKDIR /home/watchtower/app

USER root:root

RUN apk add --no-cache git=2.49.1-r0

USER watchtower:watchtower

COPY --chown=watchtower:watchtower src ./src
COPY --chown=watchtower:watchtower pyproject.toml uv.lock ./

RUN --mount=type=bind,source=.git,destination=.git \
  uv sync --frozen --active && \
  uv build

FROM base AS runtime

ENV DJANGO_SETTINGS_MODULE=nu_quran_api.settings

ARG SOURCE_URL=https://github.com/nu-quran-community/nu-quran-django \
  VCS_REF=HEAD \
  VERSION=0.0.0 \
  LICENSE=GPL-3.0-or-later

LABEL org.opencontainers.image.title="NU Quran Django API" \
  org.opencontainers.image.description="NU Quran Community Django backend API" \
  org.opencontainers.image.source="${SOURCE_URL}" \
  org.opencontainers.image.version="${VERSION}" \
  org.opencontainers.image.revision="${VCS_REF}" \
  org.opencontainers.image.licenses="${LICENSE}"

COPY --from=build --chown=watchtower:watchtower /home/watchtower/app/dist /app/dist
RUN uv pip install --find-links=/app/dist nu-quran-api

EXPOSE 8000

ENTRYPOINT ["nu-quran"]

CMD [ "server" ]
