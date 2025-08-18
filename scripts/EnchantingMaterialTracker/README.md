# Enchanting Material Tracker (EMT)

A Python tool to compare **active** enchanting‑material configurations vs a **baseline RelicHeim backup**. 
It reads your config files (does not modify them), aggregates per‑material availability scores by source, and reports % changes.

## Quick Start

### GUI Mode (Recommended)
From the `scripts/` directory, double‑click `run_emt.bat` to open the graphical interface.

### Command Line Mode
From the `scripts/` directory, run `run_emt.bat compare` to compare configurations from the command line.

## Installation
```bash
pip install -r requirements.txt   # optional extras (pyyaml, watchdog, jsonschema, pandas, reportlab)
```
Copy `settings.example.json` to `settings.json` and edit paths.

## How to Use

### GUI Interface
The GUI provides a complete interface with:
- Table view of material comparisons
- Export functionality (JSON, CSV, Markdown)
- Snapshot taking
- Path browsing and configuration
- Right‑click context menu
- Copy to clipboard features

### Command Line Interface
Available commands:
- `run_emt.bat compare` – Compare baseline vs active configurations (from scripts/ directory)
- `run_emt.bat snapshot --root "path"` – Take a snapshot of a directory (from scripts/ directory)

## What It Does

The tool compares your current Valheim mod configurations against a baseline RelicHeim backup to show:
- Which enchanting materials are available
- How their availability has changed
- Percentage changes in material availability

## Configuration

Edit `settings.json` to configure:
- **active_config_dir**: Your current Valheim mod config directory
- **baseline_backup_dir**: The RelicHeim backup directory to compare against
- **documentation_md**: Path to enchanting materials documentation
- **db_path**: SQLite database location
- **materials_registry**: Materials definition file

## Output

Results are exported to the `exports/` folder in three formats:
- **JSON**: Machine‑readable data
- **CSV**: Spreadsheet‑compatible format
- **MD**: Markdown report

## Troubleshooting

If you get errors:
1. Make sure Python 3.6+ is installed
2. Run `pip install -r requirements.txt` to install dependencies
3. Check that the paths in `settings.json` are correct
4. Ensure the directories exist and are accessible

## Drop Chance Calculation Notes

When interpreting the "chance when I kill any monster" metric produced by EMT, keep in mind that drop tables are probabilistic, and simply summing per‑mob percentages can easily exceed 100 %.  Instead EMT treats each drop roll as an independent event and combines them as follows:

- **Per‑mob union probability:** If a mob has several independent drop rolls for enchanting materials, the chance of at least one material dropping is `1 − ∏(1 − p_i)` where `p_i` is the chance for each roll.
- **Set draws:** Some drop tables pull one or two items from a set (for example `NovusMats`).  If the base chance for the roll is `b` and the probability that a single draw yields an item from the enchanting set is `q`, then the roll’s chance of yielding at least one enchanting item is `b × (1 − (1 − q)^d)` where `d` is the number of draws.  Adding `b × q` twice will overcount.
- **Baseline percentages:** RelicHeim’s baseline drop rate is not a flat 10 % for every item.  The baseline for a specific runestone depends on its set’s weight distribution.  For example, if a set contains a runestone and a shard at equal weights, the chance of getting a runestone on a 10 % / 5 % baseline is `0.10×0.5 + 0.05×(1 − (1 − 0.5)^2) = 8.75 %`.

### Weighting modes

EMT can aggregate per‑mob probabilities in three ways:

1. **Uniform** (default): Every creature counts equally.
2. **Spawn‑weighted**: Weights are derived from Spawn‑That configuration files in your active config directory.
3. **Kill‑weighted**: Provide a CSV of prefabs and kill counts to weight by your actual play‑through.

Select the weighting mode via the command‑line switch `--weighting {uniform,spawn,kills}` or through the GUI.

### CSV logging

For debugging and transparency EMT writes an `exports/roll_log.csv` file every time you run the comparison.  Each row in this file captures the full context of a drop roll – the prefab, source (baseline vs active), base chance, set name, number of draws, computed `q` value and the resulting per‑roll probability.  If any probability falls outside the range 0–100 %, EMT logs an assertion and clamps the offending value.

### Batch script hygiene

Avoid performing percentage calculations in the accompanying `.bat` scripts – these scripts should only launch the Python tool.  If you need to echo a literal `%` character in a batch file, write it as `%%`.