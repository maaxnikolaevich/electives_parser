import logging
from apscheduler.schedulers.background import BackgroundScheduler
from main import run_parser
import asyncio
import time
from settings import app_config

logger = logging.getLogger(__name__)


def run_task_parsing():
    logger.info(f"{time.asctime()}: PARSING TASK LAUNCHED")
    run_parser()
    logger.info(f"{time.asctime()}: PARSING TASK COMPLETE")


class TaskManager:
    def __init__(self):
        logger.info("RUNNING")
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            run_task_parsing, "cron", **app_config["task_manager"]["cron"]
        )

    def run(self):
        try:
            self._start()
        except (KeyboardInterrupt, SystemExit):
            self._stop()

    def _start(self):
        if not self.scheduler.running:
            self.scheduler.start()
        asyncio.get_event_loop().run_forever()

    def _stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown()
