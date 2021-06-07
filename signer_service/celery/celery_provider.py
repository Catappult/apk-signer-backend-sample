from config_loader import configs
from signer_service.celery.celery_configurations import CelerySignerConfig
from signer_service.celery.celery_signer_manager import CelerySignerManager
from signer_service.celery.celery_signer_tasks_manager import CelerySignerTasksManager
from signer_service.celery.celery_wrapper import CeleryWrapper


class CeleryProvider:
    def __init__(self):
        self.__celery_wrapper = CeleryWrapper()
        self.__celery_signer_manager = CelerySignerManager(
            self.__celery_wrapper,
            CelerySignerTasksManager(
                configs["keystore"]["path"], configs["keystore"]["password"]
            ),
            CelerySignerConfig(),
        )

    def provide_celery_signer_manager(self) -> CelerySignerManager:
        return self.__celery_signer_manager


celery_provider = CeleryProvider()
