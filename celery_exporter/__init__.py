import os

import prometheus_client

from .core import CeleryExporter

def create_app():
    broker_url = os.environ.get("CELERY_EXPORTER_BROKER_URL", "redis://redis:6379/0")
    namespace = os.environ.get("CELERY_EXPORTER_NAMESPACE", "celery")

    # TODO: implement broker SSL support available in the old version
    celery_exporter = CeleryExporter(broker_url=broker_url, namespace=namespace)
    celery_exporter.start()

    app = prometheus_client.make_asgi_app()

    return app