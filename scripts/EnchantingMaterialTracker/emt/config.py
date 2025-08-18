
from __future__ import annotations
import json, os, logging
log = logging.getLogger(__name__)
DEFAULT_SETTINGS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "settings.json")
EXAMPLE_SETTINGS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "settings.example.json")
def load_settings(path: str | None = None) -> dict:
    path = path or DEFAULT_SETTINGS_FILE
    if not os.path.exists(path):
        log.warning("settings.json not found; using settings.example.json")
        path = EXAMPLE_SETTINGS_FILE
        if not os.path.exists(path):
            raise FileNotFoundError(f"Neither settings.json nor settings.example.json found in {os.path.dirname(DEFAULT_SETTINGS_FILE)}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "db_path" in data and not os.path.isabs(data["db_path"]):
        data["db_path"] = os.path.abspath(data["db_path"])
    return data
def load_materials_registry(path: str) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Materials registry file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
def resolve_alias(material: str, aliases: dict[str, str]) -> str:
    return aliases.get(material, material)
