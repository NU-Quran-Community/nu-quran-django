FROM ghcr.io/astral-sh/uv:alpine3.22 AS base

ARG PYTHON_VERSION=3.13

RUN adduser -Ds /usr/bin/bash watchtower

USER watchtower:watchtower

WORKDIR /home/watchtower

RUN uv venv -p "${PYTHON_VERSION}" .venv

ENV VIRTUAL_ENV=/home/watchtower/.venv \
  PATH=/home/watchtower/.venv/bin:$PATH

FROM base AS build

WORKDIR /home/watchtower/app

USER watchtower:watchtower

COPY --chown=watchtower:watchtower src ./src
COPY --chown=watchtower:watchtower pyproject.toml uv.lock ./

ARG VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION="${VERSION}"

RUN uv sync --active && \
  uv build

FROM base AS runtime

ENV DJANGO_SETTINGS_MODULE=nu_quran_api.settings \
  DATABASE_URL="sqlite:////home/watchtower/db.sqlite"

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
RUN uv pip install /app/dist/nu_quran_api-"${VERSION}"-*.whl && \
  rm -rf /app/dist

EXPOSE 8000

ENTRYPOINT ["nu-quran"]
CMD [ "server" ]
