from abc import ABC, abstractmethod
from typing import Dict, Any

from signer_service.commons.logger.log_levels import LogLevels


class BaseLogger(ABC):
    @abstractmethod
    def set_level(self, level: LogLevels):
        pass

    @abstractmethod
    def error(self, tag: str, exception: Exception, extra: Dict[str, Any] = None):
        pass

    @abstractmethod
    def warning(self, tag: str, message: str, extra: Dict[str, Any] = None):
        pass

    @abstractmethod
    def info(self, tag: str, message: str, extra: Dict[str, Any] = None):
        pass

    @abstractmethod
    def debug(self, tag: str, message: str, extra: Dict[str, Any] = None):
        pass
