from celery import Celery

from signer_service.celery.celery_provider import celery_provider
from signer_service.celery.celery_signer_manager import CelerySignerManager

celery_signer_manager: CelerySignerManager = (
    celery_provider.provide_celery_signer_manager()
)
celery_signer: Celery = celery_signer_manager.get_instance()
