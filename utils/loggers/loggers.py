import logging
import logging.config as log_conf
from configs import logger_config

log_conf.dictConfig(logger_config.logger_conf)

td_logger = logging.getLogger('task_dispatcher_logger')
db_logger = logging.getLogger('db_logger')
tg_bot_logger = logging.getLogger('tg_bot_logger')

