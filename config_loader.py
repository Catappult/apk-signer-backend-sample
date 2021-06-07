import json
import os
from typing import Dict, Any


class ConfigLoader:
    def __init__(self, config_file_path: str):
        self.__config_file_path = config_file_path

    def get_parsed_config(self) -> Dict[str, Any]:
        try:
            with open(self.__config_file_path, "r", encoding="UTF-8") as file:
                return json.load(file)
        except (UnicodeDecodeError, FileNotFoundError):
            return {}


config_loader = ConfigLoader(os.path.join(os.path.dirname(__file__), "config.json"))
configs = config_loader.get_parsed_config()
