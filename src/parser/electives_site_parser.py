from logging import getLogger
from sqlalchemy.orm import sessionmaker
from models_db import *
from parser.result_model import ResultModel
from typing import List
from .abstract_site_parser import AbstractSiteParser
import datetime


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
        elective_author,
        author_discr,
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
        curr_tag_obj_list: List[Tag] = []

        if elective_tags is not None:
            for curr_tag in elective_tags:
                curr_tag_name = (
                    session.query(Tag).filter(Tag.name == f"{curr_tag}").first()
                )
                if curr_tag_name is None:
                    curr_tag_obj = Tag(name=f"{curr_tag}")
                    curr_tag_obj_list.append(curr_tag_obj)
                    session.add(curr_tag_obj)

        for item in curr_tag_obj_list:
            elective.tags.append(item)

        if elective_author or author_discr is not None:
            authors = dict(zip(elective_author, author_discr))

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

        session.add(elective)
        session.commit()

    def _send_data_to_db(self):
        data_stub = [
            {
                "title": "описание",
                "short_description": "тест",
                "full_description": "тест фулл",
                "minor": "минор",
                "elective_author": ["hfgjh", "hghjg"],
                "author_discr": ["hgjhjghj", "ghhjfhj"],
                "elective_tags": ["dsffdsdf", "dsdggfd"],
            },
            {
                "title": "testt3",
                "short_description": "kdfnk4",
                "full_description": "retrtr",
                "minor": None,
                "elective_author": ["fgdhgd", "hgkjjk"],
                "author_discr": ["xhgfhg", "jhkjhjh"],
                "elective_tags": ["тэг1", "тэг2"],
            },
            {
                "title": "testt5",
                "short_description": "kduuk4",
                "full_description": "ret56",
                "minor": "test",
                "elective_author": ["fdshhdhgf", "fdgh"],
                "author_discr": ["hjgkgh", "hjgjlhjlj"],
                "elective_tags": ["fgjfghj", "jhkiuk"],
            },
        ]
        logger.info("STARTED SENDING DATA...")
        begin_time = datetime.datetime.now()
        for item in data_stub:
            self._commit_db_objects(**item)
        logger.info(f"SENDING COMPLETED, time: {datetime.datetime.now() - begin_time}")
