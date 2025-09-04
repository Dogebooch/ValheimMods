import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional


# Workspace roots
WS = Path(__file__).resolve().parents[1]
CONFIG_DIR = WS / "config"
DOGE_DIR = WS / "Dogeheim"
SNAP_ROOT = WS / "scripts" / "snapshots" / "backups"
DIST_ROOT_DEFAULT = WS / "Dogeheim_Distribution"

# Files
CHANGELOG_PATH = DOGE_DIR / "CHANGELOG.md"
MANIFEST_PATH = DOGE_DIR / "manifest.json"

# Exclude dev-only folders from distribution; extend as needed
EXCLUDE_RELATIVE = {
    "config/backup_before_debug",
    "config/.snapshots",
}


def safe_mkdir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def parse_version_from_changelog(changelog_path: Path) -> Optional[str]:
    """Parse the first version from the changelog header lines like: '## [1.7.0] - ...'"""
    if not changelog_path.exists():
        return None
    pattern = re.compile(r"^\s*##\s*\[(\d+\.\d+\.\d+)\]")
    try:
        for line in changelog_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            m = pattern.match(line)
            if m:
                return m.group(1)
    except Exception:
        return None
    return None


def read_manifest(manifest_path: Path) -> dict:
    if not manifest_path.exists():
        return {}
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def write_manifest(manifest_path: Path, data: dict):
    safe_mkdir(manifest_path.parent)
    manifest_path.write_text(json.dumps(data, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")


def sync_manifest_version_from_changelog(changelog_path: Path = CHANGELOG_PATH, manifest_path: Path = MANIFEST_PATH) -> Optional[str]:
    """Ensure manifest.json version_number matches the top version in CHANGELOG.md.
    Returns the version used (or None if not changed)."""
    version = parse_version_from_changelog(changelog_path)
    if not version:
        print("Warning: Could not parse version from CHANGELOG.md; leaving manifest unchanged.")
        return None

    manifest = read_manifest(manifest_path)
    if not manifest:
        print("Warning: manifest.json missing or unreadable; creating a minimal one.")
        manifest = {"name": "Dogeheim", "version_number": version, "dependencies": []}
        write_manifest(manifest_path, manifest)
        print(f"manifest.json created with version {version}")
        return version

    old_version = manifest.get("version_number")
    if old_version != version:
        manifest["version_number"] = version
        write_manifest(manifest_path, manifest)
        print(f"manifest.json version updated: {old_version} -> {version}")
    else:
        print(f"manifest.json already at version {version}")
    return version


def create_snapshot(name: str):
    safe_mkdir(SNAP_ROOT)
    snap_name = f"{name}_{timestamp()}"
    snap_dir = SNAP_ROOT / snap_name
    shutil.copytree(CONFIG_DIR, snap_dir)
    print(f"Snapshot created: {snap_dir}")


def restore_snapshot(name_or_prefix: str):
    if not SNAP_ROOT.exists():
        print("No snapshots found.")
        sys.exit(1)
    matches = sorted([p for p in SNAP_ROOT.iterdir() if p.is_dir() and p.name.startswith(name_or_prefix)])
    if not matches:
        print(f"No snapshot matching '{name_or_prefix}' found.")
        sys.exit(1)
    snap = matches[-1]
    # Backup current config before restore
    safe_mkdir(SNAP_ROOT)
    auto_backup = SNAP_ROOT / f"auto_backup_before_restore_{timestamp()}"
    shutil.copytree(CONFIG_DIR, auto_backup)
    # Restore
    tmp_restore = WS / f".tmp_restore_{timestamp()}"
    shutil.copytree(snap, tmp_restore)
    shutil.rmtree(CONFIG_DIR)
    shutil.move(str(tmp_restore), str(CONFIG_DIR))
    print(f"Restored snapshot: {snap}")


def _should_exclude(path: Path) -> bool:
    try:
        rel = path.relative_to(WS).as_posix()
    except ValueError:
        return False
    for ex in EXCLUDE_RELATIVE:
        if rel.startswith(ex):
            return True
    return False


def _copy_config_to(dist_root: Path):
    # Thunderstore expects files relative to the game root. For configs,
    # place them under BepInEx/config inside the package.
    dst_cfg = dist_root / "BepInEx" / "config"
    if dst_cfg.exists():
        shutil.rmtree(dst_cfg)
    # selective copy preserving tree, excluding dev-only dirs
    for src in CONFIG_DIR.rglob("*"):
        if _should_exclude(src):
            continue
        rel = src.relative_to(WS)
        # Remap 'config/...' → 'BepInEx/config/...'
        if str(rel).startswith("config/"):
            rel = Path("BepInEx") / Path(str(rel))
        dst = dist_root / rel
        if src.is_dir():
            safe_mkdir(dst)
        else:
            safe_mkdir(dst.parent)
            shutil.copy2(src, dst)


def _copy_if_exists(src: Path, dst: Path):
    if src.exists():
        safe_mkdir(dst.parent)
        shutil.copy2(src, dst)


def _read_manifest_version(manifest_path: Path) -> str:
    if not manifest_path.exists():
        return "0.0.0"
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        return data.get("version_number", "0.0.0")
    except Exception:
        return "0.0.0"


def build_distribution(dist_root: Path, sync_version: bool = True):
    # Optionally sync version first
    if sync_version:
        sync_manifest_version_from_changelog()

    safe_mkdir(dist_root)
    # 1) copy config
    _copy_config_to(dist_root)
    # 2) include manifest/icon/readme if available (from Dogeheim/)
    manifest_src = MANIFEST_PATH
    icon_src = DOGE_DIR / "icon.png"
    readme_src = DOGE_DIR / "README.md"
    changelog_src = DOGE_DIR / "CHANGELOG.md"
    _copy_if_exists(manifest_src, dist_root / "manifest.json")
    _copy_if_exists(icon_src, dist_root / "icon.png")
    _copy_if_exists(readme_src, dist_root / "README.md")
    _copy_if_exists(changelog_src, dist_root / "CHANGELOG.md")
    print(f"Distribution folder ready at: {dist_root}")


def zip_distribution(dist_root: Path, out_dir: Optional[Path] = None) -> Path:
    out_dir = out_dir or dist_root
    manifest_path = dist_root / "manifest.json"
    version = _read_manifest_version(manifest_path)
    pkg_name = f"{dist_root.name}-{version}-{timestamp()}.zip"
    out_zip = out_dir / pkg_name
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in dist_root.rglob("*"):
            if p.is_file():
                arcname = p.relative_to(dist_root).as_posix()
                z.write(p, arcname)
    print(f"Distribution zip created: {out_zip}")
    return out_zip


def main():
    # Click-n-Play mode: double-click or no-arg run performs full package flow
    if len(sys.argv) == 1:
        print("Click-n-Play: syncing version → building distribution → creating zip …")
        try:
            version = sync_manifest_version_from_changelog()
            dist_root = DIST_ROOT_DEFAULT
            build_distribution(dist_root, sync_version=False)
            out_zip = zip_distribution(dist_root, None)
            # Try to open the distribution folder for convenience
            try:
                if sys.platform.startswith("win"):
                    os.startfile(str(dist_root))  # type: ignore[attr-defined]
                elif sys.platform == "darwin":
                    subprocess.run(["open", str(dist_root)], check=False)
                else:
                    subprocess.run(["xdg-open", str(dist_root)], check=False)
            except Exception:
                pass
            print(f"Done. Version: {version or 'unknown'}. Zip: {out_zip}")
        except Exception as e:
            print(f"Packaging failed: {e}")
            sys.exit(1)
        return

    ap = argparse.ArgumentParser(description="Package modpack and manage config snapshots (with changelog→manifest version sync)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp_sync = sub.add_parser("sync-version", help="Sync manifest.json version_number from top version in CHANGELOG.md")

    sp_snap = sub.add_parser("snapshot", help="Create a config snapshot")
    sp_snap.add_argument("--name", required=True, help="Snapshot name prefix")

    sp_restore = sub.add_parser("restore", help="Restore a config snapshot")
    sp_restore.add_argument("--match", required=True, help="Snapshot name or prefix to match")

    sp_pack = sub.add_parser("package", help="Build distribution folder and zip")
    sp_pack.add_argument("--dist", default=str(DIST_ROOT_DEFAULT), help="Distribution root folder")
    sp_pack.add_argument("--zip-out", default=None, help="Optional output dir for zip (defaults to dist root)")
    sp_pack.add_argument("--no-sync", action="store_true", help="Do not sync version from changelog before packaging")

    args = ap.parse_args()

    if args.cmd == "sync-version":
        v = sync_manifest_version_from_changelog()
        if v:
            print(f"Synced version to {v}")
    elif args.cmd == "snapshot":
        create_snapshot(args.name)
    elif args.cmd == "restore":
        restore_snapshot(args.match)
    elif args.cmd == "package":
        dist_root = Path(args.dist).resolve()
        build_distribution(dist_root, sync_version=not args.no_sync)
        zip_out = Path(args.zip_out).resolve() if args.zip_out else None
        zip_distribution(dist_root, zip_out)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()


