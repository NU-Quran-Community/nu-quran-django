FROM python:3.12-alpine AS build

COPY deps/requirements.prod.txt /usr/local/src/requirements.txt

RUN pip install -r /usr/local/src/requirements.txt

COPY MANIFEST.in pyproject.toml src/ /usr/local/src/

RUN cd /usr/local/src/ && \
  echo yes | python manage.py collectstatic && \
  pip install --no-cache -U pip .

FROM python:3.12-alpine AS runtime

COPY --from=build /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=build /usr/local/bin /usr/local/bin

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/nu-quran"]

CMD [ "server" ]
