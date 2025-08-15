FROM python:3.12-alpine AS build

SHELL ["/bin/sh", "-o", "pipefail", "-c" ]

WORKDIR /usr/local/src

COPY deps/requirements.prod.txt requirements.txt

RUN apk add --no-cache git && \
  pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install --no-cache-dir -U pip . && \
  echo yes | python src/manage.py collectstatic && \
  pip install --no-cache-dir -U pip .

FROM python:3.12-alpine AS runtime

ARG SOURCE_URL=https://github.com/nu-quran-community/nu-quran-django \
  VCS_REF=HEAD \
  VERSION=0.0.0 \
  BUILD_TIME=1970-01-01T00:00:00Z \
  LICENSE=GPL-3.0-or-later

LABEL org.opencontainers.image.title="NU Quran Django API" \
  org.opencontainers.image.description="NU Quran Community Django backend API" \
  org.opencontainers.image.source="${SOURCE_URL}" \
  org.opencontainers.image.version="${VERSION}" \
  org.opencontainers.image.created="${BUILD_TIME}" \
  org.opencontainers.image.revision="${VCS_REF}" \
  org.opencontainers.image.licenses="${LICENSE}"

COPY --from=build /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=build /usr/local/bin /usr/local/bin

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/nu-quran"]

CMD [ "server" ]
