FROM ghcr.io/astral-sh/uv:alpine3.22 AS base

ENV UV_PYTHON_INSTALL_DIR="/usr/local/share/uv/python" \
  VIRTUAL_ENV="/usr/local/venv" \
  PATH="/usr/local/venv/bin:${PATH}"

RUN uv venv -p 3.13 /usr/local/venv

FROM base AS build

WORKDIR /app

RUN apk add --no-cache git=2.49.1-r0

COPY . .

RUN --mount=type=bind,source=.git,destination=.git \
  uv sync --frozen --active && \
  python src/manage.py collectstatic --noinput && \
  uv build

FROM base AS runtime

ENV DJANGO_SETTINGS_MODULE=nu_quran_api.settings \
  DJANGO_DB_PATH=/home/nuqc/db.sqlite3

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

COPY --from=build /app/dist /app/dist

RUN apk add --no-cache tzdata && \
  uv pip install /app/dist/nu_quran_api-*.whl && \
  adduser -Ds /usr/bin/bash nuqc

USER nuqc:nuqc

EXPOSE 8000

ENTRYPOINT ["nu-quran"]

CMD ["server"]
