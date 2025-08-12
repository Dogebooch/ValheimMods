### Task
Modify `BepInEx/config/WackyItemRequiresSkillLevel.yml` to add or update Blacksmithing level requirements for item crafting.

### Inputs you provide
- **ITEM_PREFAB**: exact prefab ID (e.g., `HammerBlackMetal`) - You can get prefabs from VNEI-Export
- **LEVEL**: required Blacksmithing level
- **BLOCK_EQUIP**: `true`/`false` (default `false`)
- **EPICMMO**: `true`/`false` (default `false`)

### YAML format (exact)
```yaml
- PrefabName: <ITEM_PREFAB>
  Requirements:
    - Skill: Blacksmithing
      Level: <LEVEL>
      BlockCraft: true
      BlockEquip: <BLOCK_EQUIP>
      EpicMMO: <EPICMMO>
      ExhibitionName: "Requires Blacksmithing <LEVEL>"
```

### Rules
- **If item exists**:
  - Replace existing `Skill: Blacksmithing` block with new values.
  - If no Blacksmithing block exists, append it to `Requirements`.
- **Do not duplicate entries**.
- **Preserve YAML order, indentation, and comments**.
- **Default** to blocking crafting only (`BlockCraft: true`).