from logging import getLogger
from sqlalchemy.orm import sessionmaker
from models_db import *
from parser.result_model import ResultModel
from typing import List
from .abstract_site_parser import AbstractSiteParser
import datetime


logger = getLogger(__name__)


class ElectivesSiteSiteParser(AbstractSiteParser):
    _HEADERS = 'headers'

    def __init__(self, conn_db, params):
        super(ElectivesSiteSiteParser, self).__init__(params)
        self._engine = create_engine(
            "{}://{}:{}@{}/{}".format(
                conn_db.get("engine"),
                conn_db.get("username"),
                conn_db.get("password"),
                conn_db.get("host_name"),
                conn_db.get("db_name"),
            ),
            echo=True,
        )

    def __call__(self):
        self._send_data_to_db()

    def _handle_data(self) -> List[ResultModel]:
        data = self._send_request()
        data: List[ResultModel]
        return data

    def _commit_db_objects(
        self,
        title,
        short_description,
        full_description,
        minor,
        elective_tags,
        elective_authors,
        author_description,
    ):
        session = sessionmaker(bind=self._engine)
        session = session()
        curr_minor_obj = None
        if minor is not None:
            curr_minor_obj = (
                session.query(Minor).filter(Minor.title == f"{minor}").first()
            )
            if curr_minor_obj is None:
                curr_minor_obj = Minor(title=f"{minor}")
                session.add(curr_minor_obj)

        elective = session.query(Elective).filter(Elective.title == f"{title}").first()

        if elective is None:
            elective = Elective(
                title=title,
                short_description=short_description,
                full_description=full_description,
                minor=curr_minor_obj,
            )

        if elective_tags is not None:
            for curr_tag in elective_tags:
                curr_tag_obj = (
                    session.query(Tag).filter(Tag.name == f"{curr_tag}").first()
                )
                if curr_tag_obj is None:
                    curr_tag_obj = Tag(name=f"{curr_tag}")
                    elective.tags.append(curr_tag_obj)
                else:
                    elective.tags.append(curr_tag_obj)

        if elective_authors is not None:
            authors = dict(zip(elective_authors, author_description))

            for name, descript in authors.items():
                curr_author_obj = (
                    session.query(Author
                                  ).filter(
                        Author.name == f"{name}"
                        and Author.description == f"{descript}"
                    ).first())

                if curr_author_obj is None:
                    curr_author_obj = Author(
                        name=f"{name}", description=f"{descript}"
                    )
                    elective.authors.append(curr_author_obj)
                else:
                    elective.authors.append(curr_author_obj)

        session.add(elective)
        session.commit()

    def _send_data_to_db(self):
        data_stub = []
        logger.info("STARTED SENDING DATA...")
        begin_time = datetime.datetime.now()
        for item in data_stub:
            self._commit_db_objects(**item)
        logger.info(f"SENDING COMPLETED, time: {datetime.datetime.now() - begin_time}")
