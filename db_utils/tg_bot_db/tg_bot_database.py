import asyncio

from utils import singleton
from dotenv import load_dotenv
from db_utils.tg_bot_db import tg_users, tg_bot_requests
from db_utils import base_database, pg_db, base_db
from configs import tg_bot_db_config


@singleton.singleton
class TgBotDB(base_database.BaseDB):
    def __init__(self, database: base_db.BaseDataBase):
        self.database = database
        requester = tg_bot_requests.TgRequester()
        super().__init__(requester=requester)

    async def get_tg_users(self) -> list:
        req_type = tg_bot_requests.TgBotRequestTypes.get_users
        req_text = self._get_request_text(req_type)
        return await self.database.get_data(req_text)

