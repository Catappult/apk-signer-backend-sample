import logging
from typing import Dict, Any

import colorlog

from signer_service.commons.logger.base_logger import BaseLogger
from signer_service.commons.logger.log_levels import LogLevels


class OutputLogger(BaseLogger):
    def __init__(self, level: LogLevels = LogLevels.INFO):
        self.__level = level
        self.__logger = self.__make_logger()
        self.set_level(level)

    def __make_logger(self) -> logging.Logger:
        log_format = (
            "%(asctime)s %(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s"
        )
        date_format = "%Y-%m-%d %H:%M:%S"
        handler = colorlog.StreamHandler()
        formatter = colorlog.ColoredFormatter(log_format, datefmt=date_format)
        handler.setFormatter(formatter)

        logger = colorlog.getLogger()
        logger.handlers = []
        logger.addHandler(handler)
        logger.setLevel(self.__level)
        return logger

    def set_level(self, level: LogLevels):
        self.__level = level
        self.__logger.setLevel(level.value)

    def error(self, tag: str, exception: Exception, extra: Dict[str, Any] = None):
        log_message = self.__parse_message(str(exception), extra)
        self.__logger.error(f"{tag}: {log_message}")

    def warning(self, tag: str, message: str, extra: Dict[str, Any] = None):
        log_message = self.__parse_message(message, extra)
        self.__logger.warning(f"{tag}: {log_message}")

    def info(self, tag: str, message: str, extra: Dict[str, Any] = None):
        log_message = self.__parse_message(message, extra)
        self.__logger.info(f"{tag}: {log_message}")

    def debug(self, tag: str, message: str, extra: Dict[str, Any] = None):
        log_message = self.__parse_message(message, extra)
        self.__logger.debug(f"{tag}: {log_message}")

    @staticmethod
    def __parse_message(message: str, extra: Dict[str, Any] = None):
        return f"{message} [EXTRA: {extra}]" if extra is not None else message
