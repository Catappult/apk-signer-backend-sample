from yajwt.entities.jwt_key import JwtKey, JwtKeyType
from yajwt.jwt_requests_validator import JwtRequestsValidator
from yajwt.jwt_requests_wrapper import JwtRequestsWrapper
from yajwt.jwt_response_mapper import JwtResponseMapper
from yajwt.keys_manager.jwt_keys_manager import JwtKeysManager
from yajwt.keys_manager.jwt_keys_memory_manager import JwtKeysMemoryManager

from config_loader import configs


class JwtProvider:
    def __init__(self):
        self.__token_ttl = 60 * 60  # 1h

    def provide_jwt_requests_wrapper(self) -> JwtRequestsWrapper:
        jwt_keys_manager = self.provide_jwt_keys_manager()
        return JwtRequestsWrapper(
            jwt_keys_manager, JwtResponseMapper(), self.__token_ttl
        )

    def provide_jwt_keys_manager(self) -> JwtKeysManager:
        return JwtKeysMemoryManager(self.__get_keys())

    def __get_keys(self) -> dict:
        key_details = configs["api"]["jwt"]
        return {
            key_details["iss"]: JwtKey(
                team=key_details["iss"],
                key=key_details["public_key"],
                payload={},
                algorithm=key_details["algorithm"],
                key_type=JwtKeyType.PUBLIC_KEY,
            )
        }

    def provide_jwt_requests_validator(self) -> JwtRequestsValidator:
        return JwtRequestsValidator(self.provide_jwt_keys_manager())


jwt_provider = JwtProvider()
