from signer_service.commons.logger.global_logger import GlobalLogger
from signer_service.commons.logger.logger_provider import logger_provider
from signer_service.signing.apksigner.apksigner_service import ApkSignerService
from signer_service.signing.signing_service import SigningService


class SigningProvider:
    def __init__(self):
        self.__logger: GlobalLogger = logger_provider.provide_global_logger()

    def provide_signing_service(
        self, keystore_path: str, keystore_password: str
    ) -> SigningService:
        return SigningService(
            ApkSignerService(keystore_path, keystore_password, self.__logger)
        )


signing_provider = SigningProvider()
