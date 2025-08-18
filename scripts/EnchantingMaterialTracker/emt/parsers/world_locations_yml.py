
from __future__ import annotations
from typing import Iterable
from ..models import MaterialMetric
from .base import Parser
class WorldLocationsYml(Parser):
    source_type = "world_locations_yml"
    exts = (".yml", ".yaml")
    def parse(self, path: str, materials: set[str], aliases: dict[str, str]) -> Iterable[MaterialMetric]:
        try:
            import yaml  # type: ignore
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                data = yaml.safe_load(f) or {}
            return self._parse_structured(data, path, materials, aliases)
        except Exception:
            out = []
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            def get_val(line, key):
                if ":" in line:
                    k, v = line.split(":", 1)
                    if k.strip().lower() == key:
                        return v.strip()
                return None
            cur_item = None
            cur_weight = None
            stack_min = stack_max = None
            for ln in lines:
                v = get_val(ln, "prefab") or get_val(ln, "item") or get_val(ln, "name")
                if v:
                    if cur_item and cur_item in materials:
                        out.append(MaterialMetric(material=aliases.get(cur_item, cur_item),
                                                  source=self.source_type, file_path=path,
                                                  weight=float(cur_weight or 0.0),
                                                  stack_min=float(stack_min or 0.0),
                                                  stack_max=float(stack_max or 0.0)))
                    cur_item = v.strip().strip("'\"")
                    cur_weight = stack_min = stack_max = None
                    continue
                w = get_val(ln, "weight")
                if w: cur_weight = _to_float(w)
                smin = get_val(ln, "stackMin")
                if smin: stack_min = _to_float(smin)
                smax = get_val(ln, "stackMax")
                if smax: stack_max = _to_float(smax)
            if cur_item and cur_item in materials:
                out.append(MaterialMetric(material=aliases.get(cur_item, cur_item),
                                          source=self.source_type, file_path=path,
                                          weight=float(cur_weight or 0.0),
                                          stack_min=float(stack_min or 0.0),
                                          stack_max=float(stack_max or 0.0)))
            return out
    def _parse_structured(self, data, path, materials: set[str], aliases: dict[str, str]):
        out = []
        def walk(obj):
            if isinstance(obj, dict):
                if ("prefab" in obj or "item" in obj or "name" in obj) and any(k in obj for k in ("weight","stackMin","stackMax")):
                    item = obj.get("prefab") or obj.get("item") or obj.get("name")
                    item = aliases.get(item, item)
                    if item in materials:
                        out.append(MaterialMetric(material=item, source=self.source_type, file_path=path,
                                                  weight=float(obj.get("weight", 0.0) or 0.0),
                                                  stack_min=float(obj.get("stackMin", 0.0) or 0.0),
                                                  stack_max=float(obj.get("stackMax", 0.0) or 0.0)))
                else:
                    for v in obj.values():
                        walk(v)
            elif isinstance(obj, list):
                for it in obj:
                    walk(it)
        walk(data)
        return out
def _to_float(v):
    try: return float(str(v).strip())
    except: return 0.0
