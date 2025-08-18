
from __future__ import annotations
import os, json, csv, datetime
def ensure_dir(path: str): os.makedirs(path, exist_ok=True)
def export_json(results, outdir: str) -> str:
    ensure_dir(outdir)
    p = os.path.join(outdir, f"comparison_{datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.json")
    if not results:
        results = []
    open(p, "w", encoding="utf-8").write(json.dumps(results, indent=2)); return p
def export_csv(results, outdir: str) -> str:
    ensure_dir(outdir)
    p = os.path.join(outdir, f"comparison_{datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.csv")
    import csv
    if not results:
        results = []
    rows = [{"material": r["material"], "total_base": r["total_base"], "total_current": r["total_current"], "pct_change_total": r["pct_change_total"]} for r in results]
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["material","total_base","total_current","pct_change_total"])
        w.writeheader()
        for row in rows: w.writerow(row)
    return p
def export_md(results, outdir: str) -> str:
    ensure_dir(outdir)
    p = os.path.join(outdir, f"comparison_{datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.md")
    lines = ["# Enchanting Materials Comparison\n"]
    if not results:
        lines.append("No materials found for comparison.")
    else:
        for r in results:
            lines += [f"## {r['material']}",
                      f"- Total (Baseline): **{r['total_base']:.4f}**",
                      f"- Total (Current): **{r['total_current']:.4f}**",
                      f"- % Change: **{r['pct_change_total']:.2f}%**",""]
    open(p, "w", encoding="utf-8").write("\n".join(lines)); return p
