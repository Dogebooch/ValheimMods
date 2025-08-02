# ZenUI

Lightweight helpful UI additions.

- Improved Crafting Panel. Visual organization with grouping, sorting, and filtering.
- Remove lens dirt! Clear view of the game world.
- Item level is displayed with symbols instead of a number, no item level limit if you use mods to alter the limit.
- Colored durability bars, configurable.
- Ammo remaining displayed on the hotbar
- Biome notifications when spawning or teleporting and other key moments.
- Auto open the skills panel.
- Disable sliding animations.
- Colored food bars based on the food you ate: Health, Stamina, Eitr, or Balanced.

### Improved Crafting Panel
<img alt="Crafting UI: Light" width="300" src="https://github.com/ZenDragonX/ZenMods_Valheim/blob/main/screenshots/ZenUI/crafting.jpg?raw=true">

<img alt="Crafting UI: Dark" width="300" src="https://github.com/ZenDragonX/ZenMods_Valheim/blob/main/screenshots/ZenUI/crafting2.jpg?raw=true">


### Colored Durability Bars & Level Stars
![Screenshot Inventory Colors](https://github.com/ZenDragonX/ZenMods_Valheim/blob/main/screenshots/ZenUI/inventory.jpg?raw=true)

### Ammo Remaining
![Screenshot Ammo](https://github.com/ZenDragonX/ZenMods_Valheim/blob/main/screenshots/ZenUI/ammo.jpg?raw=true)

### Colored Food Bars
![Colored Food Bars](https://github.com/ZenDragonX/ZenMods_Valheim/blob/main/screenshots/ZenUI/foodbars.jpg?raw=true)

## Client / Server Requirements

NOTE: Technically it is *not required* on the server. However, if it is installed on the server then it will force all clients to have it installed as well. This is to enable two modes of usage:
1. Dedicated server admins can put the mod on the server to enforce all clients to have the mod installed and sync admin configs.
2. Trusted friends can agree to run the same mods and connect through a vanilla dedicated server with no enforcement but with locked admin configs.

## Client Only

This mod operates entirely client side. That means you can connect to any vanilla server with this mod installed.  Other players do not need to have the mod installed.

NOTE: If you host a game session with this mod installed, then it will be considered to be installed on the server since your session is the server. Therefore, all clients will be required to have it.  If you don't want to require all players to have this mod, then you will need to host your game in a dedicated server.  You can download and run the Valheim Dedicated Server from Steam or host one in the cloud.

## Improve Your Experience

### [CORE MODS](https://thunderstore.io/c/valheim/p/ZenDragon/ZenModpack_CORE/)

The full collection of all Zen MODS:

- Radically improved QoL
- Incredible performance
- Pre-configured
- 100% Gamepad support
- Spectacularly immersive

Enjoy!


## Sample Config File

```
## Settings file was created by plugin ZenUI v0.4.1
## Plugin GUID: ZenDragon.ZenUI

[Active Item]

## [Admin] Background color when the item is activated (equipped / selected)
## Vanilla blue color: RGBA(0.376, 0.660, 0.897, 0.761)
## Menu orange color: RGBA(0.757, 0.504, 0.184, 1.000)
# Setting type: Color
# Default value: C1812FFF
Activated Color = C1812FFF

## [Admin] Background color when the item is activated on the hotbar.
## Vanilla blue color: RGBA(0.376, 0.660, 0.897, 0.761)
## Menu orange color: RGBA(0.757, 0.504, 0.184, 1.000)
# Setting type: Color
# Default value: 5959598C
Activated Color - Hotbar = 5959598C

[General]

## Replace the vanilla crafting panel with a visual icon style with sorting and grouping. (vanilla: false)
## [logout required for changes to take effect]
# Setting type: Boolean
# Default value: true
Enable Crafting Panel = true

## [Admin] Show the biome notification on key events.  (Vanilla: 0)
## Player login, ressurecetion, after teleport, first discovery, etc.
## Turning this off will not disable first discovery notifications.
## NOTE: Using this with BiomeObserver mod is probably overkill.
# Setting type: BiomeNoticeType
# Default value: PlayerSpawn, Teleport
# Acceptable values: PlayerSpawn, Teleport
# Multiple values can be set at the same time by separating them with , (e.g. Debug, Warning)
Show Biome Notification = PlayerSpawn, Teleport

## Hide the modded text on the title screen.
## [restart required]
# Setting type: Boolean
# Default value: false
Hide Modded Text On Title Screen = false

## [Admin] When true an icon and count appears on the hotbar with ammo type and count.
## [logout required]
# Setting type: Boolean
# Default value: true
Enable Ammo Count = true

## [Admin] Remove the lens dirt from the camera.
## [logout required]
# Setting type: Boolean
# Default value: true
Remove Lens Dirt = true

## Automatically open the skills panel when the inventory is opened. (vanilla: false)
## [logout required]
# Setting type: Boolean
# Default value: false
Auto Open Skills Panel = false

## Enable the panel slide animation (vanilla: true)
# Setting type: Boolean
# Default value: true
Enable Slide Animation = true

## Colored food bars. (vanilla: false)
## Tint the background of the food you ate based on the main property of the food: Health = red, stamina = yellow, blue = eitr
# Setting type: Boolean
# Default value: true
Colored Food Bars = true

## [Admin] Comma separated list of regex patterns. Match against the translation keys. 
## Matched keys have their translations stripped of rich text.
## Some mods add rich text tags like <color> to their translations.
## In order to provide a consistant UI theme you can remove those tags from the translations of matched keys.
## If you don't want to remove any tags then leave the list empty. (Default is to remove the rich text on RtD mods)
## If you need help with regex patterns then check out https://regex101.com/ or ask an AI.
# Setting type: StringList
# Default value: _RtD$
Remove Rich Text From Translations = _RtD$

[Item Durability Bars]

## [Admin] Durability bar color when durability is good
# Setting type: Color
# Default value: 00FF0033
Durability Good = 00FF0033

## [Admin] Durability bar color when durability is worn
# Setting type: Color
# Default value: FFEB0480
Durability Worn = FFEB0480

## [Admin] Durability bar color when durability is at risk of breaking
# Setting type: Color
# Default value: FF0000B2
Durability At Risk = FF0000B2

## [Admin] Durability bar color when item is broken
# Setting type: Color
# Default value: 808080FF
Durability Broken = 808080FF

[Item Quality Symbols]

## [Admin] Item quality is shown as symbols instead of numbers on the inventory grid.
# Setting type: Boolean
# Default value: true
Show Quality As Symbols = true

## [Admin] The quality symbols are rotated 90 degrees to display them vertically instead of horizontally. This is only used if Show Quality As Symbols is enabled.
# Setting type: Boolean
# Default value: false
Rotate Symbols 90 Degrees = false

## [Admin] Color of the item quality symbols
# Setting type: Color
# Default value: FFFFAA99
Symbol Color = FFFFAA99

## [Admin] The sequence of symbols used to display the quality level. The first symbol is always the dots and can not be changed.
## Each symbol adds 4 levels. Preconfigured with 1 symobl so 8 levels supported: Vanilla 4 + 1 symbol x 4 more levels.
## So if you wanted to add 8 more levels for a total of 12 levels (4 + 8), you would add 2 more symbols to the end of the sequence.
## Here are some extra symbols you can try.  Not all unicode works, These are known to work: ★✽◈⚡▲
## Example: ★▲ would be 4 vanilla levels + 4 more levels for ★ + 4 more levels for ▲
## NOTE: If your item level exceeds this value it will be displayed as a number instead of a symbol.
# Setting type: String
# Default value: ★
Extra Level Symbols = ★

```

---
#### Like My Mods? Donations Welcome

`Bitcoin`

<img alt="Donation QR" src="https://github.com/ZenDragonX/ZenMods_Valheim/blob/main/BTC_QR.png?raw=true" width=180>
