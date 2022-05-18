from abc import ABC, abstractmethod
from typing import Dict, List
from requests import get

from result_model import ResultModel


class AbstractSiteParser(ABC):
    def __init__(self, params: Dict):
        self._parsing_url = params.get("parsing_url")

    def _send_request(self):
        response = get(url=self._parsing_url)
        return response

    @abstractmethod
    def _handle_data(self) -> List[ResultModel]:
        pass

    @abstractmethod
    def _send_data_to_db(self):
        pass
