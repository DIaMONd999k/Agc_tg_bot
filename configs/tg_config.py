import os
from dotenv import load_dotenv
from utils.validators import db_requests_validators

load_dotenv()
token = os.getenv("TG_BOT_TOKEN")
admin_id = os.getenv('ADMIN_ID')
lic_man_host = os.getenv('LIC_MAN_HOST')


time_interval = '1 minute'
if not db_requests_validators.validate_timeinterval_units(time_interval):
    raise TypeError('Формат записи интервала проверки данных не соответствует требования PostreSQL')
