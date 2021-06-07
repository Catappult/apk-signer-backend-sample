import pickle

import celery

from signer_service.signing.signing_service import SigningService


class ApkSignerTask(celery.Task):
    def __init__(self, signing_service: SigningService):
        self.__signing_service = signing_service

    def run(self, apk_path: str) -> bytes:
        return pickle.dumps(self.__signing_service.sign_apk(apk_path))
