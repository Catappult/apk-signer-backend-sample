from signer_service.commons.operation_result import OperationResult, OperationStatus
from signer_service.signing.apksigner.apksigner_service import (
    ApkSignerService,
    ApkSignerException,
)


class SigningService:
    def __init__(self, apksigner_service: ApkSignerService):
        self.__apksigner_service = apksigner_service

    def sign_apk(self, apk_path: str) -> OperationResult:
        try:
            signed_path = self.__apksigner_service.sign(apk_path)
            return OperationResult(status=OperationStatus.SUCCESS, data=signed_path)
        except ApkSignerException as e:
            return OperationResult(status=OperationStatus.ERROR, error_details=e)
