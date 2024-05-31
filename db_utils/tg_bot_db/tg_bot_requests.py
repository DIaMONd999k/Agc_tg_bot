from typing import Union, Dict, Any
from db_utils import db_requests


class TgBotRequestTypes(db_requests.BaseRequestTypes):
    get_users = 'get_users'


class RequestTgUsers(db_requests.BaseRequest):
    def get_request(self) -> str:
        return f"select * from bot_data.get_tg_users();"


class TgRequester(db_requests.BaseRequester):
    def __init__(self):
        super().__init__()

    @staticmethod
    def _get_requester(req_type: TgBotRequestTypes,
                       params: Union[Dict[str, Any], None] = None) -> db_requests.BaseRequest:
        match req_type:
            case TgBotRequestTypes.get_users:
                return RequestTgUsers()
