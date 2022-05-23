import re
from logging import getLogger

from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from src.models_db import *
from src.parser.result_model import ResultModel
from typing import List
from .abstract_site_parser import AbstractSiteParser
import datetime
from requests import get


logger = getLogger(__name__)


class ElectivesSiteSiteParser(AbstractSiteParser):
    _HEADERS = {
        "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/99.0.4844.84 Safari/537.36",
        "accept": "*/*"
    }

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

    def _handle_data(self):
        data = self._send_request().text
        soup = BeautifulSoup(data, "lxml")
        minor_list = soup.find_all("li")
        result_list = []
        for minor in minor_list:
            elective_list = minor.find_all("div", class_="b-minor-elective--item")
            for elective in elective_list:
                elective_attributes = []
                elective_title = elective.find("div", class_="b-minor-elective--title");
                elective_attributes.append(elective_title.text.strip())
                elective_attributes.append(re.sub("^\s+|\n|\r|\s+$", '', elective.find("div",
                                                                                       class_="b-minor-elective--descr").text))
                elective_url = 'https://www.utmn.ru' + elective_title.find("a").get("href")
                elective_page = get(elective_url, headers=self._HEADERS).text
                page_soup = BeautifulSoup(elective_page, 'lxml')
                full_descr = page_soup.find("div", class_='b-minor-content_text')
                if full_descr is not None:
                    elective_attributes.append(full_descr.text.strip())
                else: elective_attributes.append('None')

                authors_list = elective.find_all("div", class_="b-minor-elective--author")
                author_names = []
                author_descrs =[]
                for author in authors_list:
                    author_name = author.find("a", class_="b-minor-elective--author-name")
                    author_descr = author.find("div", class_="b-minor-elective--author-descr")
                    if author_name is not None:
                        author_names.append(
                            re.sub("^\s+|\n|\r|\s+$", '', author_name.text))
                    else: author_names.append('None')
                    if author_descr is not None:
                        author_descrs.append(re.sub("^\s+|\n|\r|\s+$", '', author_descr.text))
                    else: author_descrs.append('None')

                elective_attributes.append(author_names)
                elective_attributes.append(author_descrs)
                tags = []
                tag_list = elective.find_all("div", class_="b-minor-elective--directions__item")
                for tag in tag_list: tags.append(tag.text.strip())
                elective_attributes.append(tags)
                elective_attributes.append(minor.find("div", class_="b-minor-elective--title").text.strip())
                result_list.append({
                    'title': elective_attributes[0],
                    'short_description': elective_attributes[1],
                    'full_description': elective_attributes[2],
                    'elective_authors': elective_attributes[3],
                    'author_description': elective_attributes[4],
                    'elective_tags': elective_attributes[5],
                    'minor': elective_attributes[6]
                })
        return result_list

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
        data_stub = self._handle_data()
        logger.info("STARTED SENDING DATA...")
        begin_time = datetime.datetime.now()
        for item in data_stub:
            self._commit_db_objects(**item)
        logger.info(f"SENDING COMPLETED, time: {datetime.datetime.now() - begin_time}")
