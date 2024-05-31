import asyncio
import os
import asyncpg

from utils import singleton
from dotenv import load_dotenv
from utils.validators import db_requests_validators
from db_utils.loodsman_db import loodsman_users, loodsman_requests
from db_utils import base_database, base_db, pg_db


class LoodBDException(Exception):
    def __init__(self, message, extra_info):
        super().__init__(message)
        self.extra_info = extra_info


@singleton.singleton
class LoodsmanDataBase(base_database.BaseDB):
    def __init__(self, database: base_db.BaseDataBase, time_interval: str = '1 minute'):
        requester = loodsman_requests.LoodsmanRequester()
        super().__init__(requester)
        self.database = database
        self._time_interval = self.validate_timeinterval(time_interval)

    @staticmethod
    def validate_timeinterval(time_interval: str) -> str:
        if db_requests_validators.validate_timeinterval_units(time_interval):
            __time, __time_unit = time_interval.split()
            return f'{str(int(__time)*2)} {__time_unit}'
        else:
            raise TypeError('Формат записи интервала проверки данных не соответствует требования PostreSQL')

    async def get_users_tasks(self) -> list[asyncpg.Record]:
        params = {'time_interval': self._time_interval}
        req_type = loodsman_requests.LoodsmanRequestTypes.get_users_tasks
        req_text = self._get_request_text(req_type, params)
        response = None
        try:
            response = await self.database.get_data(req_text)
        except:
            pass
        return response

    async def get_users(self) -> list[asyncpg.Record]:
        req_type = loodsman_requests.LoodsmanRequestTypes.get_users
        req_text = self._get_request_text(req_type)
        return await self.database.get_data(req_text)

    def set_time_interval(self, new_time_interval) -> None:
        self._time_interval = self.validate_timeinterval(new_time_interval)

    def get_time_interval(self) -> str:
        return self._time_interval
