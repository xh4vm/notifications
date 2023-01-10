FROM python:3.10-slim AS admin_panel-builder

WORKDIR /opt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.txt ./

RUN apt-get update && apt-get install -y --no-install-recommends python-dev && \
     pip install --upgrade pip \
     && pip install wheel && pip3 wheel -r requirements.txt --wheel-dir=/opt/wheels


FROM python:3.10-slim

COPY --from=admin_panel-builder /opt /opt

WORKDIR /opt/content

#ENTRYPOINT ["/bin/bash", "-c", "chmod +x ./start.sh && ./start.sh"]

COPY . .

RUN mkdir -p /opt/content/staticfiles && mkdir -p /opt/content/mediafiles && \
    pip install --no-index --find-links=/opt/wheels -r requirements.txt

RUN chmod +x  ./start.sh

ENTRYPOINT ["./start.sh"]