import asyncio
from typing import Dict, Union, Any

import asyncpg

from asyncpg import Pool, Connection
from db_utils import base_db


class PgDataBase(base_db.BaseDataBase):
    def __init__(self, db_config: Dict, use_pool: bool = False):
        self.pg_user = db_config['pg_user']
        self.pg_password = db_config['pg_password']
        self.pg_database = db_config['pg_database']
        self.pg_host = db_config['pg_host']
        self.pg_port = db_config['pg_port']
        self.use_pool = use_pool

        self.dsn = f'postgres://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_database}'
        self._pool: Pool = self._create_pool() if self.use_pool else None

    def _create_pool(self) -> Pool:
        return asyncio.get_event_loop().run_until_complete(asyncpg.create_pool(dsn=self.dsn))

    async def _create_connection(self) -> Connection:
        return await asyncpg.connect(host=self.pg_host,
                                     port=self.pg_port,
                                     user=self.pg_user,
                                     password=self.pg_password,
                                     database=self.pg_database)

    async def _get_connection(self):
        if self.use_pool:
            return await self._pool.acquire()
        else:
            return await self._create_connection()

    @staticmethod
    async def _get_recordset(connection: Connection, request_text: str) -> list:
        try:
            response = await connection.fetch(f"{request_text}")
        finally:
            await connection.close()
        return response

    async def get_data(self, request_text: str) -> list:
        connection = await self._get_connection()
        return await self._get_recordset(connection, request_text)

    async def set_data(self, request_text: str) -> None:
        connection = await self._get_connection()
        await self._get_recordset(connection, request_text)

    async def update_data(self, req_text: str) -> None:
        raise NotImplemented
