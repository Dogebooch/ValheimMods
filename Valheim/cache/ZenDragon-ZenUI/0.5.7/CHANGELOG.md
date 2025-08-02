v0.5.7
- add config option: show craftable items together at the top of the list (on by default)

v0.5.6
- improve visual distinction when item can not be crafted: made the red X larger and centered it over the item's icon.

v0.5.5
- remove admin requirement for biome notification config option.

v0.5.4
- add a stronger visual distinction for items that you do not have resources to craft yet on the crafting panel: Red X and darker tint to uncraftable items.

v0.5.3
- cleanup references to food panels on logout. 

v0.5.2
- fix: was not displaying the socket tab correctly in Jewelcrafting's Gemcutter table.

v0.5.1
- fix: when applying search filter to item recipe requirements: exclude resources with zero amount requirement from the results.

v0.5.0
- added search filter to crafting UI
- changed config names related to crafting, check your configs.

v0.4.10
- fix: handle other mods adding their own custom tabs.

v0.4.9
- fix: sorting order was incorrect when dealing with multiple items of the same name but different amounts.  before: amount/name, now: name/amount.
- fix: add notice to the item's tooltip for items which only require one ingredient.

v0.4.8
- fix: case where a modded item with a non-vanilla ItemType could not be explicitly assigned to a different group via the configs.

v0.4.7
- handle case where mods add multiple recipes to craft the same item.

v0.4.6
- epic loot compatibility fix.

v0.4.5
- bugfix: error would occur when the config for crafting group item assignment was changed from default to blank.
- no longer requires game restart for changes to crafting groups to take effect.

v0.4.4
- added a "magic" crafting group category. 
- added config options for explicitly mapping items to groups allowing mod authors and end users to override the default groupings on a per item basis.

v0.4.3
- revert changes that were trying to fix epic loot.  better they are handled within epic loot itself. I have, reached out to the devs and will coordinate a fix.

v0.4.2
- change config option: Enable Crafting Panel no longer requires admin.  Does not need to be installed on server to change the value.
- Fix for epic loot compatibility.  The UI in epic loot was not displaying some text on certain dialogs.

v0.4.1
- added a new crafting menu which lists items by icon instead of name.

v0.3.2
- add feature: colored food bars. food icons tint to the color of the food type you ate. Health, Stamina, Eitr.

v0.3.1
- set default config option panel slide animations: enabled (same as vanilla)

v0.3.0
- add option to auto open skills panel
- add option to enable/disable the panel slide animation

v0.2.8
- added a finer grain of control to Biome notifications config options.

v0.2.7
- minor bugfix to biome notifications displaying twice under rare edge cases.

v0.2.6
- update readme, no code changes.

v0.2.5
- add biome notifications when changing biome via teleport or resurrection or first login.

v0.2.4
- update for Zen.ModLib v1.1.0

v0.2.3
- fixed config sync

v0.2.2
- fix fishing bait not displaying correctly in the hotbar.

v0.2.1
- removed BepInEx from dependency, Zen.ModLib handles it.

v0.2.0
- use Zen.ModLib

v0.1.6
- add a config option for the rotation mentioned in v0.1.5

v0.1.5
- tone down the durability bar color brightness and added config options.
- The durability bar was turning gray at 25% remaining.  Now stays red until broken at 0%.
- rotated item quality symbols 90 degrees and added support for modded items up to level 8 soft cap with dots & stars. Then beyond level 8 there is no limit as you can add extra symbols via config.

v0.1.4
- update logging and config subsystem.

v0.1.3
- UPDATE FOR VALHEIM v0.220.3
- Removed the patch for hiding the ship hud when Ctrl+F3 pressed because the bug was fixed in vanilla.

v0.1.2 
- Added option to hide ship controls wheel when main HUD is hidden.