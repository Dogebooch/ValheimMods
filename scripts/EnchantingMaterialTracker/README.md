# Enchanting Material Tracker (EMT)

A Python tool to compare **active** enchanting-material configurations vs a **baseline RelicHeim backup**. 
It reads your config files (does not modify them), aggregates per-material availability scores by source, and reports % changes.

## Quick Start

### GUI Mode (Recommended)
From the `scripts/` directory, double-click `run_emt.bat` to open the graphical interface.

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
- Right-click context menu
- Copy to clipboard features

### Command Line Interface
Available commands:
- `run_emt.bat compare` - Compare baseline vs active configurations (from scripts/ directory)
- `run_emt.bat snapshot --root "path"` - Take a snapshot of a directory (from scripts/ directory)

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
- **JSON**: Machine-readable data
- **CSV**: Spreadsheet-compatible format
- **MD**: Markdown report

## Troubleshooting

If you get errors:
1. Make sure Python 3.6+ is installed
2. Run `pip install -r requirements.txt` to install dependencies
3. Check that the paths in `settings.json` are correct
4. Ensure the directories exist and are accessible
