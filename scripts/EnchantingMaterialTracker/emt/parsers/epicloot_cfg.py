
from __future__ import annotations
import re
from typing import Iterable
from ..models import MaterialMetric
from .base import Parser
class EpicLootChestCfg(Parser):
    source_type = "epicloot_chest_cfg"
    exts = (".cfg",)
    def parse(self, path: str, materials: set[str], aliases: dict[str, str]) -> Iterable[MaterialMetric]:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        section_re = re.compile(r"^\s*\[([^\]]+)\]\s*$", re.MULTILINE)
        positions = [(m.start(), m.group(1)) for m in section_re.finditer(text)]
        positions.append((len(text), None))
        out = []
        for i in range(len(positions)-1):
            start, name = positions[i]
            end, _ = positions[i+1]
            body = text[start:end]
            for block in re.split(r"\n\s*\n", body):
                item_match = re.search(r"^\s*(Item|Prefab|Name)\s*=\s*(?P<item>\S+)", block, flags=re.MULTILINE | re.IGNORECASE)
                if not item_match:
                    continue
                item = item_match.group("item").strip()
                item = aliases.get(item, item)
                if item not in materials:
                    continue
                weight = _first_float(block, r"SetTemplateWeight\s*=\s*([0-9.]+)")
                a_min = _first_float(block, r"(SetAmountMin|AmountMin)\s*=\s*([0-9.]+)")
                a_max = _first_float(block, r"(SetAmountMax|AmountMax)\s*=\s*([0-9.]+)")
                out.append(MaterialMetric(material=item, source=self.source_type, file_path=path,
                                          weight=weight or 0.0, amount_min=a_min or 0.0, amount_max=a_max or 0.0))
        return out
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
