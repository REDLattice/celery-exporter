import logging

import celery
import prometheus_client

from .monitor import (
    EnableEventsThread,
    TaskThread,
    WorkerMonitoringThread,
    setup_metrics,
)

__all__ = ("CeleryExporter",)


class CeleryExporter:
    def __init__(
        self,
        broker_url,
        max_tasks=10000,
        namespace="celery",
        transport_options=None,
        enable_events=False,
        broker_use_ssl=None,
    ):
        self._max_tasks = max_tasks
        self._namespace = namespace
        self._enable_events = enable_events

        self._app = celery.Celery(broker=broker_url, broker_use_ssl=broker_use_ssl)
        self._app.conf.broker_transport_options = transport_options or {}

    def start(self):

        setup_metrics(self._app, self._namespace)

        t = TaskThread(
            app=self._app,
            namespace=self._namespace,
            max_tasks_in_memory=self._max_tasks,
        )
        t.daemon = True
        t.start()

        w = WorkerMonitoringThread(app=self._app, namespace=self._namespace)
        w.daemon = True
        w.start()

        if self._enable_events:
            e = EnableEventsThread(app=self._app)
            e.daemon = True
            e.start()
