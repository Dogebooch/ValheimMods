
from __future__ import annotations
from collections import defaultdict
from .db import DB
def aggregate_scores(db: DB, snapshot_id: int):
    rows = db.fetch_snapshot_metrics(snapshot_id)
    agg = defaultdict(lambda: defaultdict(float))  # material -> source -> score
    for material, source, score in rows:
        agg[material][source] += score or 0.0
    return agg
def percent_change(new: float, old: float) -> float:
    if old == 0 and new == 0: return 0.0
    if old == 0: return 100.0
    return (new - old) / old * 100.0
def compare_snapshots(db_path: str, baseline_id: int, active_id: int):
    db = DB(db_path)
    base = aggregate_scores(db, baseline_id)
    cur = aggregate_scores(db, active_id)
    materials = set(base.keys()) | set(cur.keys())
    results = []
    for m in sorted(materials):
        sources = set(base.get(m, {}).keys()) | set(cur.get(m, {}).keys())
        total_base = sum(base.get(m, {}).values())
        total_cur = sum(cur.get(m, {}).values())
        entry = {"material": m, "total_base": total_base, "total_current": total_cur,
                 "pct_change_total": percent_change(total_cur, total_base), "sources": {}}
        for s in sorted(sources):
            b = base.get(m, {}).get(s, 0.0); c = cur.get(m, {}).get(s, 0.0)
            entry["sources"][s] = {"baseline": b, "current": c, "pct_change": percent_change(c, b)}
        results.append(entry)
    db.close()
    return results
