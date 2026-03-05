import json
import shutil
from pathlib import Path


HOME_DIR = Path.home() / ".mfdballm"
HOME_CONFIG = HOME_DIR / "config.json"

PROJECT_DEFAULT = (
    Path(__file__).resolve().parents[1]
    / "config"
    / "config.default.json"
)


def ensure_config():
    """
    Ensure runtime config exists in ~/.mfdballm/config.json
    """
    HOME_DIR.mkdir(parents=True, exist_ok=True)

    if not HOME_CONFIG.exists():
        shutil.copy(PROJECT_DEFAULT, HOME_CONFIG)

    return HOME_CONFIG


def load_config():
    """
    Load config.json from runtime directory
    """
    config_path = ensure_config()

    with open(config_path, "r") as f:
        return json.load(f)
