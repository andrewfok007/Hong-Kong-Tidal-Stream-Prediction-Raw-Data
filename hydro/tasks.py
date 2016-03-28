from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from hydro.utils import get_latest_hydro_data
from hydro.utils import message

logger = get_task_logger(__name__)

# Celery task for retrieving data at 4am everyday
@periodic_task(
    run_every=(crontab(hour='4')),
    name="task_retrieve_hydro_data",
    ignore_result=True
)
def task_retrieve_hydro_data():
    get_latest_hydro_data()
    logger.info(message)
