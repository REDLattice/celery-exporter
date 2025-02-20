# Celery Exporter

[![test](https://github.com/REDLattice/celery-exporter/actions/workflows/test.yml/badge.svg)](https://github.com/REDLattice/celery-exporter/actions/workflows/test.yml)

Celery Exporter is a Prometheus metrics exporter for Celery 4, written in python.

Here the list of exposed metrics:

* `celery_tasks_total` exposes the number of tasks currently known to the queue
  labeled by `name`, `state`, `queue` and `namespace`.
* `celery_tasks_runtime_seconds` tracks the number of seconds tasks take
  until completed as histogram labeled by `name`, `queue` and `namespace`
* `celery_tasks_latency_seconds` exposes a histogram of task latency, i.e. the time until
  tasks are picked up by a worker
* `celery_workers` exposes the number of currently probably alive workers

---
## Requirements


### Dependencies
The project comes with `redis` lib already installed, you have to install any other dependency in case you are using other brokers.

### Celery app
Celery workers have to be configured to send task-related events:
http://docs.celeryproject.org/en/latest/userguide/configuration.html#worker-send-task-events.

Celery Exporter is able to enable events on your workers (see _Command Options_).

---
## Install and Run

### Docker
```bash
# Download image
$ docker pull REDLattice/celery-exporter

# Run it
$ docker run -it --rm REDLattice/celery-exporter
```

#### Environment Variables

The module exports an ASGI factory that you can run with something like `uvicorn`. In order to set the broker URL or the metric namespace, use the following environment variables:

```
CELERY_EXPORTER_BROKER_URL=redis://redis:6379/0
CELERY_EXPORTER_NAMESPACE=celery
```

_Previous versions of `celery-exporter` supported setting SSL parameters for communicating with the broker. These are currently not implemented in this version._

If you then look at the exposed metrics, you should see something like this:
```bash
# HELP celery_workers Number of alive workers
# TYPE celery_workers gauge
celery_workers{namespace="celery"} 1.0
# HELP celery_tasks_total Number of tasks per state
# TYPE celery_tasks_total gauge
celery_tasks_total{name="my_app.tasks.calculate_something",namespace="celery",queue="celery",state="RECEIVED"} 0.0
celery_tasks_total{name="my_app.tasks.calculate_something",namespace="celery",queue="celery",state="PENDING"} 0.0
celery_tasks_total{name="my_app.tasks.calculate_something",namespace="celery",queue="celery",state="STARTED"} 0.0
celery_tasks_total{name="my_app.tasks.calculate_something",namespace="celery",queue="celery",state="RETRY"} 0.0
celery_tasks_total{name="my_app.tasks.calculate_something",namespace="celery",queue="celery",state="FAILURE"} 0.0
celery_tasks_total{name="my_app.tasks.calculate_something",namespace="celery",queue="celery",state="REVOKED"} 0.0
celery_tasks_total{name="my_app.tasks.calculate_something",namespace="celery",queue="celery",state="SUCCESS"} 1.0
celery_tasks_total{name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery",state="RECEIVED"} 3.0
celery_tasks_total{name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery",state="PENDING"} 0.0
celery_tasks_total{name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery",state="STARTED"} 1.0
celery_tasks_total{name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery",state="RETRY"} 2.0
celery_tasks_total{name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery",state="FAILURE"} 1.0
celery_tasks_total{name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery",state="REVOKED"} 0.0
celery_tasks_total{name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery",state="SUCCESS"} 7.0
# HELP celery_tasks_runtime_seconds Task runtime (seconds)
# TYPE celery_tasks_runtime_seconds histogram
celery_tasks_runtime_seconds_bucket{le="0.005",name="my_app.tasks.calculate_something",namespace="celery",queue="celery"} 29.0
celery_tasks_runtime_seconds_bucket{le="0.01",name="my_app.tasks.calculate_something",namespace="celery",queue="celery"} 29.0
celery_tasks_runtime_seconds_bucket{le="0.025",name="my_app.tasks.calculate_something",namespace="celery",queue="celery"} 29.0
celery_tasks_runtime_seconds_bucket{le="0.05",name="my_app.tasks.calculate_something",namespace="celery",queue="celery"} 29.0
celery_tasks_runtime_seconds_bucket{le="0.075",name="my_app.tasks.calculate_something",namespace="celery",queue="celery"} 29.0
celery_tasks_runtime_seconds_bucket{le="0.1",name="my_app.tasks.calculate_something",namespace="celery",queue="celery"} 29.0
celery_tasks_runtime_seconds_bucket{le="0.25",name="my_app.tasks.calculate_something",namespace="celery",queue="celery"} 29.0
celery_tasks_runtime_seconds_bucket{le="0.5",name="my_app.tasks.calculate_something",namespace="celery",queue="celery"} 29.0
celery_tasks_runtime_seconds_bucket{le="0.75",name="my_app.tasks.calculate_something",namespace="celery",queue="celery"} 29.0
celery_tasks_runtime_seconds_bucket{le="1.0",name="my_app.tasks.calculate_something",namespace="celery",queue="celery"} 29.0
celery_tasks_runtime_seconds_bucket{le="2.5",name="my_app.tasks.calculate_something",namespace="celery",queue="celery"} 29.0
celery_tasks_runtime_seconds_bucket{le="5.0",name="my_app.tasks.calculate_something",namespace="celery",queue="celery"} 29.0
celery_tasks_runtime_seconds_bucket{le="7.5",name="my_app.tasks.calculate_something",namespace="celery",queue="celery"} 29.0
celery_tasks_runtime_seconds_bucket{le="10.0",name="my_app.tasks.calculate_something",namespace="celery",queue="celery"} 29.0
celery_tasks_runtime_seconds_bucket{le="+Inf",name="my_app.tasks.calculate_something",namespace="celery",queue="celery"} 29.0
celery_tasks_runtime_seconds_count{name="my_app.tasks.calculate_something",namespace="celery",queue="celery"} 29.0
celery_tasks_runtime_seconds_sum{name="my_app.tasks.calculate_something",namespace="celery",queue="celery"} 0.04020289977779612
celery_tasks_runtime_seconds_bucket{le="0.005",name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery"} 2.0
celery_tasks_runtime_seconds_bucket{le="0.01",name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery"} 2.0
celery_tasks_runtime_seconds_bucket{le="0.025",name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery"} 2.0
celery_tasks_runtime_seconds_bucket{le="0.05",name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery"} 2.0
celery_tasks_runtime_seconds_bucket{le="0.075",name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery"} 2.0
celery_tasks_runtime_seconds_bucket{le="0.1",name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery"} 2.0
celery_tasks_runtime_seconds_bucket{le="0.25",name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery"} 2.0
celery_tasks_runtime_seconds_bucket{le="0.5",name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery"} 2.0
celery_tasks_runtime_seconds_bucket{le="0.75",name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery"} 2.0
celery_tasks_runtime_seconds_bucket{le="1.0",name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery"} 2.0
celery_tasks_runtime_seconds_bucket{le="2.5",name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery"} 2.0
celery_tasks_runtime_seconds_bucket{le="5.0",name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery"} 2.0
celery_tasks_runtime_seconds_bucket{le="7.5",name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery"} 2.0
celery_tasks_runtime_seconds_bucket{le="10.0",name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery"} 2.0
celery_tasks_runtime_seconds_bucket{le="+Inf",name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery"} 2.0
celery_tasks_runtime_seconds_count{name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery"} 2.0
celery_tasks_runtime_seconds_sum{name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery"} 0.00402028997777961
# TYPE celery_tasks_runtime_seconds_created gauge
celery_tasks_runtime_seconds_created{name="my_app.tasks.calculate_something",namespace="celery",queue="celery"} 1.548944949810905e+09
celery_tasks_runtime_seconds_created{name="my_app.tasks.fetch_some_data",namespace="celery",queue="celery"} 1.5489449550243628e+09
# HELP celery_tasks_latency_seconds Seconds between a task is received and started.
# TYPE celery_tasks_latency_seconds histogram
celery_tasks_latency_seconds_bucket{namespace="celery",name="my_app.tasks.fetch_some_data",queue="celery",le="0.005"} 2.0
celery_tasks_latency_seconds_bucket{namespace="celery",name="my_app.tasks.fetch_some_data",queue="celery",le="0.01"} 3.0
celery_tasks_latency_seconds_bucket{namespace="celery",name="my_app.tasks.fetch_some_data",queue="celery",le="0.025"} 4.0
celery_tasks_latency_seconds_bucket{namespace="celery",name="my_app.tasks.fetch_some_data",queue="celery",le="0.05"} 4.0
celery_tasks_latency_seconds_bucket{namespace="celery",name="my_app.tasks.fetch_some_data",queue="celery",le="0.075"} 5.0
celery_tasks_latency_seconds_bucket{namespace="celery",name="my_app.tasks.fetch_some_data",queue="celery",le="0.1"} 5.0
celery_tasks_latency_seconds_bucket{namespace="celery",name="my_app.tasks.fetch_some_data",queue="celery",le="0.25"} 5.0
celery_tasks_latency_seconds_bucket{namespace="celery",name="my_app.tasks.fetch_some_data",queue="celery",le="0.5"} 5.0
celery_tasks_latency_seconds_bucket{namespace="celery",name="my_app.tasks.fetch_some_data",queue="celery",le="0.75"} 5.0
celery_tasks_latency_seconds_bucket{namespace="celery",name="my_app.tasks.fetch_some_data",queue="celery",le="1.0"} 5.0
celery_tasks_latency_seconds_bucket{namespace="celery",name="my_app.tasks.fetch_some_data",queue="celery",le="2.5"} 8.0
celery_tasks_latency_seconds_bucket{namespace="celery",name="my_app.tasks.fetch_some_data",queue="celery",le="5.0"} 11.0
celery_tasks_latency_seconds_bucket{namespace="celery",name="my_app.tasks.fetch_some_data",queue="celery",le="7.5"} 11.0
celery_tasks_latency_seconds_bucket{namespace="celery",name="my_app.tasks.fetch_some_data",queue="celery",le="10.0"} 11.0
celery_tasks_latency_seconds_bucket{namespace="celery",name="my_app.tasks.fetch_some_data",queue="celery",le="+Inf"} 11.0
celery_tasks_latency_seconds_count{namespace="celery",name="my_app.tasks.fetch_some_data",queue="celery"} 11.0
celery_tasks_latency_seconds_sum{namespace="celery",name="my_app.tasks.fetch_some_data",queue="celery"} 16.478713035583496
# TYPE celery_task_latency_created gauge
celery_task_latency_seconds_created{namespace="celery",name="my_app.tasks.fetch_some_data",queue="celery"} 1.5489449475378375e+09
```

### Inspired by @zerok work
https://github.com/zerok/celery-prometheus-exporter
