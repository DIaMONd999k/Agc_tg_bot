import os
from dotenv import load_dotenv


load_dotenv()
loodsman_db_config = {
    'pg_user': os.getenv('LOODSMAN_USER'),
    'pg_password': os.getenv('LOODSMAN_PASS'),
    'pg_database': os.getenv('LOODSMAN_DB'),
    'pg_host': os.getenv('LOODSMAN_DB_HOST'),
    'pg_port': os.getenv('LOODSMAN_DB_PORT')

}
