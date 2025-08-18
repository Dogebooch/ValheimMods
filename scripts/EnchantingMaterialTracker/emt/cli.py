
from __future__ import annotations
import argparse, os
from .config import load_settings
from .snapshot import take_snapshot
from .db import DB
from .compare import compare_snapshots
from .export import export_json, export_csv, export_md
def main():
    ap = argparse.ArgumentParser(prog="emt", description="Enchanting Material Tracker")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("compare", help="Take baseline+active snapshots (if needed) and compare them.")
    p_snap = sub.add_parser("snapshot", help="Take a snapshot for a given root dir.")
    p_snap.add_argument("--root", required=False, help="Root directory to snapshot. Defaults to active_config_dir.")
    args = ap.parse_args()
    settings = load_settings()
    if args.cmd == "snapshot":
        root = args.root or settings["active_config_dir"]
        snap_id = take_snapshot(root, settings)
        print(f"Snapshot {snap_id} created for {root}"); return
    if args.cmd == "compare":
        try:
            db = DB(settings["db_path"])
            base_id = db.latest_snapshot_id_for_root(settings["baseline_backup_dir"]) or take_snapshot(settings["baseline_backup_dir"], settings)
            act_id = db.latest_snapshot_id_for_root(settings["active_config_dir"]) or take_snapshot(settings["active_config_dir"], settings)
            db.close()
            results = compare_snapshots(settings["db_path"], base_id, act_id)
            outdir = os.path.join(os.path.dirname(settings["db_path"]), "exports")
            print("Exports:")
            print("  JSON:", export_json(results, outdir))
            print("  CSV :", export_csv(results, outdir))
            print("  MD  :", export_md(results, outdir))
        except Exception as e:
            print(f"Error during comparison: {e}")
            return 1
if __name__ == "__main__":
    main()
