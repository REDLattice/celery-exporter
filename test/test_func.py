from unittest.mock import patch, MagicMock
from celery_test_utils import BaseTest

import celery
import celery_exporter.monitor
from celery_exporter.core import CeleryExporter

setup_metrics_mock = MagicMock(return_value=None)
task_thread_mock = MagicMock(spec=celery_exporter.monitor.TaskThread)
worker_thread_mock = MagicMock(spec=celery_exporter.monitor.WorkerMonitoringThread)
event_thread_mock = MagicMock(spec=celery_exporter.monitor.EnableEventsThread)


@patch("celery.task.control.inspect.registered_tasks", {"worker1": [BaseTest.task]})
@patch("celery_exporter.core.setup_metrics", setup_metrics_mock)
@patch("celery_exporter.core.TaskThread", task_thread_mock)
@patch("celery_exporter.core.WorkerMonitoringThread", worker_thread_mock)
@patch("celery_exporter.core.EnableEventsThread", event_thread_mock)
class TestCeleryExporter(BaseTest):
    def setUp(self):
        self.cel_exp = CeleryExporter(
            broker_url="memory://",
            max_tasks=TestCeleryExporter.max_tasks,
            namespace=TestCeleryExporter.namespace,
            enable_events=True,
        )

    def test_setup_metrics(self):
        self.cel_exp.start()
        setup_metrics_mock.assert_called_with(
            self.cel_exp._app, TestCeleryExporter.namespace
        )

    def test_task_thread(self):
        self.cel_exp.start()
        task_thread_mock.assert_called_with(
            self.cel_exp._app,
            TestCeleryExporter.namespace,
            TestCeleryExporter.max_tasks,
        )

    def test_worker_thread(self):
        self.cel_exp.start()
        worker_thread_mock.assert_called_with(
            self.cel_exp._app, TestCeleryExporter.namespace
        )

    def test_event_thread(self):
        self.cel_exp.start()
        event_thread_mock.assert_called_with(self.cel_exp._app)
