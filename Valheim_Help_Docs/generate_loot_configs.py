"""Utility to generate loot configuration files.

This script loads loot definitions and writes configuration files for the
Valheim mod setup. Prior to writing, it validates that there are no duplicate
(PrefabID, ItemPrefab) pairs to prevent stacked drop probabilities.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable, List, Dict, Tuple


def load_entries(source: Path) -> List[Dict[str, object]]:
    """Load loot entries from a JSON file.

    The expected format is a list of dictionaries, each containing at least
    ``PrefabID`` and ``ItemPrefab`` keys. The actual generation logic of this
    project may extend these entries with additional metadata.
    """
    with source.open() as f:
        data = json.load(f)
    if not isinstance(data, list):  # pragma: no cover - defensive
        raise ValueError("Input JSON must contain a list of entries")
    return data


def find_duplicate_pairs(entries: Iterable[Dict[str, object]]) -> List[Tuple[object, object]]:
    """Return a list of duplicated (PrefabID, ItemPrefab) pairs."""
    pairs = [(e.get("PrefabID"), e.get("ItemPrefab")) for e in entries]
    counts = Counter(pairs)
    return [pair for pair, count in counts.items() if count > 1]


def write_configs(entries: Iterable[Dict[str, object]], output_dir: Path) -> None:
    """Placeholder for writing configuration files.

    The actual implementation depends on the project's requirements. This
    function exists to illustrate where generation would occur once the entries
    have been validated.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    # Here we simply dump the entries back as JSON to demonstrate writing.
    out_file = output_dir / "loot_entries.json"
    with out_file.open("w") as f:
        json.dump(list(entries), f, indent=2)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Path to JSON file with loot entries")
    parser.add_argument("--output", type=Path, default=Path("output"), help="Directory for generated configs")
    parser.add_argument(
        "--warn-only",
        action="store_true",
        help="Print a warning instead of raising an error on duplicates",
    )
    args = parser.parse_args(argv)

    entries = load_entries(args.source)
    duplicates = find_duplicate_pairs(entries)
    if duplicates:
        msg = f"Duplicate (PrefabID, ItemPrefab) combinations found: {duplicates}. Generation skipped."
        if args.warn_only:
            print(msg, file=sys.stderr)
            return 1
        raise ValueError(msg)

    write_configs(entries, args.output)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
