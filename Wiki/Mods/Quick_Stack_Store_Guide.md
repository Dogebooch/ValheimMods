# Quick Stack Store Mod Guide

## Overview
The Quick Stack Store mod enhances Valheim's inventory management with advanced features for stacking, storing, sorting, and trashing items. This guide covers all the features and how to use them effectively.

## Key Features

### 1. Quick Stacking
**Purpose**: Automatically stack items from your inventory into nearby containers.

**How to Use**:
- **Hotkey**: `P` (default)
- **Button**: Look for the "Quick Stack" button in your inventory or containers
- **Range**: 10 units (configurable)

**Behavior**:
- Stacks items to the currently opened container or nearby containers
- Respects favorited items (won't stack favorited items)
- Can include hotkey bar items
- Shows result message after stacking

### 2. Quick Restocking
**Purpose**: Automatically restock consumables and ammo from nearby containers.

**How to Use**:
- **Hotkey**: `L` (default)
- **Button**: Look for the "Restock" button in your inventory or containers
- **Range**: 10 units (configurable)

**Behavior**:
- Only restocks ammo and consumables by default
- Can be configured to restock all items
- Respects favorited items
- Shows result message after restocking

### 3. Store All / Take All
**Purpose**: Quickly store or retrieve all items from containers.

**How to Use**:
- **Store All Button**: Available in containers
- **Take All Button**: Available in containers
- **Hotkeys**: Configurable (none set by default)

**Behavior**:
- Store All excludes favorited items
- Can include/exclude equipped items
- Can include/exclude hotkey bar items

### 4. Sorting
**Purpose**: Automatically sort inventory and containers.

**How to Use**:
- **Hotkey**: `O` (default)
- **Button**: Available in inventory and containers
- **Auto-sort**: Enabled for both inventory and containers on open

**Sort Criteria**:
- **Type** (default): Groups items by type
- **Internal Name**: Alphabetical by internal name
- **Translated Name**: Alphabetical by display name
- **Value**: By item value
- **Weight**: By item weight

**Features**:
- Merges stacks after sorting
- Leaves empty favorited slots empty
- Sorts in ascending order by default

### 5. Favoriting System
**Purpose**: Mark items and slots as favorites to protect them from automatic actions.

**How to Use**:
- **Hotkey**: Hold `Alt` (LeftAlt or RightAlt) + Left-click on item
- **Toggle Button**: Star button in inventory
- **Visual**: Yellow border around favorited items/slots

**Protection**:
- Favorited items won't be quick stacked
- Favorited items won't be stored with "Store All"
- Favorited items won't be sorted
- Favorited items won't be trashed

### 6. Trash System
**Purpose**: Mark items for deletion and manage auto-pickup.

**How to Flag Items for Trash**:
- **Hover over item** + **Click trash can**
- **Hold Alt** + **Left-click** on item
- **Use favorite toggle** + **Click trash can**

**How to Remove Trash Flags**:
- **Hold Alt** + **Left-click** trash flagged item again
- **Use favorite toggle** + **Click trash can** again

**Visual Indicators**:
- **Red border** around trash flagged items
- **Tooltip hint** showing trash status

**Auto-Pickup Prevention**:
- **Enabled**: Trash flagged items won't auto-pickup from world
- **Manual pickup**: Still possible with interact button

**Quick Trash**:
- **Click trash can** (while not holding anything) to delete all trash flagged items
- **Hotkey**: Configurable (none set by default)

## Hotkeys Reference

| Action | Default Hotkey | Description |
|--------|----------------|-------------|
| Quick Stack | `P` | Stack items to nearby containers |
| Quick Restock | `L` | Restock consumables from nearby containers |
| Sort | `O` | Sort inventory/containers |
| Trash Item | `Delete` | Trash currently held item |
| Favorite | `Alt` + Left-click | Toggle favorite on item |
| Trash Flag | `Alt` + Left-click | Toggle trash flag on item |

## Configuration Options

### General Settings
- **Use Top-Down Logic**: Whether to always put items in top row first
- **Controller Support**: Hardcoded controller bindings
- **Button Display**: Override all new UI elements

### Quick Stacking
- **Range**: How close containers need to be (default: 10 units)
- **Include Hotkey Bar**: Whether to include hotkey bar items
- **Trophy Handling**: Whether to stack trophies into same container

### Restocking
- **Range**: How close containers need to be (default: 10 units)
- **Only Ammo/Consumables**: Whether to restock only consumables
- **Only Favorited**: Whether to restock only favorited items
- **Stack Limits**: Custom limits for ammo, consumables, and general items

### Sorting
- **Auto-Sort**: When to automatically sort (Never, On Open, Both)
- **Criteria**: What to sort by (Type, Name, Value, Weight)
- **Merge Stacks**: Whether to merge stacks after sorting
- **Leave Empty Slots**: Whether to leave favorited slots empty

### Trashing
- **Auto-Pickup Prevention**: Whether trash flagged items auto-pickup
- **Trophy Trashing**: Whether to always consider trophies as trash
- **Confirmation Dialogs**: When to show confirmation dialogs

## Tips and Best Practices

### 1. Use Favoriting Strategically
- **Favorite important items** to prevent accidental stacking/storing
- **Favorite empty slots** to reserve space for specific items
- **Use different colors** to distinguish favorited items vs slots

### 2. Organize with Sorting
- **Set auto-sort to "Both"** for automatic organization
- **Use "Type" sorting** for logical grouping
- **Combine with favoriting** to maintain custom organization

### 3. Efficient Trash Management
- **Flag common trash items** to prevent auto-pickup
- **Use quick trash** to clean inventory quickly
- **Reset trash flags** if you change your mind about items

### 4. Container Management
- **Use "Store All"** for quick storage of materials
- **Use "Take All"** for quick retrieval
- **Combine with restocking** for consumable management

### 5. Multiplayer Considerations
- **Area stacking** requires Multi User Chest mod
- **Server sync** for area stacking/restocking settings
- **Container permissions** affect mod functionality

## Troubleshooting

### Common Issues

**Items not stacking**:
- Check if items are favorited
- Verify container is within range
- Ensure container allows stacking

**Auto-pickup not working**:
- Check if items are trash flagged
- Verify `PreventAutoPickupOfTrashFlaggedItems` setting
- Reset trash flagging data if needed

**Sorting not working**:
- Check auto-sort settings
- Verify sort criteria
- Ensure no conflicts with other mods

**Hotkeys not responding**:
- Check if hotkeys are overridden
- Verify `OverrideKeybindBehavior` setting
- Ensure no conflicts with other mods

### Reset Options

**Reset All Favoriting Data**:
- Set `ResetAllFavoritingData = YesDeleteAllMyFavoritingData`
- This clears all favorites and trash flags
- Automatically resets to `No` after clearing

**Reset to Default**:
- Set `ConfigTemplate = ResetToDefault`
- This resets all settings to default values
- Does not affect custom keybinds

## Advanced Configuration

### Custom Keybinds
All hotkeys can be customized in the configuration file:
- `QuickStackKeybind`
- `RestockKeybind`
- `SortKeybind`
- `TrashKeybind`
- `QuickTrashKeybind`
- `StoreAllKeybind`
- `TakeAllKeybind`

### Container Behavior
- **Physical vs Non-Physical**: Different rules for different container types
- **Player-built vs World**: Different permissions for different containers
- **Multiplayer**: Special considerations for multiplayer servers

### Performance Settings
- **Debug Logs**: Enable for troubleshooting
- **Sound/Visual Suppression**: Disable container opening effects
- **Speed Tests**: Enable for performance monitoring

---

*This guide covers the Quick Stack Store mod v1.4.13. For the latest information, check the mod's official documentation.*
