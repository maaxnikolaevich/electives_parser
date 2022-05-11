from .abstract_handler import AbstractSiteParser
from logging import getLogger
from sqlalchemy import create_engine, text


logger = getLogger(__name__)


class ElectivesSiteSiteParser(AbstractSiteParser):
    def __init__(self, conn_db, params):
        super(ElectivesSiteSiteParser, self).__init__(params)
        self._engine = create_engine(
            "{}://{}:{}@{}/{}".format(
                conn_db.get("engine"),
                conn_db.get("username"),
                conn_db.get("password"),
                conn_db.get("host_name"),
                conn_db.get("db_name"),
            ), echo=True
        )

    def __call__(self):
        self._send_data_to_db()

    def _handle_data(self):
        data = self._send_request()

    def _send_data_to_db(self):
        query = text('''insert into test (new_column) values ('helloworld')''')
        self._engine.execute(query)
        logger.info('ok!')
