import asyncio
import os

from configs import tg_bot_db_config, lood_db_config, tg_config
from db_utils import pg_db
from db_utils.loodsman_db import loodsman_database
from db_utils.tg_bot_db import tg_users, tg_bot_database

# конфиги для подключения к БД
tg_db_conf = tg_bot_db_config.tg_bot_db_config
lood_db_conf = lood_db_config.loodsman_db_config
polling_timeout = tg_config.time_interval

# выбираем с каким типом БД будет работать бот и с которым работает лоцман
db_for_tg_bot = pg_db.PgDataBase(tg_db_conf)
db_for_lood = pg_db.PgDataBase(lood_db_conf)

# создаем объекты, котрые будут общаться с БД
tg_db = tg_bot_database.TgBotDB(db_for_tg_bot)
lood_db = loodsman_database.LoodsmanDataBase(
    db_for_lood,
    time_interval=polling_timeout
)

# грузим пользователей приложения
event_loop = asyncio.get_event_loop()
tg_bot_users = tg_users.TgBotUsers()
task = event_loop.create_task(tg_db.get_tg_users())
request = event_loop.run_until_complete(task)
tg_bot_users.add_users(request)

admin_chat_id = os.getenv('ADMIN_ID')
