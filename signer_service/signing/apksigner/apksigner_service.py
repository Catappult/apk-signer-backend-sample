import os
import subprocess

from signer_service.commons.file_utils import FileUtils
from signer_service.commons.logger.base_logger import BaseLogger


class ApkSignerException(Exception):
    pass


class ApkSignerService:
    APKSIGNER = "apksigner"
    SIGNED_EXTENSION = "-signed"

    def __init__(
        self,
        keystore_path: str,
        keystore_password: str,
        logger: BaseLogger,
    ):
        self.__keystore_path = keystore_path
        self.__keystore_password = keystore_password
        self.__logger = logger

    def sign(self, apk_path: str) -> str:
        filename = FileUtils.get_stem_from_path(apk_path)
        signed_filename = filename + self.SIGNED_EXTENSION + ".apk"
        signed_path = os.path.join(FileUtils.get_parent(apk_path), signed_filename)
        FileUtils.silently_remove(signed_path)

        try:
            subprocess.check_output(
                [
                    self.APKSIGNER,
                    "sign",
                    "--ks",
                    self.__keystore_path,
                    "--ks-pass",
                    "pass:" + self.__keystore_password,
                    "--out",
                    signed_path,
                    apk_path,
                ]
            )

            self.__logger.info("ApkSignerService", f"Signed APK'{signed_path}'")
            return signed_path
        except subprocess.CalledProcessError as e:
            self.__logger.error(
                "ApkSignerService",
                Exception("Failed to sign APK"),
                extra={"apk_path": apk_path, "msg": e},
            )
            raise ApkSignerException(e)
        finally:
            FileUtils.silently_remove(apk_path)
