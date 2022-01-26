# --------------------------------------------------------------
# Imports
# --------------------------------------------------------------
import logging
from datetime import datetime, timedelta

import prefect
import pytz
from prefect import Flow, Parameter, task
from prefect.executors import LocalDaskExecutor
from prefect.schedules import Schedule
from prefect.schedules.clocks import IntervalClock
from prefect.storage.docker import Docker  # from prefect.storage import Docker
from pysnowflake.simple import Session  # from sqprefect.tasks.snowflake import execute
from slugify import slugify
from sqprefect import find_config

# --------------------------------------------------------------
# Constants
# --------------------------------------------------------------
FLOW_TYPE = "adhoc"  # "adhoc" or "prod"
CONFIG = find_config()
GCP_PROJECT = CONFIG["gcp_project"]
PREFECT_PROJECT = CONFIG["prefect_project"][FLOW_TYPE]

FLOW_NAME = "Example-Prefect-Flows (health/_examples/0001)"
ENVIRONMENT = "production"
AGENT_LABELS = ["local"]
logging.basicConfig(level=logging.INFO)

# --------------------------------------------------------------
# Storage, Schedule, Executor
# --------------------------------------------------------------

# Schedule
schedule = Schedule(
    clocks=[
        IntervalClock(
            start_date=datetime(2021, 12, 16, 0, 1, tzinfo=pytz.timezone("US/Pacific")),
            interval=timedelta(days=1),
        )
    ]
)

# Docker storage is the most flexible for managing your dependencies
storage = Docker(
    dockerfile="Dockerfile",
    registry_url=f"us.gcr.io/{GCP_PROJECT}",
    image_name=slugify(FLOW_NAME),
)

# Default executor will run everything in serial
executor = LocalDaskExecutor()

# --------------------------------------------------------------
# Functions
# --------------------------------------------------------------

# None for this simple example

# --------------------------------------------------------------
# Task Definitions
# --------------------------------------------------------------


@task
def say_hello(name):
    print(f"Hello, {name}!")
    return f"Hello, {name}!"


# --------------------------------------------------------------
# Open a Flow context
# --------------------------------------------------------------
with Flow(
    FLOW_NAME, storage=storage, schedule=schedule, executor=executor
) as health_example:
    first = say_hello("David")

health_example.run()
