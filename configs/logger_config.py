import os
import sys

from configs import app_config
from utils.loggers import log_filters

log_db = app_config.db_for_tg_bot


def check_log_path(log_p: str) -> None:
    if not os.path.exists(log_p):
        try:
            os.makedirs(log_p)
        except PermissionError:
            raise


def get_log_path() -> str:
    log_p = ''
    if os.name == 'posix':
        log_p = '/var/log/agc_bot_logs/'
    elif os.name == 'nt':
        log_p = os.path.expanduser('~') + r'\\AppData\\Local\\Temp\\agc_bot_logs\\'
    check_log_path(log_p)
    return log_p


log_path = get_log_path()

info_format = '[{levelname}] {asctime}: {msg}'
warning_format = ('[{levelname}] - {asctime}: package name: {name}\n'
                  'filename: {filename}, funcname: {funcName}, lineNo:{lineno}\n'
                  'message: {msg}')

logger_conf = {
    'version': 1,
    'disable_existing_loggers': False,
    'datefmt': '%m/%d/%Y %I:%M:%S %p %Z',
    'formatters': {
        'info_formatter': {
            'format': info_format,
            'style': '{'
        },
        'warning_formatter': {
            'format': warning_format,
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'level': 'DEBUG',
            'formatter': 'info_formatter'
        },
        'dbFH_warn': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_path + 'db.log',
            'maxBytes': 1024 ** 2,
            'backupCount': 5,
            'level': 'WARNING',
            'formatter': 'warning_formatter',
        },
        'dbFH_info': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_path + 'db.log',
            'maxBytes': 1024 ** 2,
            'backupCount': 5,
            'level': 'INFO',
            'formatter': 'info_formatter',
            'filters': ['info_only_filter']
        },
        'botFH_warn': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_path + 'bot.log',
            'maxBytes': 1024 ** 2,
            'backupCount': 5,
            'level': 'WARNING',
            'formatter': 'warning_formatter',
        },
        'botFH_info': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_path + 'bot.log',
            'maxBytes': 1024 ** 2,
            'backupCount': 5,
            'level': 'INFO',
            'formatter': 'info_formatter',
            'filters': ['info_only_filter']
        },
        'taskDispFH_warn': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_path + 'task_dispatcher.log',
            'maxBytes': 1024 ** 2,
            'backupCount': 5,
            'level': 'WARNING',
            'formatter': 'warning_formatter'
        },
        'taskDispFH_info': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_path + 'task_dispatcher.log',
            'maxBytes': 1024 ** 2,
            'backupCount': 5,
            'level': 'INFO',
            'formatter': 'info_formatter',
            'filters': ['info_only_filter']
        },
        'taskDispDBH': {
            '()': 'utils.loggers.log_handlers.DbLogHandler',
            'level': 'INFO',
            'db': log_db,
            'filters': ['send_msg_filter']

        }
    },
    'filters': {
        'info_only_filter': {
            '()': log_filters.InfoOnlyFilter
        },
        'warning_filter': {
            '()': log_filters.WarningFilter
        },
        'error_filter': {
            '()': log_filters.ErrorFilter
        },
        'send_msg_filter': {
            '()': log_filters.SendMsgFilter
        },
    },
    'loggers': {
        'task_dispatcher_logger': {
            'level': 'DEBUG',
            'handlers': ['console', 'taskDispDBH', 'taskDispFH_warn', 'taskDispFH_info']
        },
        'db_logger': {
            'level': 'DEBUG',
            'handlers': ['console', 'dbFH_warn', 'dbFH_info']
        },
        'tg_bot_logger': {
            'level': 'DEBUG',
            'handlers': ['console', 'botFH_warn', 'botFH_info']
        }
    }
}
