import enum
from abc import ABC, abstractmethod
from typing import Union, Dict, Any


class BaseRequestTypes(enum.Enum):
    pass


class BaseRequest(ABC):
    def __init__(self, params: Union[Dict[str, Any], None] = None) -> None:
        self.params = params

    @abstractmethod
    def get_request(self) -> str:
        raise NotImplemented


class BaseRequester(ABC):

    def __init__(self):
        self._request = None

    @staticmethod
    @abstractmethod
    def _get_requester(req_type: BaseRequestTypes,
                       params: Union[Dict[str, Any], None] = None) -> BaseRequest:
        raise NotImplemented

    def get_request_text(self, req_type: BaseRequestTypes,
                         params: Union[Dict[str, Any], None] = None) -> str:
        self._request = self._get_requester(req_type, params)
        return self._request.get_request()
