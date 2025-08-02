v1.1.24
- fix: translation loading error that was causing some translations to not load correctly.

v1.1.23
- add a config option to swap Mouse3 and Mouse4 buttons because Valheim maps them inverted.

v1.1.22
- Move Piece highlighting code from ZenSign into this shared lib so that other ZenMods can use it, like ZenDistributor.

v1.1.21
- add InventoryGrid.GetHoveredItem

v1.1.20
- add TryAddItem function to InventoryExt that returns the added item if successful.
- add capability to KeyHint management to alter key hint label
- fix: in string handling with ProperCase() where it would error on empty string.
- fix: gamepad map button returned to the default behavior.
- add: vanilla fix for handling TextInput when the inventory is open.
- add: universal TextPrompt input wrapper around TextInput
- rework gamepad remap to make room for ZenMap's portable maps and return of the dedicated map button.  If you use gamepad, check the button map after this update.  A few minor changes have been applied if you use ZenMods which require gamepad remap.
- add function for applying custom texture to item prefabs.

v1.1.19
- refactor some internal functions and added additional utilities relating to inventory item lookup.

v1.1.18
- add UI.CleanImageTransparency for quick access to shader for cleanup of icon transparencies.

v1.1.17
- removed write operations to avoid Thunderstore automated checks from triggering false-positives.

v1.1.16
- added utility functions for sprite handling.

v1.1.15
- extra checks for data validation. some mods really mangle items and forget to add basic things like ItemDrop components.

v1.1.14
- added an option for automatic sanitization of item and recipe data on game start. this handles cases where mods do not properly index their items into all ObjectDB indexes.
- config option to disable sanitization if desired.

v1.1.13
- improved internal logging mechanism.

v1.1.12
- fixed a null ref warning preventing some configs from loading when checking if ConfigManager is installed.

v1.1.11
- fix vanilla: when in DebugFly mode give the player a nicer animation state than the default which is to make them look like they are standing on solid ground, which is goofy looking.
- fix vanilla: correct for missing space at the end of the translation string: `$msg_turretotherammo`
- moved general purpose UI meter creation code out of `ZenHoverItem` into this lib so that other ZenMods can use it.

v1.1.10
- added helper time conversion functions: RealToGameTime and RealToGameTimeFuel

v1.1.9
- internal changes for making console command prefixes public so that other ZenMods can read them.  Nothing major.

v1.1.8
- added a config option to control the threshold before warnings get logged about potential performance impacts from mods like ConfigWatcher which can cause excessive IO thrashing from constantly reloading your config files.

v1.1.7
- replaced calls to GUIManager.IsHeadless() with internal implementation ModLib.IsHeadless because JVL and Jewelcrafting were fighting when GUIManager's static constructor would cause PrefabManager to initialize assets and that triggered the softref system which would somehow cause errors whenever Jewelcrafting was installed.

v1.1.6
- added check if ConfigurationManager is installed. Pause detecting config file IO thrashing if the ConfigurationManager window is open, resume detection once it closes.

v1.1.5
- added a fix for a bug in vanilla where CraftingStations and CookingStations were not correctly checking if the fire was actually lit under them.

v1.1.4
- added Localize() extension that takes params.
- require version matching at Patch level instead of Minor.  Everyone must run the same exact version. Too complicated to debug otherwise.

v1.1.3
- add compatibility for Seasons mod in fireplace fuel burn rate calculations.

v1.1.2
- Changed remap of gamepad sit from Select to X + Alt Function to free up room for ZenConstruction to use Select as the dedicated Hammer button.

v1.1.1
- Add method: UI.InsertInteractAlt

v1.1.0
- improved config sync handling for prefabs and fallback for single player mode.
- refactored internal code
- add a default constructor to StringList
- code cleanup: remove some public methods, breaks backwards compatibility with some ZenMods, update all ZenMods.

v1.0.5
- add capability to automatically sync config changes for custom crafting items.

v1.0.4
- internal code cleanup

v1.0.3
- relocated input refresh method to base class, no major changes.

v1.0.2
- fix minor logging issue.

v1.0.1
- add config option to force gamepad remap if desired.

v1.0.0
- initial release