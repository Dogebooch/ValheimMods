
from __future__ import annotations
import re
from typing import Iterable
from ..models import MaterialMetric
from .base import Parser
class BackpacksCfg(Parser):
    source_type = "backpack_cfg"
    exts = (".cfg", ".yml", ".yaml")
    def parse(self, path: str, materials: set[str], aliases: dict[str, str]) -> Iterable[MaterialMetric]:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        out = []
        for m in re.finditer(r"(ValidItems|AllowedItems)\s*=\s*([^\n]+)", text, flags=re.IGNORECASE):
            items = re.split(r"[,; ]+", m.group(2).strip())
            for it in items:
                it = it.strip()
                if not it: continue
                mat = aliases.get(it, it)
                if mat in materials:
                    out.append(MaterialMetric(material=mat, source=self.source_type, file_path=path, weight=1.0))
        for m in re.finditer(r"-\s*([A-Za-z0-9_]+)", text):
            it = m.group(1).strip()
            mat = aliases.get(it, it)
            if mat in materials:
                out.append(MaterialMetric(material=mat, source=self.source_type, file_path=path, weight=1.0))
        return out
