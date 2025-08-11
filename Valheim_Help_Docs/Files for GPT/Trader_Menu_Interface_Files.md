# Trader Menu & Interface Affecting Files

This document provides a comprehensive overview of all configuration files that affect trader menus and interfaces in the Valheim modded setup.

## 🏪 Primary Trader Mods

### 1. Traders Extended (`shudnal.TradersExtended.cfg`)
**Purpose**: Enhances vanilla traders (Haldor, Hildir) with additional features

**Menu Effects**:
- Buyback system with colored items
- Item discovery requirements
- Flexible pricing based on trader coin amounts
- Repair functionality
- Fixed GUI positioning
- Hide equipped/hotbar items
- Quality multipliers for pricing

**File Location**: `Valheim/profiles/Dogeheim_Player/BepInEx/config/shudnal.TradersExtended.cfg`

### 2. More World Traders (`warpalicious.More_World_Traders.cfg`)
**Purpose**: Adds new trader locations throughout the world

**Menu Effects**:
- New trader prefabs and locations
- Custom trader integration with Traders Extended
- Spawn quantities and trader types

**File Location**: `Valheim/profiles/Dogeheim_Player/BepInEx/config/warpalicious.More_World_Traders.cfg`

## 🎨 UI/Interface Mods

### 3. ZenUI (`ZenDragon.ZenUI.cfg`)
**Purpose**: UI customization and improvements

**Menu Effects**:
- Color schemes for active items
- Crafting group assignments
- Item categorization
- Background colors and visual styling

**File Location**: `Valheim/profiles/Dogeheim_Player/BepInEx/config/ZenDragon.ZenUI.cfg`

### 4. Configuration Manager (`com.bepis.bepinex.configurationmanager.cfg`)
**Purpose**: In-game configuration interface

**Menu Effects**:
- F1 menu for mod configuration
- Color schemes for config windows
- Window sizing and positioning
- Font sizes and styling

**File Location**: `Valheim/profiles/Dogeheim_Player/BepInEx/config/com.bepis.bepinex.configurationmanager.cfg`

## 📦 Item/Equipment Mods with Trader Integration

### 5. Magic Revamp (`blacks7ar.MagicRevamp.cfg`)
**Trader Features**: Magic items can be sold at traders
**Menu Effects**: Adds magic items to trader inventories

**File Location**: `Valheim/profiles/Dogeheim_Player/BepInEx/config/blacks7ar.MagicRevamp.cfg`

### 6. Cooking Additions (`blacks7ar.CookingAdditions.cfg`)
**Trader Features**: Food items can be sold at traders
**Menu Effects**: Adds food items to trader inventories

**File Location**: `Valheim/profiles/Dogeheim_Player/BepInEx/config/blacks7ar.CookingAdditions.cfg`

### 7. Potion Plus (`com.odinplus.potionsplus.cfg`)
**Trader Features**: Potions can be sold at traders
**Menu Effects**: Adds potions to trader inventories

**File Location**: `Valheim/profiles/Dogeheim_Player/BepInEx/config/com.odinplus.potionsplus.cfg`

### 8. Odin's Kingdom (`odinplus.plugins.odinskingdom.cfg`)
**Trader Features**: Kingdom items can be sold at traders
**Menu Effects**: Adds kingdom items to trader inventories

**File Location**: `Valheim/profiles/Dogeheim_Player/BepInEx/config/odinplus.plugins.odinskingdom.cfg`

### 9. Southsil Armor (`southsil.SouthsilArmor.cfg`)
**Trader Features**: Armor pieces can be sold at traders
**Menu Effects**: Adds armor to trader inventories

**File Location**: `Valheim/profiles/Dogeheim_Player/BepInEx/config/southsil.SouthsilArmor.cfg`

### 10. Odin Ship Plus (`marlthon.OdinShipPlus.cfg`)
**Trader Features**: Ship items can be sold at traders
**Menu Effects**: Adds ship components to trader inventories

**File Location**: `Valheim/profiles/Dogeheim_Player/BepInEx/config/marlthon.OdinShipPlus.cfg`

### 11. Epic MMO System (`WackyMole.EpicMMOSystem.cfg`)
**Trader Features**: MMO items can be sold at traders
**Menu Effects**: Adds MMO progression items to trader inventories

