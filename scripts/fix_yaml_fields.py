"""Line-based YAML fixer for ExhibitionName and PrefabName fields."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

SPECIAL_CHARS_RE = re.compile(r"[():@/ ]")


def split_comment(text: str) -> tuple[str, str]:
    """Split a line into value and comment portions."""
    for i, ch in enumerate(text):
        if ch == '#' and (i == 0 or text[i - 1].isspace()):
            return text[:i], text[i:]
    return text, ''


def fix_file(source: Path, dest: Path) -> None:
    """Apply line-based fixes and write to ``dest``."""
    with source.open('r', encoding='utf-8') as fin, dest.open('w', encoding='utf-8') as fout:
        for original in fin:
            line = original.rstrip('\n')
            newline = '\n' if original.endswith('\n') else ''

            m_ex = re.match(r"^(\s*ExhibitionName:\s*)(.*)$", line)
            if m_ex:
                value, comment = split_comment(m_ex.group(2))
                if value.strip() == '':
                    space = '' if m_ex.group(1).endswith(' ') else ' '
                    fout.write(f"{m_ex.group(1)}{space}\"\"{value}{comment}{newline}")
                else:
                    fout.write(original)
                continue

            m_prefab = re.match(r"^(\s*PrefabName:\s*)(.*)$", line)
            if m_prefab:
                value, comment = split_comment(m_prefab.group(2))
                stripped = value.strip()
                if stripped:
                    is_quoted = (
                        (stripped.startswith('"') and stripped.endswith('"')) or
                        (stripped.startswith("'") and stripped.endswith("'"))
                    )
                    if not is_quoted and SPECIAL_CHARS_RE.search(stripped):
                        leading = value[: len(value) - len(value.lstrip())]
                        trailing = value[len(value.rstrip()):]
                        value = f"{leading}\"{stripped}\"{trailing}"
                fout.write(f"{m_prefab.group(1)}{value}{comment}{newline}")
                continue

            fout.write(original)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fix ExhibitionName and PrefabName formatting in YAML files.")
    parser.add_argument('input', type=Path, help='Path to input YAML file')
    parser.add_argument('output', type=Path, help='Path to write fixed YAML file')
    args = parser.parse_args()

    fix_file(args.input, args.output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
