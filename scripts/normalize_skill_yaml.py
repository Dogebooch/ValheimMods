from __future__ import annotations

import re
from pathlib import Path
from datetime import datetime


def normalize_and_dedup_skill_yaml(yaml_path: Path) -> tuple[int, int, int]:
    """Normalize PrefabName headers to exact internal prefabs and deduplicate blocks.

    Returns (total_blocks, headers_changed, duplicates_removed).
    """
    text = yaml_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    header_pat = re.compile(r"^(?P<indent>\s*)-\s*PrefabName\s*:\s*(?P<name>.+?)\s*$")

    out: list[str] = []
    seen: set[str] = set()
    i = 0
    total_blocks = 0
    headers_changed = 0
    duplicates_removed = 0

    while i < len(lines):
        m = header_pat.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue

        # Collect a full block: header + following lines until next header or EOF
        start = i
        block: list[str] = [lines[i]]
        i += 1
        while i < len(lines) and not header_pat.match(lines[i]):
            block.append(lines[i])
            i += 1

        total_blocks += 1
        indent = m.group("indent")
        name_raw = m.group("name").strip()

        # Extract exact prefab: prefer content in last parentheses if present, else raw trimmed
        if "(" in name_raw:
            # take everything after the last '(' and trim any trailing ')'
            exact = name_raw[name_raw.rfind("(") + 1 :]
            exact = exact.split(")", 1)[0].strip()
        else:
            exact = name_raw

        # If the header changed, count it
        if exact != name_raw:
            headers_changed += 1

        # Compose normalized header
        new_header = f"{indent}- PrefabName: {exact}\n"

        # Deduplicate on exact prefab name
        if exact in seen:
            duplicates_removed += 1
            continue

        seen.add(exact)
        out.append(new_header)
        out.extend(block[1:])

    yaml_path.write_text("".join(out), encoding="utf-8", newline="\n")
    return total_blocks, headers_changed, duplicates_removed


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    yaml_path = repo_root / "Valheim" / "profiles" / "Dogeheim_Player" / "BepInEx" / "config" / "Detalhes.ItemRequiresSkillLevel.yml"
    if not yaml_path.exists():
        print(f"YAML not found: {yaml_path}")
        return 1
    # Backup first
    backup = yaml_path.with_suffix(yaml_path.suffix + ".bak")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_ts = yaml_path.with_suffix(yaml_path.suffix + f".{ts}.bak")
    try:
        backup_ts.write_text(yaml_path.read_text(encoding="utf-8"), encoding="utf-8")
    except Exception:
        # fall back to plain .bak
        try:
            backup.write_text(yaml_path.read_text(encoding="utf-8"), encoding="utf-8")
        except Exception:
            pass

    total_blocks, changed, dups = normalize_and_dedup_skill_yaml(yaml_path)
    print(f"Processed blocks: {total_blocks}; headers normalized: {changed}; duplicates removed: {dups}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


