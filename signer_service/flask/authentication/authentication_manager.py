import re
from typing import Optional

from werkzeug.datastructures import EnvironHeaders
from werkzeug.wrappers import BaseRequest
from yajwt.jwt_requests_validator import JwtRequestsValidator

from signer_service.commons.logger.base_logger import BaseLogger


class AuthenticationManager:
    def __init__(
        self, jwt_requests_validator: JwtRequestsValidator, logger: BaseLogger
    ):
        self.__jwt_requests_validator = jwt_requests_validator
        self.__logger = logger

    def validate(self, request: BaseRequest) -> bool:
        # request object is not iterable, can't use dict()
        self.__logger.debug(
            "AuthenticationManager",
            f"Received a new request to validate: '{request.__dict__}'",
        )
        if request.path != "/signer/sign":
            return True

        jwt_token = self.__get_jwt_token(request.headers)
        if jwt_token is None:
            self.__logger.warning("AuthenticationManager", "No JWT token found.")
            return False

        token = self.__jwt_requests_validator.validate(jwt_token)
        self.__logger.debug("AuthenticationManager", f"Validation result: '{token}'")
        return token.valid

    def __get_jwt_token(self, headers: EnvironHeaders) -> Optional[str]:
        token = headers.get("Authorization")
        if token is None:
            return None
        match = re.search(r"Bearer\s(.+)", token)
        return match.group(1) if match else None
