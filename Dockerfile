FROM ghcr.io/astral-sh/uv:alpine3.22 AS base

ENV UV_PYTHON_INSTALL_DIR="/usr/local/share/uv/python" \
  VIRTUAL_ENV="/usr/local/venv" \
  PATH="/usr/local/venv/bin:${PATH}"

RUN uv venv -p 3.13 /usr/local/venv

FROM base AS build

WORKDIR /app

COPY src src/
COPY pyproject.toml uv.lock MANIFEST.in ./

ARG VERSION=0.0.0

ENV SETUPTOOLS_SCM_PRETEND_VERSION="${VERSION}"

RUN uv sync --frozen --active && \
  python src/manage.py collectstatic --noinput && \
  uv build

FROM base AS runtime

ENV DJANGO_SETTINGS_MODULE=nile_quran_community_api.settings \
  DATABASE_URL="sqlite:////home/nqc/db.sqlite"

ARG SOURCE_URL=https://github.com/nile-quran-community/nile-quran-django \
  VCS_REF=HEAD \
  VERSION=0.0.0 \
  LICENSE=GPL-3.0-or-later

LABEL org.opencontainers.image.title="Nile Quran Community Django API" \
  org.opencontainers.image.description="Nile Quran Community Django backend API" \
  org.opencontainers.image.source="${SOURCE_URL}" \
  org.opencontainers.image.version="${VERSION}" \
  org.opencontainers.image.revision="${VCS_REF}" \
  org.opencontainers.image.licenses="${LICENSE}"

COPY --from=build /app/dist /app/dist

RUN apk add --no-cache tzdata && \
  uv pip install /app/dist/nile_quran_community_api-*.whl && \
  adduser -Ds /usr/bin/bash nqc

USER nqc:nqc

EXPOSE 8000

ENTRYPOINT ["nqc"]
CMD ["server"]
