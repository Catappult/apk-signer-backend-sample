import os
from pathlib import Path


class FileUtils:
    @staticmethod
    def get_filename_from_path(path: str) -> str:
        return Path(path).name

    @staticmethod
    def get_stem_from_path(path: str) -> str:
        return Path(path).stem

    @staticmethod
    def get_parent(path: str) -> Path:
        return Path(path).parent

    @staticmethod
    def silently_remove(path: str):
        try:
            os.remove(path)
        except (os.error, TypeError):
            pass
