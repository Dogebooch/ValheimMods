
from __future__ import annotations
from typing import Iterable, Tuple, List
from .models import MaterialMetric
def validate_metrics(metrics: Iterable[MaterialMetric]) -> List[Tuple[str, str]]:
    issues: List[Tuple[str, str]] = []
    for m in metrics:
        if m.source in ("epicloot_chest_cfg", "drop_that_list_cfg", "drop_that_char_cfg"):
            if m.weight and not (0.01 <= m.weight <= 10.0):
                issues.append((m.file_path, f"{m.material}: weight {m.weight} out of 0.01-10.0"))
            if (m.amount_min and m.amount_max) and (m.amount_min > m.amount_max):
                issues.append((m.file_path, f"{m.material}: amount_min {m.amount_min} > amount_max {m.amount_max}"))
        if m.source == "world_locations_yml":
            if m.stack_min and m.stack_max and m.stack_min > m.stack_max:
                issues.append((m.file_path, f"{m.material}: stackMin {m.stack_min} > stackMax {m.stack_max}"))
    return issues
