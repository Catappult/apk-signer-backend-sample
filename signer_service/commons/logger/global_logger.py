from typing import Dict, Any, List

from signer_service.commons.logger.base_logger import BaseLogger
from signer_service.commons.logger.log_levels import LogLevels


class GlobalLogger(BaseLogger):
    def __init__(self, loggers: List[BaseLogger]):
        self.__loggers = loggers

    def set_level(self, level: LogLevels):
        for logger in self.__loggers:
            logger.set_level(level)

    def error(self, tag: str, exception: Exception, extra: Dict[str, Any] = None):
        for logger in self.__loggers:
            logger.error(tag, exception, extra)

    def warning(self, tag: str, message: str, extra: Dict[str, Any] = None):
        for logger in self.__loggers:
            logger.warning(tag, message, extra)

    def info(self, tag: str, message: str, extra: Dict[str, Any] = None):
        for logger in self.__loggers:
            logger.info(tag, message, extra)

    def debug(self, tag: str, message: str, extra: Dict[str, Any] = None):
        for logger in self.__loggers:
            logger.debug(tag, message, extra)
