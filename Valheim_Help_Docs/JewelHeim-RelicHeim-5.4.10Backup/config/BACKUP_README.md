# RelicHeim Backup Files - Naming Convention

This directory contains backup files from RelicHeim version 5.4.10.
All files have been prefixed with "BACKUP_5.4.10_" to avoid naming conflicts with current user configuration files.

## File Naming Convention
- Original: `org.bepinex.plugins.sailing.cfg`
- Backup: `BACKUP_5.4.10_org.bepinex.plugins.sailing.cfg`

## Purpose
These files serve as reference material and backup copies of the original RelicHeim configuration.
They should not be confused with current user configuration files located in:
`Valheim/profiles/Dogeheim_Player/BepInEx/config/`

## Usage
When parsing or analyzing configuration files:
1. Current user configs: Use files WITHOUT the "BACKUP_5.4.10_" prefix
2. Reference/backup files: Use files WITH the "BACKUP_5.4.10_" prefix

This naming convention ensures no conflicts when comparing or processing configuration files.
