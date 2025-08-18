
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Literal
SourceType = Literal["epicloot_chest_cfg", "drop_that_list_cfg", "drop_that_char_cfg", "world_locations_yml", "epicloot_json", "backpack_cfg"]
@dataclass
class MaterialMetric:
    material: str
    source: SourceType
    file_path: str
    weight: float = 0.0
    chance: float = 0.0
    amount_min: float = 0.0
    amount_max: float = 0.0
    stack_min: float = 0.0
    stack_max: float = 0.0
    def availability_score(self) -> float:
        avg_amount = 0.0
        if self.amount_min > 0 or self.amount_max > 0:
            lo = self.amount_min if self.amount_min > 0 else self.amount_max
            hi = self.amount_max if self.amount_max > 0 else self.amount_min
            avg_amount = (lo + hi) / 2.0
        if self.stack_min > 0 or self.stack_max > 0:
            lo = self.stack_min if self.stack_min > 0 else self.stack_max
            hi = self.stack_max if self.stack_max > 0 else self.stack_min
            avg_amount = max(avg_amount, (lo + hi) / 2.0)
        base = self.chance if self.chance > 0 else self.weight
        if base <= 0 and avg_amount > 0:
            base = 1.0
        return base * (avg_amount if avg_amount > 0 else 1.0)
@dataclass
class Snapshot:
    root_dir: str
    created_at: str
    metrics: List[MaterialMetric] = field(default_factory=list)
