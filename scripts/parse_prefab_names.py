#!/usr/bin/env python3
"""Parse VNEI exported files to extract prefab names.

This script reads various exports found in
``Valheim_Help_Docs/VNEI-Export`` to collect mappings between
internal prefab names and their localized names.

It understands the following formats:
- ``VNEI.indexed.items.csv``
- ``VNEI.indexed.items.txt``
- ``VNEI.indexed.items.yml``

The resulting data is exposed via :func:`get_prefab_name_mappings` which
returns a list of dictionaries with keys ``internal_name`` and
``localized_name``. Entries are normalised by trimming whitespace and
stripping any surrounding quotes.
"""
from __future__ import annotations

from pathlib import Path
import csv
import re
from typing import Dict, List

BASE_DIR = Path("Valheim_Help_Docs") / "VNEI-Export"


def _normalise(value: str) -> str:
    """Trim whitespace and surrounding quotes from ``value``."""
    return value.strip().strip('"').strip("'")


def parse_vnei_csv(path: Path) -> List[Dict[str, str]]:
    """Parse ``VNEI.indexed.items.csv`` for prefab mappings."""
    results: List[Dict[str, str]] = []
    with path.open(newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            internal = _normalise(row.get('Internal Name', ''))
            localized = _normalise(row.get('Localized Name', ''))
            if internal:
                results.append({'internal_name': internal, 'localized_name': localized})
    return results


def parse_vnei_txt(path: Path) -> List[Dict[str, str]]:
    """Parse ``VNEI.indexed.items.txt`` for prefab mappings."""
    pattern = re.compile(
        r"Internal Name:\s*(?P<internal>[^,]+),\s*Localized Name:\s*(?P<localized>[^,]+)",
        re.IGNORECASE,
    )
    results: List[Dict[str, str]] = []
    with path.open(encoding='utf-8') as handle:
        for line in handle:
            match = pattern.search(line)
            if match:
                internal = _normalise(match.group('internal'))
                localized = _normalise(match.group('localized'))
                results.append({'internal_name': internal, 'localized_name': localized})
    return results


def parse_vnei_yml(path: Path) -> List[Dict[str, str]]:
    """Parse ``VNEI.indexed.items.yml`` for prefab names.

    This format only contains internal names. Localised names will be empty
    strings.
    """
    results: List[Dict[str, str]] = []
    with path.open(encoding='utf-8') as handle:
        for line in handle:
            line = line.strip()
            if line.startswith('- '):
                internal = _normalise(line[2:])
                results.append({'internal_name': internal, 'localized_name': ''})
    return results


def get_prefab_name_mappings(base_dir: Path | None = None) -> List[Dict[str, str]]:
    """Load prefab mappings from VNEI export files.

    Parameters
    ----------
    base_dir:
        Directory containing the VNEI export files. Defaults to the project
        ``Valheim_Help_Docs/VNEI-Export`` path.

    Returns
    -------
    list of dict
        Normalised mappings with ``internal_name`` and ``localized_name`` keys.
    """
    base = base_dir or BASE_DIR
    entries: Dict[str, str] = {}

    csv_file = base / 'VNEI.indexed.items.csv'
    if csv_file.exists():
        for item in parse_vnei_csv(csv_file):
            entries[item['internal_name']] = item['localized_name']

    txt_file = base / 'VNEI.indexed.items.txt'
    if txt_file.exists():
        for item in parse_vnei_txt(txt_file):
            entries.setdefault(item['internal_name'], item['localized_name'])

    yml_file = base / 'VNEI.indexed.items.yml'
    if yml_file.exists():
        for item in parse_vnei_yml(yml_file):
            entries.setdefault(item['internal_name'], item['localized_name'])

    return [
        {'internal_name': name, 'localized_name': entries[name]}
        for name in sorted(entries)
    ]


if __name__ == '__main__':
    mappings = get_prefab_name_mappings()
    print(f"Loaded {len(mappings)} prefab mappings")
    for entry in mappings[:10]:
        print(f"{entry['internal_name']}: {entry['localized_name']}")
