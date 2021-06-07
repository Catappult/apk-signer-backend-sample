import pickle
from typing import Any

import celery
from flask import Flask

from signer_service.celery.celery_configurations import CelerySignerConfig
from signer_service.celery.celery_signer_tasks_manager import CelerySignerTasksManager
from signer_service.celery.celery_wrapper import CeleryWrapper
from signer_service.commons.operation_result import OperationResult


class CelerySignerManager:
    def __init__(
        self,
        celery_wrapper: CeleryWrapper,
        celery_signer_tasks_manager: CelerySignerTasksManager,
        celery_signer_config: CelerySignerConfig,
    ):
        self.__celery_wrapper = celery_wrapper
        self.__celery_signer_tasks_manager = celery_signer_tasks_manager
        self.__celery_signer_config = celery_signer_config
        self.__celery_signer: celery.Celery = None

    def get_instance(self) -> celery.Celery:
        if not self.__celery_signer:
            celery_signer = self.__create_celery()
            self.__celery_signer_tasks_manager.register_tasks(celery_signer)
            self.__celery_signer = celery_signer
        return self.__celery_signer

    def __create_celery(self) -> celery.Celery:
        flask_app = Flask(self.__celery_signer_config.name)
        flask_app.config.update(
            CELERY_BROKER_URL=self.__celery_signer_config.broker_url,
            CELERY_RESULT_BACKEND=self.__celery_signer_config.result_backend,
        )
        return self.__celery_wrapper.build(flask_app, self.__celery_signer_config)

    def get_task(self, task_name: str) -> celery.Task:
        if not self.__celery_signer:
            self.get_instance()
        return self.__celery_signer_tasks_manager.get_task(task_name)

    def get_job_status(self, job_id: str) -> Any:
        job = self.__celery_signer_tasks_manager.get_job(job_id)
        return job.status

    def get_job_result(self, job_id: str) -> OperationResult:
        job = self.__celery_signer_tasks_manager.get_job(job_id)
        return pickle.loads(job.result)
