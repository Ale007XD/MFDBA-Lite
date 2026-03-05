import json
import os


DEFAULT_CONFIG_PATH = "config/config.default.json"


def load_config(path: str | None = None):

    config_path = path or DEFAULT_CONFIG_PATH

    if not os.path.exists(config_path):
        return {}

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)
