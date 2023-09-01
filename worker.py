import os
import shutil
from pathlib import Path
from celery import Celery
from celery.signals import worker_process_init
from celery.utils.log import get_task_logger

path = Path(__file__).parent.absolute() / ".data/broker"
logger = get_task_logger(__name__)


app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    # broker="filesystem://",
    # broker_transport_options={
    #     "data_folder_in": path / "in",
    #     "data_folder_out": path / "out",
    #     "data_folder_processed": path / "processed",
    # },
    broker_connection_retry_on_startup=True,
    result_persistent=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)


@worker_process_init.connect
def worker_init(**kwargs):
    """
    Create the directories for the broker transport options.
    """
    for _, directory in app.connection().transport_options.items():
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)


@app.task
def task1(payload: dict):
    logger.info(payload)
    return payload
