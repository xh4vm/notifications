FROM python:3.10-slim AS message-sender-builder

WORKDIR /opt
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends curl tini \
    && pip install wheel && pip3 wheel -r requirements.txt --wheel-dir=/opt/wheels


FROM python:3.10-slim

COPY --from=message-sender-builder /opt /opt
COPY --from=message-sender-builder /usr/bin/tini /usr/bin/tini

WORKDIR /opt/sender
ENTRYPOINT [ "tini", "--" ]
CMD [ "python3", "./sender.py" ]

COPY . .
RUN  pip install --no-index --find-links=/opt/wheels -r requirements.txt