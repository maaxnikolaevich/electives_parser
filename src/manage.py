from task_manager import TaskManager
import logging

logger = logging.getLogger(__name__)


def run_worker():
    try:
        logger.info('RUN TASK MANAGER...')
        tm = TaskManager()
        tm.run()
    except Exception as exc:
        logger.error(exc, exc_info=True)


if __name__ == "__main__":
    run_worker()
