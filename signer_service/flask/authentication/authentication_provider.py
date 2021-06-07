from yajwt.jwt_requests_validator import JwtRequestsValidator

from signer_service.commons.logger.global_logger import GlobalLogger
from signer_service.flask.authentication.authentication_manager import (
    AuthenticationManager,
)
from signer_service.commons.logger.logger_provider import logger_provider
from signer_service.flask.authentication.jwt.jwt_provider import jwt_provider


class AuthenticationProvider:
    def __init__(self):
        self.__jwt_requests_validator: JwtRequestsValidator = (
            jwt_provider.provide_jwt_requests_validator()
        )
        self.__logger: GlobalLogger = logger_provider.provide_global_logger()

    def provide_authentication_manager(self) -> AuthenticationManager:
        return AuthenticationManager(self.__jwt_requests_validator, self.__logger)


authentication_provider = AuthenticationProvider()
