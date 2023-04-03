FROM ghcr.io/pyo3/maturin as build

COPY . /io
RUN maturin build --release -o /src/wheelhouse -i python3.9

FROM python:3.9-buster as base-image

ENV LANG=C.UTF-8

ARG BUILD_DATE
ARG DOCKER_REPO
ARG VERSION
ARG VCS_REF

LABEL org.label-schema.schema-version="1.0" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name=$DOCKER_REPO \
      org.label-schema.version=$VERSION \
      org.label-schema.description="Prometheus metrics exporter for Celery" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/RedLattice/celery-exporter"

WORKDIR /app/

COPY --from=build-rs /src/wheelhouse/ /app/wheelhouse/

COPY requirements/ ./requirements
RUN pip install uvicorn
RUN pip install -r ./requirements/requirements.txt

RUN pip install wheelhouse/*

ENTRYPOINT [ "uvicorn", "--factory", "celery_exporter:create_app" ]
CMD []
