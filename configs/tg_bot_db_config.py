import os
from dotenv import load_dotenv


load_dotenv()
tg_bot_db_config = {
    'pg_user': os.getenv('TG_USER'),
    'pg_password': os.getenv('TG_PASS'),
    'pg_database': os.getenv('TG_DB'),
    'pg_host': os.getenv('TG_DB_HOST'),
    'pg_port': os.getenv('TG_DB_PORT')

}


