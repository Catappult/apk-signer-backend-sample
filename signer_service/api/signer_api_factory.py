from flask_restx import Api

from signer_service.api.signer_api import SignerEndpoint, signer_api
from signer_service.celery import CelerySignerManager
from signer_service.celery.tasks.signer.apk_signer_task import ApkSignerTask
from signer_service.signing.signing_service import SigningService


class SignerApiFactory:
    def __init__(
        self,
        apk_signer_task: ApkSignerTask,
        signing_service: SigningService,
        celery_signer_manager: CelerySignerManager,
        tmp_dir: str,
    ):
        self.__apk_signer_task = apk_signer_task
        self.__signing_service = signing_service
        self.__celery_signer_manager = celery_signer_manager
        self.__tmp_dir = tmp_dir

    def create_namespace(self, api: Api):
        api.add_namespace(signer_api, "/signer")
        signer_api.add_resource(
            SignerEndpoint,
            "/sign",
            methods=["POST", "GET"],
            resource_class_kwargs={
                "apk_signer_task": self.__apk_signer_task,
                "signing_service": self.__signing_service,
                "celery_signer_manager": self.__celery_signer_manager,
                "tmp_dir": self.__tmp_dir,
            },
        )
