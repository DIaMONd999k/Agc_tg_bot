import logging


class InfoOnlyFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, 'action'):
            if record.levelno == 20:
                return True


class SendMsgFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if hasattr(record, 'action'):
            if record.action == 'send_message':
                return True


class WarningFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, 'action'):
            if record.levelno >= 20:
                return True


class ErrorFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, 'action'):
            if record.levelno >= 40:
                return True
