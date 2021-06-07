from typing import List

import celery
from celery.result import AsyncResult

from signer_service.celery.tasks.signer.apk_signer_task import ApkSignerTask
from signer_service.commons.logger.global_logger import GlobalLogger
from signer_service.commons.logger.logger_provider import logger_provider
from signer_service.signing.signing_provider import signing_provider
from signer_service.signing.signing_service import SigningService


class CelerySignerTasksManager:
    def __init__(self, keystore_path: str, keystore_password: str):
        self.__tasks = []
        self.__celery_app: celery.Celery = None

        self.__signing_service: SigningService = (
            signing_provider.provide_signing_service(keystore_path, keystore_password)
        )
        self.__logger: GlobalLogger = logger_provider.provide_global_logger()

    def register_tasks(self, celery_app: celery.Celery):
        if not self.__celery_app:
            self.__celery_app = celery_app

        if not self.__tasks:
            self.__tasks = self.__get_celery_signer_tasks()

    def __get_celery_signer_tasks(self) -> List[celery.Task]:
        return [self.__get_apk_signer_task()]

    def __get_apk_signer_task(self) -> celery.Task:
        if self.already_registered("ApkSignerTask"):
            return self.get_task("ApkSignerTask")

        apk_signer_task = ApkSignerTask(self.__signing_service)
        return self.__celery_app.register_task(apk_signer_task)

    def already_registered(self, task_name: str) -> bool:
        try:
            return bool(self.get_task(task_name))
        except ModuleNotFoundError:
            return False

    def get_task(self, task_name: str) -> celery.Task:
        for task in self.__tasks:
            if str(task.name).endswith(task_name):
                return task
        raise ModuleNotFoundError(f"Couldn't find '{task_name}'")

    def get_job(self, job_id: str) -> AsyncResult:
        return self.__tasks[0].AsyncResult(job_id)
