import asyncio
import logging
import nest_asyncio

from db_utils import base_db


class DbLogHandler(logging.Handler):
    def __init__(self, db: base_db.BaseDataBase) -> None:
        super().__init__()
        self.db = db

    def emit(self, record: logging.LogRecord) -> None:
        try:
            nest_asyncio.apply()
            event_loop = asyncio.get_running_loop()
            task = event_loop.create_task(self.db.set_data(record.msg))
            event_loop.run_until_complete(task)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
