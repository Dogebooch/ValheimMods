
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

def classify_source_type(source: str) -> str:
    """Classify source as boss, monster, chest, etc."""
    source_lower = source.lower()
    
    # Boss patterns
    boss_patterns = ['boss', 'elder', 'bonemass', 'moder', 'yagluth', 'queen', 'king']
    if any(pattern in source_lower for pattern in boss_patterns):
        return "boss"
    
    # Monster patterns
    monster_patterns = ['greydwarf', 'troll', 'draugr', 'skeleton', 'blob', 'leech', 
                       'wraith', 'surtling', 'wolf', 'fenring', 'lox', 'goblin']
    if any(pattern in source_lower for pattern in monster_patterns):
        return "monster"
    
    # Chest patterns
    chest_patterns = ['chest', 'treasure', 'crypt', 'tomb', 'burial', 'vault']
    if any(pattern in source_lower for pattern in chest_patterns):
        return "chest"
    
    return "other"

def aggregate_by_source_type(material_sources: dict) -> dict:
    """Aggregate material scores by source type (boss, monster, chest, etc.)"""
    aggregated = defaultdict(float)
    
    for source, score in material_sources.items():
        source_type = classify_source_type(source)
        aggregated[source_type] += score
    
    return dict(aggregated)

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
        
        # Aggregate by source type
        base_by_type = aggregate_by_source_type(base.get(m, {}))
        cur_by_type = aggregate_by_source_type(cur.get(m, {}))
        
        entry = {
            "material": m, 
            "total_base": total_base, 
            "total_current": total_cur,
            "pct_change_total": percent_change(total_cur, total_base), 
            "sources": {},
            "by_source_type": {}
        }
        
        # Individual sources
        for s in sorted(sources):
            b = base.get(m, {}).get(s, 0.0)
            c = cur.get(m, {}).get(s, 0.0)
            entry["sources"][s] = {
                "baseline": b, 
                "current": c, 
                "pct_change": percent_change(c, b)
            }
        
        # By source type
        all_source_types = set(base_by_type.keys()) | set(cur_by_type.keys())
        for source_type in all_source_types:
            b = base_by_type.get(source_type, 0.0)
            c = cur_by_type.get(source_type, 0.0)
            entry["by_source_type"][source_type] = {
                "baseline": b,
                "current": c,
                "pct_change": percent_change(c, b)
            }
        
        results.append(entry)
    
    db.close()
    return results

def generate_detailed_report(comparison_results: list) -> str:
    """Generate a detailed report showing drop chances by source type"""
    report_lines = []
    report_lines.append("# Material Drop Chance Analysis")
    report_lines.append("")
    report_lines.append("This report shows the drop chances for RelicHeim materials from different sources.")
    report_lines.append("")
    
    # Group materials by tier (assuming naming convention)
    tier_materials = defaultdict(list)
    for result in comparison_results:
        material = result["material"]
        if "Magic" in material:
            tier_materials["Magic"].append(result)
        elif "Rare" in material:
            tier_materials["Rare"].append(result)
        elif "Epic" in material:
            tier_materials["Epic"].append(result)
        elif "Legendary" in material:
            tier_materials["Legendary"].append(result)
        elif "Mythic" in material:
            tier_materials["Mythic"].append(result)
        else:
            tier_materials["Other"].append(result)
    
    for tier, materials in tier_materials.items():
        report_lines.append(f"## {tier} Tier Materials")
        report_lines.append("")
        
        for material_data in materials:
            material = material_data["material"]
            report_lines.append(f"### {material}")
            report_lines.append("")
            
            # Show total changes
            total_base = material_data["total_base"]
            total_current = material_data["total_current"]
            total_change = material_data["pct_change_total"]
            
            report_lines.append(f"**Total Drop Chance:**")
            report_lines.append(f"- Baseline: {total_base:.2f}%")
            report_lines.append(f"- Current: {total_current:.2f}%")
            report_lines.append(f"- Change: {total_change:+.1f}%")
            report_lines.append("")
            
            # Show by source type
            by_type = material_data["by_source_type"]
            
            if "boss" in by_type:
                boss_data = by_type["boss"]
                report_lines.append(f"**Boss Drops:**")
                report_lines.append(f"- Baseline: {boss_data['baseline']:.2f}%")
                report_lines.append(f"- Current: {boss_data['current']:.2f}%")
                report_lines.append(f"- Change: {boss_data['pct_change']:+.1f}%")
                report_lines.append("")
            
            if "monster" in by_type:
                monster_data = by_type["monster"]
                report_lines.append(f"**Monster Drops:**")
                report_lines.append(f"- Baseline: {monster_data['baseline']:.2f}%")
                report_lines.append(f"- Current: {monster_data['current']:.2f}%")
                report_lines.append(f"- Change: {monster_data['pct_change']:+.1f}%")
                report_lines.append("")
            
            if "chest" in by_type:
                chest_data = by_type["chest"]
                report_lines.append(f"**Chest Drops:**")
                report_lines.append(f"- Baseline: {chest_data['baseline']:.2f}%")
                report_lines.append(f"- Current: {chest_data['current']:.2f}%")
                report_lines.append(f"- Change: {chest_data['pct_change']:+.1f}%")
                report_lines.append("")
            
            report_lines.append("---")
            report_lines.append("")
    
    return "\n".join(report_lines)
