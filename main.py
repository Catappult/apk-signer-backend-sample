import os.path

from celery import Task
from flask import Flask

from config_loader import configs
from signer_service.api.api_factory import ApiFactory, SwaggerApi
from signer_service.api.default_api_factory import DefaultApiFactory
from signer_service.api.signer_api_factory import SignerApiFactory
from signer_service.celery import celery_provider, CelerySignerManager
from signer_service.commons.logger.global_logger import GlobalLogger
from signer_service.commons.logger.log_levels import LogLevels
from signer_service.commons.logger.logger_provider import logger_provider
from signer_service.flask.flask_provider import flask_provider
from signer_service.signing.signing_provider import signing_provider
from signer_service.signing.signing_service import SigningService

logger: GlobalLogger = logger_provider.provide_global_logger()
if configs["api"]["debug"]:
    logger.set_level(LogLevels.DEBUG)
    logger.debug("main", "Running in DEBUG mode")

celery_signer_manager: CelerySignerManager = (
    celery_provider.provide_celery_signer_manager()
)
apk_signer_task: Task = celery_signer_manager.get_task("ApkSignerTask")
signing_service: SigningService = signing_provider.provide_signing_service(
    configs["keystore"]["path"], configs["keystore"]["password"]
)

api_factory: ApiFactory = ApiFactory(
    DefaultApiFactory(),
    SignerApiFactory(
        apk_signer_task,
        signing_service,
        celery_signer_manager,
        os.path.join("/tmp", "signer_service"),
    ),
)
api: SwaggerApi = api_factory.get_api()

flask_app: Flask = flask_provider.provide_flask_wrapper("signer").get_app()
api.init_app(flask_app)
