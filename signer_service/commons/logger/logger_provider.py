from signer_service.commons.logger.global_logger import GlobalLogger
from signer_service.commons.logger.output_logger import OutputLogger


class LoggerProvider:
    def __init__(self):
        self.__output_logger = OutputLogger()

    def provide_global_logger(self) -> GlobalLogger:
        return GlobalLogger([self.__output_logger])


logger_provider = LoggerProvider()