**File Location**: `Valheim/profiles/Dogeheim_Player/BepInEx/config/WackyMole.EpicMMOSystem.cfg`

### 12. Backpacks (`org.bepinex.plugins.backpacks.cfg`)
**Trader Features**: Backpacks can be sold at traders
**Menu Effects**: Adds backpacks to trader inventories

**File Location**: `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.backpacks.cfg`

## 🌍 World/Content Mods

### 13. Warpalicious World Packs (Multiple .cfg files)
**Purpose**: Add world content that may include trader-related items

**Files**:
- `warpalicious.Meadows_Pack_1.cfg` - Meadows biome content
- `warpalicious.Meadows_Pack_2.cfg` - Additional meadows content
- `warpalicious.Blackforest_Pack_2.cfg` - Black Forest biome content
- `warpalicious.MWL_Blackforest_Pack_1.cfg` - More World Locations Black Forest
- `warpalicious.Plains_Pack_1.cfg` - Plains biome content
- `warpalicious.Mountains_Pack_1.cfg` - Mountains biome content
- `warpalicious.Mistlands_Pack_1.cfg` - Mistlands biome content
- `warpalicious.Swamp_Pack_1.cfg` - Swamp biome content
- `warpalicious.AshlandsPack1.cfg` - Ashlands biome content
- `warpalicious.Adventure_Map_Pack_1.cfg` - Adventure map content
- `warpalicious.Forbidden_Catacombs.cfg` - Catacombs content
- `warpalicious.Underground_Ruins.cfg` - Underground ruins content

**Menu Effects**: May add items to trader inventories

## 🔧 Supporting Files

### 14. BepInEx Configuration (`BepInEx.cfg`)
**Purpose**: Core mod framework
**Menu Effects**: Affects overall mod loading and UI behavior

**File Location**: `Valheim/profiles/Dogeheim_Player/BepInEx/config/BepInEx.cfg`

### 15. HookGenPatcher (`HookGenPatcher.cfg`)
**Purpose**: Mod compatibility patcher
**Menu Effects**: May affect trader menu stability

**File Location**: `Valheim/profiles/Dogeheim_Player/BepInEx/config/HookGenPatcher.cfg`

## 📋 Summary of Menu Effects

### Direct Trader Menu Changes:
- **Traders Extended**: Buyback system, pricing, repair, GUI positioning
- **More World Traders**: New trader locations and types
- **ZenUI**: Visual styling and item categorization
- **Configuration Manager**: F1 config menu

### Trader Inventory Changes:
- **Magic Revamp**: Magic items
- **Cooking Additions**: Food items
- **Potion Plus**: Potions
- **Odin's Kingdom**: Kingdom items
- **Southsil Armor**: Armor pieces
- **Odin Ship Plus**: Ship components
- **Epic MMO System**: MMO items
- **Backpacks**: Backpack items

### Visual/Interface Changes:
- **ZenUI**: Colors, grouping, categorization
- **Configuration Manager**: Config menu styling
- **Traders Extended**: Buyback colors, GUI positioning

## 🚀 GitHub Integration

All these files have been added to the Git repository and are ready for commit and push to GitHub. The files are organized in the following structure:

```
Valheim/
└── profiles/
    └── Dogeheim_Player/
        └── BepInEx/
            └── config/
                ├── shudnal.TradersExtended.cfg
                ├── warpalicious.More_World_Traders.cfg
                ├── ZenDragon.ZenUI.cfg
                ├── com.bepis.bepinex.configurationmanager.cfg
                ├── blacks7ar.MagicRevamp.cfg
                ├── blacks7ar.CookingAdditions.cfg
                ├── com.odinplus.potionsplus.cfg
                ├── odinplus.plugins.odinskingdom.cfg
                ├── southsil.SouthsilArmor.cfg
                ├── marlthon.OdinShipPlus.cfg
                ├── WackyMole.EpicMMOSystem.cfg
                ├── org.bepinex.plugins.backpacks.cfg
                ├── warpalicious.*.cfg (12 world pack files)
                ├── BepInEx.cfg
                └── HookGenPatcher.cfg
```

## 📝 Notes

- All configuration files are in the `.cfg` format
- Files are located in the BepInEx config directory for the Dogeheim_Player profile
- These files control trader menu behavior, inventory items, and UI appearance
- Changes to these files will affect trader functionality in-game
- The files are now tracked by Git and ready for version control
