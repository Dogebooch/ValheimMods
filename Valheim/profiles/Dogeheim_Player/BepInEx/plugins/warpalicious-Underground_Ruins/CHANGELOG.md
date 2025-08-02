| `Version` | `Update Notes`    |
|-----------|-------------------|
| 1.0.8     | - Fixed a bug causing puzzle solution to display incorrectly. |
|           | - Increased default spawn quantity from 40 --> 60, requires config reset (i.e delete and let regenerate) |
| 1.0.7     | - Removed ServerSync from ILRepack.targets |
| 1.0.6     | - Fixed a bug causing pickable items to not appear. If you see a log warning "Failed to find loot list with name UndergroundRuinsLoot1", then delete you warpalicious.Underground_Ruins.cfg file to reset it. |
| 1.0.5     | - Yaml formatting fix. |
| 1.0.4     | - Fixed an incorrect AddLocation method. |
| 1.0.3     | - Fixed a bug where item prefabs would fail to pupulate loot lists |
|           | - Replaced ServerSync with Jotunn SynchronizationManager to fix crossplay issues introduced in Valheim version 0.220.3 |
| 1.0.2     | - Fixed a bug where creatures and loot would not appear when dungeon was loaded, unloaded, and reloaded. |
| 1.0.1     | - Attempt to fix an issue with Russian language computers failing to parse YAML files. |
| 1.0.0     | - Initial Release |