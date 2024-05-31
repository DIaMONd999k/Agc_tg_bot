from abc import ABC, abstractmethod


class BaseDataBase(ABC):
    @abstractmethod
    async def get_data(self, request_text: str) -> list:
        raise NotImplemented

    @abstractmethod
    async def set_data(self, req_text: str) -> str:
        raise NotImplemented

    @abstractmethod
    async def update_data(self, req_text: str) -> str:
        raise NotImplemented
