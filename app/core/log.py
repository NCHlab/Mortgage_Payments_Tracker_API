import logging
import sys
from datetime import datetime

from pythonjsonlogger import jsonlogger

logger = logging.getLogger(__name__)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname
        if not log_record.get("timestamp"):
            now = datetime.now().isoformat()
            log_record["timestamp"] = now


def setup_logger(logger, log_level: int) -> None:
    formatter = CustomJsonFormatter(
        "(timestamp) (level) (name) (message) (pathname) (funcName) (lineno)"
    )
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    ch.setLevel(log_level)
    logger.addHandler(ch)
    logger.setLevel(log_level)


def convert_log_setting(setting: str) -> int:

    if setting is None:
        return logging.INFO

    setting = setting.upper()

    if setting == "DEBUG":
        return logging.DEBUG
    elif setting == "INFO":
        return logging.INFO
    elif setting == "WARNING":
        return logging.WARNING
    elif setting == "ERROR":
        return logging.ERROR
    elif setting == "CRITICAL":
        return logging.CRITICAL
    else:
        msg = "Couldn't detect log level. Converting to default value"
        logger.info(msg)
        return logging.INFO
