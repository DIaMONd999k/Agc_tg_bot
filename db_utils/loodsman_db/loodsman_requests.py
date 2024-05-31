from typing import Union, Dict, Any
from db_utils import db_requests


class LoodsmanRequestTypes(db_requests.BaseRequestTypes):
    get_users_tasks = 'get_users_tasks'
    get_users = 'get_users'


class RequestUsersTasks(db_requests.BaseRequest):
    def get_request(self) -> str:
        time_interval = self.params['time_interval']
        if time_interval is not None:
            return f"select * from ora_dbo.tg_get_tasks(interval '{time_interval}');"
        else:
            raise Exception


class RequestUsers(db_requests.BaseRequest):
    def get_request(self) -> str:
        return f"select * from ora_dbo.tg_get_users();"


class LoodsmanRequester(db_requests.BaseRequester):
    def __init__(self):
        super().__init__()

    @staticmethod
    def _get_requester(req_type: LoodsmanRequestTypes,
                       params: Union[Dict[str, Any], None] = None) -> db_requests.BaseRequest:
        match req_type:
            case LoodsmanRequestTypes.get_users_tasks:
                return RequestUsersTasks(params)
            case LoodsmanRequestTypes.get_users:
                return RequestUsers()
