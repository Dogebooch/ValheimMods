
from __future__ import annotations
import json
from typing import Iterable
from ..models import MaterialMetric
from .base import Parser
class EpicLootJson(Parser):
    source_type = "epicloot_json"
    exts = (".json",)
    def parse(self, path: str, materials: set[str], aliases: dict[str, str]) -> Iterable[MaterialMetric]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return []
        out = []
        def walk(obj):
            if isinstance(obj, dict):
                for k, v in list(obj.items()):
                    mat = aliases.get(k, k)
                    if mat in materials and _is_number(v):
                        out.append(MaterialMetric(material=mat, source=self.source_type, file_path=path, weight=float(v)))
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for it in obj:
                    walk(it)
        walk(data); return out
def _is_number(x):
    try: float(x); return True
    except: return False
