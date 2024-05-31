from abc import ABC, abstractmethod
from typing import Dict, Union, Any

from db_utils import db_requests
from db_utils.db_requests import BaseRequestTypes


class BaseDB(ABC):
    def __init__(self, requester: db_requests.BaseRequester):
        self._requester = requester

    def _get_request_text(self, req_type: BaseRequestTypes,
                          params: Union[Dict[str, Any], None] = None) -> str:
        return self._requester.get_request_text(req_type, params)
