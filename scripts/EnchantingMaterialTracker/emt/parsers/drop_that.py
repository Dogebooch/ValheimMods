
from __future__ import annotations
import re
from typing import Iterable
from ..models import MaterialMetric
from .base import Parser
class DropThatListCfg(Parser):
    source_type = "drop_that_list_cfg"
    exts = (".cfg",)
    def parse(self, path: str, materials: set[str], aliases: dict[str, str]) -> Iterable[MaterialMetric]:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        out = []
        for block in re.split(r"\n\s*\n", text):
            item = _first_str(block, r"^\s*(Item|Prefab|Name)\s*=\s*([A-Za-z0-9_]+)")
            if not item: continue
            item = aliases.get(item, item)
            if item not in materials: continue
            chance = _first_float(block, r"(DropChance|Chance)\s*=\s*([0-9.]+)")
            weight = _first_float(block, r"(Weight|SetTemplateWeight)\s*=\s*([0-9.]+)")
            a_min = _first_float(block, r"(AmountMin|SetAmountMin)\s*=\s*([0-9.]+)")
            a_max = _first_float(block, r"(AmountMax|SetAmountMax)\s*=\s*([0-9.]+)")
            out.append(MaterialMetric(material=item, source=self.source_type, file_path=path,
                                      chance=chance or 0.0, weight=weight or 0.0,
                                      amount_min=a_min or 0.0, amount_max=a_max or 0.0))
        return out
class DropThatCharCfg(Parser):
    source_type = "drop_that_char_cfg"
    exts = (".cfg",)
    def parse(self, path: str, materials: set[str], aliases: dict[str, str]) -> Iterable[MaterialMetric]:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        out = []
        for block in re.split(r"\n\s*\n", text):
            item = _first_str(block, r"^\s*(Item|Prefab|Name)\s*=\s*([A-Za-z0-9_]+)")
            if not item: continue
            item = aliases.get(item, item)
            if item not in materials: continue
            chance = _first_float(block, r"(DropChance|Chance)\s*=\s*([0-9.]+)")
            weight = _first_float(block, r"(Weight|SetTemplateWeight)\s*=\s*([0-9.]+)")
            a_min = _first_float(block, r"(AmountMin|SetAmountMin)\s*=\s*([0-9.]+)")
            a_max = _first_float(block, r"(AmountMax|SetAmountMax)\s*=\s*([0-9.]+)")
            out.append(MaterialMetric(material=item, source=self.source_type, file_path=path,
                                      chance=chance or 0.0, weight=weight or 0.0,
                                      amount_min=a_min or 0.0, amount_max=a_max or 0.0))
        return out
def _first_str(s: str, pat: str):
    m = re.search(pat, s, flags=re.IGNORECASE | re.MULTILINE)
    return (m.group(2).strip() if m else None)
def _first_float(s: str, pat: str):
    m = re.search(pat, s, flags=re.IGNORECASE)
    if not m: return None
    try: 
        # Handle patterns with optional groups
        if m.groups() and m.group(1) is not None:
            return float(m.group(1))
        elif m.groups() and m.group(2) is not None:
            return float(m.group(2))
        return None
    except: return None
