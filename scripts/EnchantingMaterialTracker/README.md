# Enchanting Material Tracker (EMT)

A Python tool to compare **active** enchanting-material configurations vs a **baseline RelicHeim backup**. 
It reads your config files (does not modify them), aggregates per-material availability scores by source, and reports % changes.

## Install
```bash
pip install -r requirements.txt   # optional extras (pyyaml, watchdog, jsonschema, pandas, reportlab)
```
Copy `settings.example.json` to `settings.json` and edit paths.

## Run
```bash
python -m emt.cli compare
python -m emt.gui       # optional GUI
```
