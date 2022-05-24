from abc import ABC, abstractmethod
from typing import Dict, List
from requests import get

from src.parser.result_model import ResultModel


class AbstractSiteParser(ABC):
    _HEADERS = None

    def __init__(self, params: Dict):
        self._parsing_url = params.get("conn_url")

    def _send_request(self):
        response = get(url=self._parsing_url, headers=self._HEADERS)
        return response

    @abstractmethod
    def _handle_data(self):
        pass

    @abstractmethod
    def _send_data_to_db(self):
        pass
