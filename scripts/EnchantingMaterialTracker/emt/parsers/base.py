
from __future__ import annotations
from typing import Iterable
from ..models import MaterialMetric
class Parser:
    source_type: str
    exts: tuple[str, ...]
    def supports(self, path: str) -> bool:
        return path.lower().endswith(self.exts)
    def parse(self, path: str, materials: set[str], aliases: dict[str, str]) -> Iterable[MaterialMetric]:
        raise NotImplementedError
