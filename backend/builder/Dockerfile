FROM python:3.10-slim AS message-builder-builder

WORKDIR /opt
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && pip install wheel && pip3 wheel -r requirements.txt --wheel-dir=/opt/wheels


FROM python:3.10-slim

COPY --from=message-builder-builder /opt /opt

WORKDIR /opt/builder
ENTRYPOINT [ "celery", "-A", "builder", "worker", "-l", "info", "-B" ]

COPY . .
RUN  pip install --no-index --find-links=/opt/wheels -r requirements.txt