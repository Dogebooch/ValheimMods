# RelicHeim Configuration Changes Report

Generated on: 2025-08-15 12:30:58

This report shows **only the changes** made to configuration files compared to the base RelicHeim installation.
Files that are identical to the backup or have no backup file are not shown.

For each modified file, you'll see:
- **Key Changes**: Specific configuration values that changed (old → new)
- **Full Diff**: Complete diff showing all line-by-line changes

## Summary


- **Total Changed Files**: 70
- **Modified**: 67 
- **Errors**: 0
- **Info Items**: 3

## Detailed Changes

### Azumatt Mods

*Files in this category with changes from RelicHeim backup:*

#### Azumatt.AzuCraftyBoxes.cfg

**Status**: Modified

**Summary**: +15, -51 changes

**Key Changes**:

**Total changes**: 66 (showing top 8)

• **rk_crate**: `` *(removed)*
• **rk_crate2**: `` *(removed)*
• **1 - General.Mod Enabled**: `On` *(new setting)*
• **1 - General.Output Debug Logs**: `Off` *(new setting)*
• **1 - General.Lock Configuration**: `On` *(new setting)*
• **1 - General.Prevent Pulling Format**: `<size=30><color=#ffffff>{0}</color></size>\n<size=25>{1}</size>` *(new setting)*
• **1 - General.Prevent Pulling Message**: `On` *(new setting)*
• **1 - General.Prevent Pulling Status**: `On` *(new setting)*
• ... and 58 more changes

**Full Diff**:

```diff
--- backup/Azumatt.AzuCraftyBoxes.cfg+++ current/Azumatt.AzuCraftyBoxes.cfg@@ -1,338 +1,92 @@-# Below you can find example groups. Groups are used to exclude or includeOverride quickly. They are reusable lists! 
-# Please note that some of these groups/container limitations are kinda pointless but are here for example.
-# Make sure to follow the format of the example below. If you have any questions, please ask in my discord.
+## Settings file was created by plugin AzuCraftyBoxes v1.8.4
+## Plugin GUID: Azumatt.AzuCraftyBoxes
 
-# Full vanilla prefab name list: https://valheim-modding.github.io/Jotunn/data/prefabs/prefab-list.html
-# Item prefab name list: https://valheim-modding.github.io/Jotunn/data/objects/item-list.html
+[1 - General]
 
-# There are several predefined groups set up for you that are not listed. You can use these just like you would any group you create yourself.
-# These are the "All", "Food", "Potion", "Fish", "Swords", "Bows", "Crossbows", "Axes", "Clubs", "Knives", "Pickaxes", "Polearms", "Spears", "Equipment", "Boss Trophy", "Trophy", "Crops", "Seeds", "Ores", "Metals", and "Woods" groups.
-# The criteria for these groups are as follows:
-# groups:
-#   Food:
-#     - Criteria: Both of the following properties must have a value greater than 0.0 on the sharedData property of the ItemDrop script:
-#         - food
-#         - foodStamina
-#   Potion:
-#     - Criteria: The following properties must meet the specified conditions on the sharedData property of the ItemDrop script:
-#         - food > 0.0
-#         - foodStamina == 0.0
-#   Fish:
-#     - itemType: Fish
-#   Swords, Bows, Crossbows, Axes, Clubs, Knives, Pickaxes, Polearms, Spears:
-#     - itemType: OneHandedWeapon, TwoHandedWeapon, TwoHandedWeaponLeft, Bow
-#     - Criteria: Items in these groups have a specific skillType on the sharedData property of the ItemDrop script. Each group corresponds to the skillType as follows:
-#         - Swords: skillType == Skills.SkillType.Swords
-#         - Bows: skillType == Skills.SkillType.Bows
-#         - Crossbows: skillType == Skills.SkillType.Crossbows
-#         - Axes: skillType == Skills.SkillType.Axes
-#         - Clubs: skillType == Skills.SkillType.Clubs
-#         - Knives: skillType == Skills.SkillType.Knives
-#         - Pickaxes: skillType == Skills.SkillType.Pickaxes
-#         - Polearms: skillType == Skills.SkillType.Polearms
-#         - Spears: skillType == Skills.SkillType.Spears
-#            Example:   An item with itemType set to OneHandedWeapon and skillType set to Skills.SkillType.Swords would belong to the Swords group.
-#   Equipment:
-#     - itemType: Torch
-#   Boss Trophy:
-#     - itemType: Trophie
-#     - Criteria: sharedData.m_name ends with any of the following boss names:
-#         - eikthyr, elder, bonemass, dragonqueen, goblinking, SeekerQueen
-#   Trophy:
-#     - itemType: Trophie
-#     - Criteria: sharedData.m_name does not end with any boss names
-#   Crops:
-#     - itemType: Material
-#     - Criteria: Can be cultivated and grown into a pickable object with an amount greater than 1
-#   Seeds:
-#     - itemType: Material
-#     - Criteria: Can be cultivated and grown into a pickable object with an amount equal to 1
-#   Ores:
-#     - itemType: Material
-#     - Criteria: Can be processed by any of the following smelters:
-#         - smelter
-#         - blastfurnace
-#   Metals:
-#     - itemType: Material
-#     - Criteria: Is the result of processing an ore in any of the following smelters:
-#         - smelter
-#         - blastfurnace
-#   Woods:
-#     - itemType: Material
-#     - Criteria: Can be processed by the charcoal_kiln smelter
-#   All:
-#     - Criteria: Item has an ItemDrop script and all needed fields are populated. (all items)
+## If on, the configuration is locked and can be changed by server admins only. [Synced with Server]
+# Setting type: Toggle
+# Default value: On
+# Acceptable values: Off, On
+Lock Configuration = On
 
+## If off, everything in the mod will not run. This is useful if you want to disable the mod without uninstalling it. [Synced with Server]
+# Setting type: Toggle
+# Default value: On
+# Acceptable values: Off, On
+Mod Enabled = On
 
+## If on, the debug logs will be displayed in the BepInEx console window when BepInEx debugging is enabled. [Synced with Server]
+# Setting type: Toggle
+# Default value: Off
+# Acceptable values: Off, On
+Output Debug Logs = Off
 
+## If on, a message will be displayed above the player's head when the prevention pulling logic is toggled using the keybind. [Not Synced with Server]
+# Setting type: Toggle
+# Default value: On
+# Acceptable values: Off, On
+Prevent Pulling Message = On
 
-groups:
-  Armor: # Group name
-    - ArmorBronzeChest # Item prefab name, note that this is case sensitive and must be the prefab name
-    - ArmorBronzeLegs
-    - ArmorCarapaceChest
-    - ArmorCarapaceLegs
-    - ArmorFenringChest
-    - ArmorFenringLegs
-    - ArmorIronChest
-    - ArmorIronLegs
-    - ArmorLeatherChest
-    - ArmorLeatherLegs
-    - ArmorMageChest
-    - ArmorMageLegs
-    - ArmorPaddedCuirass
-    - ArmorPaddedGreaves
-    - ArmorRagsChest
-    - ArmorRagsLegs
-    - ArmorRootChest
-    - ArmorRootLegs
-    - ArmorTrollLeatherChest
-    - ArmorTrollLeatherLegs
-    - ArmorWolfChest
-    - ArmorWolfLegs
-  Arrows:
-    - ArrowBronze
-    - ArrowCarapace
-    - ArrowFire
-    - ArrowFlint
-    - ArrowFrost
-    - ArrowIron
-    - ArrowNeedle
-    - ArrowObsidian
-    - ArrowPoison
-    - ArrowSilver
-    - ArrowWood
-    - draugr_arrow
-  Tier 2 Items:
-    - Bronze
-    - PickaxeBronze
-    - ArmorBronzeChest
-    - ArmorBrozeLeggings
+## String format for the message displayed when the prevention pulling logic is toggled. {0} is replaced by the message, and {1} is replaced by the on/off status. Set to nothing to leave it as default. [Not Synced with Server]
+# Setting type: String
+# Default value: <size=30><color=#ffffff>{0}</color></size>\n<size=25>{1}</size>
+Prevent Pulling Format = <size=30><color=#ffffff>{0}</color></size>\n<size=25>{1}</size>
 
+## If on, the status effect will be displayed when you cannot pull from containers. [Not Synced with Server]
+# Setting type: Toggle
+# Default value: On
+# Acceptable values: Off, On
+Prevent Pulling Status = On
 
-# By default, if you don't specify a container below, it will be considered as you want to allow pulling all objects for pulling from it.
-# If you are having issues with a container, please make sure you have the full prefab name of the container. Additionally, make sure you have exclude or includeOverride set up correctly.
-# Worst case you can define a container like this. This will allow everything to be pulled from the container.
-# rk_barrel:  
-#  includeOverride: []
+[2 - CraftyBoxes]
 
-## Please note that the below containers are just examples. You can add as many containers as you want.
-## If you want to add a new container, just copy and paste the below example and change the name of the container to the prefab name of the container you want to add.
-## The values are set up to include everything by using the includeOverride (aside from things that aren't really a part of vanilla recipes, like Swords or Bows). 
-## This is to give you examples on how it's done, but still allow everything to be pulled from the container.
+## The maximum range from which to pull items from. [Synced with Server]
+# Setting type: Single
+# Default value: 20
+Container Range = 20
 
-piece_chest:
-  exclude: # Exclude these items from being able to be pulled from the container
-    #- Food # Exclude all in group
-    - PickaxeBronze # Allow prefab names as well, in this case we will use something that isn't a food
-  includeOverride:
-   # - Food # This would not work, you cannot includeOverride a group that is excluded. You can only override prefabs from that group.
-    - PickaxeBronze # You can however, be weird, and override a prefab name you have excluded.
+## * If on, leaves one item in the chest when pulling from it, so that you are able to pull from it again and store items more easily with other mods. (Such as AzuAutoStore or QuickStackStore). If off, it will pull all items from the chest. [Synced with Server]
+# Setting type: Toggle
+# Default value: Off
+# Acceptable values: Off, On
+Leave One Item = Off
 
-# It's highly unlikely that you will need the armor, swords, bows, etc. groups below. These are just in case you want to use them. 
-# They were also easy ways for me to show you how to use the groups without actually excluding something you might want to always pull by default.
+## String used to show required and available resources. {0} is replaced by how much is available, and {1} is replaced by how much is required. Set to nothing to leave it as default. [Not Synced with Server]
+# Setting type: String
+# Default value: {0}/{1}
+ResourceCostString = {0}/{1}
 
-piece_chest_wood:
-  exclude:
-    - Swords # Exclude all in group
-    - Tier 2 Items # Exclude all in group
-    - Bows # Exclude all in group
-  includeOverride: # If the item is in the groups above, say, you were using a predefined group but want to override just one item to be ignored and allow pulling it
-    - BowFineWood
-    - Wood
-    - Bronze
+## Resource amounts will flash to this colour when coming from containers [Not Synced with Server]
+# Setting type: Color
+# Default value: FFEB04FF
+FlashColor = FFEB04FF
 
-piece_chest_private:
-  exclude:
-    - All # Exclude everything
+## Resource amounts will flash from this colour when coming from containers (set both colors to the same color for no flashing) [Not Synced with Server]
+# Setting type: Color
+# Default value: FFFFFFFF
+UnFlashColor = FFFFFFFF
 
-piece_chest_blackmetal:
-  exclude:
-    - Swords # Exclude all in group
-    - Tier 2 Items # Exclude all in group
-    - Bows # Exclude all in group
-  includeOverride: # If the item is in the groups above, say, you were using a predefined group but want to override just one item to be ignored and allow pulling it
-    - BowFineWood
-    - Wood
-    - Bronze
+## The color of the build panel's count of pieces you can build [Not Synced with Server]
+# Setting type: Color
+# Default value: 00FF00FF
+Can Build Color = 00FF00FF
 
-rk_cabinet: # rk_ is typically the prefix for containers coming from RockerKitten's mods
-  exclude:
-    - Food
-  includeOverride:
-    - Food
+## The color of the build panel's count if you cannot build something [Not Synced with Server]
+# Setting type: Color
+# Default value: FF0000FF
+Cannot Build Color = FF0000FF
 
-rk_cabinet2:
-  exclude:
-    - Food
-  includeOverride:
-    - Food
+[3 - Keys]
 
-rk_barrel:
-  exclude:
-    - Armor
-    - Swords
+## Modifier key to pull all available fuel or ore when down. Use https://docs.unity3d.com/Manual/ConventionalGameInput.html [Not Synced with Server]
+# Setting type: KeyboardShortcut
+# Default value: LeftShift
+# Acceptable values: None, Backspace, Tab, Clear, Return, Pause, Escape, Space, Exclaim, DoubleQuote, Hash, Dollar, Percent, Ampersand, Quote, LeftParen, RightParen, Asterisk, Plus, Comma, Minus, Period, Slash, Alpha0, Alpha1, Alpha2, Alpha3, Alpha4, Alpha5, Alpha6, Alpha7, Alpha8, Alpha9, Colon, Semicolon, Less, Equals, Greater, Question, At, LeftBracket, Backslash, RightBracket, Caret, Underscore, BackQuote, A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, LeftCurlyBracket, Pipe, RightCurlyBracket, Tilde, Delete, Keypad0, Keypad1, Keypad2, Keypad3, Keypad4, Keypad5, Keypad6, Keypad7, Keypad8, Keypad9, KeypadPeriod, KeypadDivide, KeypadMultiply, KeypadMinus, KeypadPlus, KeypadEnter, KeypadEquals, UpArrow, DownArrow, RightArrow, LeftArrow, Insert, Home, End, PageUp, PageDown, F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14, F15, Numlock, CapsLock, ScrollLock, RightShift, LeftShift, RightControl, LeftControl, RightAlt, LeftAlt, RightMeta, RightMeta, RightMeta, LeftApple, LeftApple, LeftApple, LeftWindows, RightWindows, AltGr, Help, Print, SysReq, Break, Menu, Mouse0, Mouse1, Mouse2, Mouse3, Mouse4, Mouse5, Mouse6, JoystickButton0, JoystickButton1, JoystickButton2, JoystickButton3, JoystickButton4, JoystickButton5, JoystickButton6, JoystickButton7, JoystickButton8, JoystickButton9, JoystickButton10, JoystickButton11, JoystickButton12, JoystickButton13, JoystickButton14, JoystickButton15, JoystickButton16, JoystickButton17, JoystickButton18, JoystickButton19, Joystick1Button0, Joystick1Button1, Joystick1Button2, Joystick1Button3, Joystick1Button4, Joystick1Button5, Joystick1Button6, Joystick1Button7, Joystick1Button8, Joystick1Button9, Joystick1Button10, Joystick1Button11, Joystick1Button12, Joystick1Button13, Joystick1Button14, Joystick1Button15, Joystick1Button16, Joystick1Button17, Joystick1Button18, Joystick1Button19, Joystick2Button0, Joystick2Button1, Joystick2Button2, Joystick2Button3, Joystick2Button4, Joystick2Button5, Joystick2Button6, Joystick2Button7, Joystick2Button8, Joystick2Button9, Joystick2Button10, Joystick2Button11, Joystick2Button12, Joystick2Button13, Joystick2Button14, Joystick2Button15, Joystick2Button16, Joystick2Button17, Joystick2Button18, Joystick2Button19, Joystick3Button0, Joystick3Button1, Joystick3Button2, Joystick3Button3, Joystick3Button4, Joystick3Button5, Joystick3Button6, Joystick3Button7, Joystick3Button8, Joystick3Button9, Joystick3Button10, Joystick3Button11, Joystick3Button12, Joystick3Button13, Joystick3Button14, Joystick3Button15, Joystick3Button16, Joystick3Button17, Joystick3Button18, Joystick3Button19, Joystick4Button0, Joystick4Button1, Joystick4Button2, Joystick4Button3, Joystick4Button4, Joystick4Button5, Joystick4Button6, Joystick4Button7, Joystick4Button8, Joystick4Button9, Joystick4Button10, Joystick4Button11, Joystick4Button12, Joystick4Button13, Joystick4Button14, Joystick4Button15, Joystick4Button16, Joystick4Button17, Joystick4Button18, Joystick4Button19, Joystick5Button0, Joystick5Button1, Joystick5Button2, Joystick5Button3, Joystick5Button4, Joystick5Button5, Joystick5Button6, Joystick5Button7, Joystick5Button8, Joystick5Button9, Joystick5Button10, Joystick5Button11, Joystick5Button12, Joystick5Button13, Joystick5Button14, Joystick5Button15, Joystick5Button16, Joystick5Button17, Joystick5Button18, Joystick5Button19, Joystick6Button0, Joystick6Button1, Joystick6Button2, Joystick6Button3, Joystick6Button4, Joystick6Button5, Joystick6Button6, Joystick6Button7, Joystick6Button8, Joystick6Button9, Joystick6Button10, Joystick6Button11, Joystick6Button12, Joystick6Button13, Joystick6Button14, Joystick6Button15, Joystick6Button16, Joystick6Button17, Joystick6Button18, Joystick6Button19, Joystick7Button0, Joystick7Button1, Joystick7Button2, Joystick7Button3, Joystick7Button4, Joystick7Button5, Joystick7Button6, Joystick7Button7, Joystick7Button8, Joystick7Button9, Joystick7Button10, Joystick7Button11, Joystick7Button12, Joystick7Button13, Joystick7Button14, Joystick7Button15, Joystick7Button16, Joystick7Button17, Joystick7Button18, Joystick7Button19, Joystick8Button0, Joystick8Button1, Joystick8Button2, Joystick8Button3, Joystick8Button4, Joystick8Button5, Joystick8Button6, Joystick8Button7, Joystick8Button8, Joystick8Button9, Joystick8Button10, Joystick8Button11, Joystick8Button12, Joystick8Button13, Joystick8Button14, Joystick8Button15, Joystick8Button16, Joystick8Button17, Joystick8Button18, Joystick8Button19
+FillAllModKey = LeftShift
 
-rk_barrel2:
-  exclude:
-    - Armor
-    - Swords
+## Key to prevent pulling from nearby containers. This prevents all pulling logic from running, essentially making the mod appear as if it's not installed. This is different from the Mod Enabled option because it allows toggling on the fly (specifically for you as the player)  Use https://docs.unity3d.com/Manual/ConventionalGameInput.html [Not Synced with Server]
+# Setting type: KeyboardShortcut
+# Default value: O + LeftAlt
+# Acceptable values: None, Backspace, Tab, Clear, Return, Pause, Escape, Space, Exclaim, DoubleQuote, Hash, Dollar, Percent, Ampersand, Quote, LeftParen, RightParen, Asterisk, Plus, Comma, Minus, Period, Slash, Alpha0, Alpha1, Alpha2, Alpha3, Alpha4, Alpha5, Alpha6, Alpha7, Alpha8, Alpha9, Colon, Semicolon, Less, Equals, Greater, Question, At, LeftBracket, Backslash, RightBracket, Caret, Underscore, BackQuote, A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, LeftCurlyBracket, Pipe, RightCurlyBracket, Tilde, Delete, Keypad0, Keypad1, Keypad2, Keypad3, Keypad4, Keypad5, Keypad6, Keypad7, Keypad8, Keypad9, KeypadPeriod, KeypadDivide, KeypadMultiply, KeypadMinus, KeypadPlus, KeypadEnter, KeypadEquals, UpArrow, DownArrow, RightArrow, LeftArrow, Insert, Home, End, PageUp, PageDown, F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14, F15, Numlock, CapsLock, ScrollLock, RightShift, LeftShift, RightControl, LeftControl, RightAlt, LeftAlt, RightMeta, RightMeta, RightMeta, LeftApple, LeftApple, LeftApple, LeftWindows, RightWindows, AltGr, Help, Print, SysReq, Break, Menu, Mouse0, Mouse1, Mouse2, Mouse3, Mouse4, Mouse5, Mouse6, JoystickButton0, JoystickButton1, JoystickButton2, JoystickButton3, JoystickButton4, JoystickButton5, JoystickButton6, JoystickButton7, JoystickButton8, JoystickButton9, JoystickButton10, JoystickButton11, JoystickButton12, JoystickButton13, JoystickButton14, JoystickButton15, JoystickButton16, JoystickButton17, JoystickButton18, JoystickButton19, Joystick1Button0, Joystick1Button1, Joystick1Button2, Joystick1Button3, Joystick1Button4, Joystick1Button5, Joystick1Button6, Joystick1Button7, Joystick1Button8, Joystick1Button9, Joystick1Button10, Joystick1Button11, Joystick1Button12, Joystick1Button13, Joystick1Button14, Joystick1Button15, Joystick1Button16, Joystick1Button17, Joystick1Button18, Joystick1Button19, Joystick2Button0, Joystick2Button1, Joystick2Button2, Joystick2Button3, Joystick2Button4, Joystick2Button5, Joystick2Button6, Joystick2Button7, Joystick2Button8, Joystick2Button9, Joystick2Button10, Joystick2Button11, Joystick2Button12, Joystick2Button13, Joystick2Button14, Joystick2Button15, Joystick2Button16, Joystick2Button17, Joystick2Button18, Joystick2Button19, Joystick3Button0, Joystick3Button1, Joystick3Button2, Joystick3Button3, Joystick3Button4, Joystick3Button5, Joystick3Button6, Joystick3Button7, Joystick3Button8, Joystick3Button9, Joystick3Button10, Joystick3Button11, Joystick3Button12, Joystick3Button13, Joystick3Button14, Joystick3Button15, Joystick3Button16, Joystick3Button17, Joystick3Button18, Joystick3Button19, Joystick4Button0, Joystick4Button1, Joystick4Button2, Joystick4Button3, Joystick4Button4, Joystick4Button5, Joystick4Button6, Joystick4Button7, Joystick4Button8, Joystick4Button9, Joystick4Button10, Joystick4Button11, Joystick4Button12, Joystick4Button13, Joystick4Button14, Joystick4Button15, Joystick4Button16, Joystick4Button17, Joystick4Button18, Joystick4Button19, Joystick5Button0, Joystick5Button1, Joystick5Button2, Joystick5Button3, Joystick5Button4, Joystick5Button5, Joystick5Button6, Joystick5Button7, Joystick5Button8, Joystick5Button9, Joystick5Button10, Joystick5Button11, Joystick5Button12, Joystick5Button13, Joystick5Button14, Joystick5Button15, Joystick5Button16, Joystick5Button17, Joystick5Button18, Joystick5Button19, Joystick6Button0, Joystick6Button1, Joystick6Button2, Joystick6Button3, Joystick6Button4, Joystick6Button5, Joystick6Button6, Joystick6Button7, Joystick6Button8, Joystick6Button9, Joystick6Button10, Joystick6Button11, Joystick6Button12, Joystick6Button13, Joystick6Button14, Joystick6Button15, Joystick6Button16, Joystick6Button17, Joystick6Button18, Joystick6Button19, Joystick7Button0, Joystick7Button1, Joystick7Button2, Joystick7Button3, Joystick7Button4, Joystick7Button5, Joystick7Button6, Joystick7Button7, Joystick7Button8, Joystick7Button9, Joystick7Button10, Joystick7Button11, Joystick7Button12, Joystick7Button13, Joystick7Button14, Joystick7Button15, Joystick7Button16, Joystick7Button17, Joystick7Button18, Joystick7Button19, Joystick8Button0, Joystick8Button1, Joystick8Button2, Joystick8Button3, Joystick8Button4, Joystick8Button5, Joystick8Button6, Joystick8Button7, Joystick8Button8, Joystick8Button9, Joystick8Button10, Joystick8Button11, Joystick8Button12, Joystick8Button13, Joystick8Button14, Joystick8Button15, Joystick8Button16, Joystick8Button17, Joystick8Button18, Joystick8Button19
+Prevent Pulling Logic = O + LeftAlt
 
-rk_crate:
-  exclude:
-    - Armor
-    - Swords
-
-rk_crate2:
-  exclude:
-    - Armor
-    - Swords
-
-# Below you will find the configuration for the charcoal kiln, smelter, blast furnace, 
-# piece_cookingstation, piece_cookingstation_iron, piece_oven,
-# bonfire, CastleKit_groundtorch_unlit, fire_pit, hearth,piece_brazierceiling01, piece_brazierfloor01, 
-# piece_groundtorch, piece_groundtorch_blue, piece_groundtorch_green, piece_groundtorch_mist, piece_groundtorch_wood, piece_jackoturnip, and piece_walltorch.
-# The settings here will override the chest settings above.
-charcoal_kiln:
-  exclude:
-    - Woods
-  includeOverride:
-    - Wood
-
-# Below are for RelicHeim/JewelHeim
-SmallerKiln_JH:
-  exclude:
-    - Woods
-  includeOverride:
-    - Wood
-
-smelter:
-  exclude: [] # This is an example of how to allow everything to be pulled from the bonfire but still have it in the config file.
-
-blastfurnace:
-  exclude: []
-
-piece_cookingstation:
-  exclude: []
-
-piece_cookingstation_iron:
-  exclude: []
-
-piece_oven:
-  exclude: []
-
-bonfire:
-  exclude: []
-
-CastleKit_groundtorch_unlit:
-  exclude: []
-
-fire_pit:
-  exclude: []
-
-hearth:
-  exclude: []
-
-piece_brazierceiling01:
-  exclude: []
-
-piece_brazierfloor01:
-  exclude: []
-
-piece_groundtorch:
-  exclude: []
-
-piece_groundtorch_blue:
-  exclude: []
-
-piece_groundtorch_green:
-  exclude: []
-
-piece_groundtorch_mist:
-  exclude: []
-
-piece_groundtorch_wood:
-  exclude: []
-
-piece_jackoturnip:
-  exclude: []
-
-piece_walltorch:
-  exclude: []
-
-# The station configurations below are checked before containers. Meaning, if it's blocked in one of the stations, it doesn't matter if it's included in the container.
-# Including something here also overrides container includes/excludes.
-
-# Epic Loot Table
-piece_enchantingtable:
-  exclude: []
-
-
-# Vanilla Crafting Stations
-piece_workbench:
-  exclude: []
-
-piece_cauldron:
-  exclude: []
-
-piece_preptable:
-  exclude: []
-
-piece_stonecutter:
-  exclude: []
-
-piece_artisanstation:
-  exclude: []
-
-forge:
-  exclude: []
-
-blackforge:
-  exclude: []
-  
-piece_magetable:
-  exclude: []
-  
-# Below are for RelicHeim purposes, don't delete
-bp_explorer:
-  exclude:
-    - Trophy
-    - Boss Trophy
-    - Armor
-    - Equipment
-TrophyBackpack:
-  exclude:
-    - Trophy
-    - Boss Trophy
-    - Armor
-    - Equipment
-ExplorersBackpack:
-  exclude:
-    - Trophy
-    - Boss Trophy
-    - Armor
-    - Equipment
-SimpleBackpack:
-  exclude:
-    - Trophy
-    - Boss Trophy
-    - Armor
-    - Equipment
-TrollBackpack:
-  exclude:
-    - Trophy
-    - Boss Trophy
-    - Armor
-    - Equipment
-TrollBackpack:
-  exclude:
-    - Trophy
-    - Boss Trophy
-    - Armor
-    - Equipment
-WishboneBackpack:
-  exclude:
-    - Trophy
-    - Boss Trophy
-    - Armor
-    - Equipment
```

---

#### Azumatt.FactionAssigner.cfg

**Status**: Modified

**Summary**: +1, -30 changes

**Key Changes**:

**Total changes**: 31 (showing top 8)

• **1 - Logging.Log Faction Info**: `Off` *(new setting)*
• **Abomination**: `Undead` *(removed)*
• **ArcticBear_TW**: `Boss` *(removed)*
• **ArcticGolem_TW**: `Boss` *(removed)*
• **ArcticMammoth_TW**: `Boss` *(removed)*
• **ArcticSerpent_TW**: `Boss` *(removed)*
• **ArcticWolf_TW**: `Boss` *(removed)*
• **BlobTar**: `Boss` *(removed)*
• ... and 23 more changes

**Full Diff**:

```diff
--- backup/Azumatt.FactionAssigner.cfg+++ current/Azumatt.FactionAssigner.cfg@@ -1,46 +1,11 @@-Abomination: Undead
-Troll: ForestMonsters
-StoneGolem: MountainMonsters
-Lox: PlainsMonsters
-Skeleton_Poison: Undead
-BlobTar: Boss
-Hatchling: MountainMonsters
-GoblinBrute: PlainsMonsters
-Serpent: Boss
-# Monstrum:
-ObsidianGolem_TW: MountainMonsters
-Shark_TW: Boss
-# Monstrum_DeepNorth
-ArcticBear_TW: Boss
-ArcticWolf_TW: Boss
-ArcticMammoth_TW: Boss
-ArcticSerpent_TW: Boss
-ArcticGolem_TW: Boss
-StormCultist_TW: Boss
-StormFenring_TW: Boss
-JotunnBrute_TW: Boss
-JotunnJuggernaut_TW: Boss
-JotunnBladefist_TW: Boss
-JotunnShaman_TW: Boss
-JotunnWolf_TW: Boss
-StormWolf_TW: Boss
-# Wizardry:
-GreydwarfMage_TW: ForestMonsters
-SkeletonMage_TW: Undead
-FenringMage_TW: MountainMonsters
-GoblinMage_TW: PlainsMonsters
-CorruptedDvergerMage_TW: Boss
-SummonedSeeker_TW: Boss
+## Settings file was created by plugin FactionAssigner v1.0.4
+## Plugin GUID: Azumatt.FactionAssigner
 
-#Factions:
-#Players
-#AnimalsVeg
-#ForestMonsters
-#Undead
-#Demon
-#MountainMonsters
-#SeaMonsters
-#PlainsMonsters
-#Boss
-#MistlandsMonsters
-#Dverger+[1 - Logging]
+
+## If on, when you reach the main menu, a list of all creatures and their factions will be logged to the console. Due to where this runs, this doesn't need to be server synced. [Not Synced with Server]
+# Setting type: Toggle
+# Default value: Off
+# Acceptable values: Off, On
+Log Faction Info = Off
+

```

---


### Creature Config

*Files in this category with changes from RelicHeim backup:*

#### CreatureConfig_Creatures.yml

**Status**: Modified

**Summary**: +4 changes

**Key Changes**:

**Total changes**: 4 (showing top 4)

• **world level**: `` *(new setting)*
• **LeechMatron**: `` *(new setting)*
• **attacks**: `` *(new setting)*
• **charge**: `` *(new setting)*

**Full Diff**:

```diff
--- backup/CreatureConfig_Creatures.yml+++ current/CreatureConfig_Creatures.yml@@ -86,6 +86,12 @@  Ashlands:
   health: 15
   health per star: 3
+# New swamp elite
+LeechMatron:
+  health: 10
+  health per star: 5
+  damage: 2
+  damage per star: 1
 #Mountains
 Ulv:
   health: 2.2
@@ -244,6 +250,12 @@   count: 5
  effect power:
   Regenerating: 0.5
+ world level:
+  health: 1.2
+  damage: 1.2
+ attacks:
+  charge:
+   damage: 1.5
  tamed:
   damage: 0.6
   damage per star: 0.1

```

---

#### CreatureConfig_Bosses.yml

**Status**: Modified

**Summary**: +18, ~9 changes

**Key Changes**:

**Total changes**: 27 (showing top 8)

• **attack speed**: `1.2` → `1.1` (-0.1)
• **damage**: `[1, 1.1, 1.12, 1.14, 1.16, 1.2]` → `[1.2, 1.3, 1.4, 1.5, 1.6, 1.7]`
• **health**: `1` → `1.2` (+0.2)
• **health per star**: `0.02` → `0.1` (+0.08)
• **movement speed**: `1.1` → `1.2` (+0.1)
• **size**: `2` *(new setting)*
• **AvalancheDrake**: `` *(new setting)*
• **Elementalist**: `35` → `40` (+5)
• ... and 19 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| Elementalist | 35 | 40 | +5 |
| Fire | 0.25 | 0.1 | -0.15 |
| Frost | 0.75 | 1 | +0.25 |
| armored | 0 | 100 | +100 |
| attack speed | 1.2 | 1.1 | -0.1 |
| health | 1 | 1.2 | +0.2 |
| health per star | 0.02 | 0.1 | +0.08 |
| movement speed | 1.1 | 1.2 | +0.1 |

**Full Diff**:

```diff
--- backup/CreatureConfig_Bosses.yml+++ current/CreatureConfig_Bosses.yml@@ -43,9 +43,10 @@     Blunt: 0.75
     Bows: 0.5
   affix:
-    Enraged: 80
-    Summoner: 10
-    Mending: 10
+    Enraged: 70
+    Summoner: 10
+    Mending: 10
+    WebSnare: 10
     other: 0
   affix power:
     Mending: 0.2
@@ -64,6 +65,24 @@     other: 0
   affix power:
     Mending: 0.1
+
+AvalancheDrake:
+  size: 1.6
+  infusion:
+    Spirit: 1
+  health: 1.1
+  health per star: 0.1
+  attack speed: 1.2
+  movement speed: 1.2
+  damage: [1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
+  affix:
+    Enraged: 40
+    Elementalist: 40
+    Summoner: 10
+    RockSummoner: 10
+    other: 0
+  affix power:
+    RockSummoner: 0.1
 
 GoblinKing:
   health: 1.1
@@ -101,9 +120,10 @@     Frost: 0.75
     Fire: 0.25
   affix:
-    Enraged: 80
-    Summoner: 10
-    Mending: 10
+    Enraged: 70
+    Summoner: 10
+    Mending: 10
+    WebSnare: 10
     other: 0
   affix power:
     Mending: 0.1
@@ -120,6 +140,60 @@     Elementalist: 40
     Summoner: 10
     Mending: 10
+    other: 0
+  affix power:
+    Mending: 0.1
+
+TempestSerpent:
+  size: 2.5
+  health: 1.15
+  health per star: 0.1
+  attack speed: 1.3
+  movement speed: 1.2
+  damage: [1.4, 1.5, 1.6, 1.7, 1.8, 2.0]
+  infusion:
+    lightning: 100
+  effect:
+    armored: 100
+  affix:
+    Enraged: 60
+    Elementalist: 30
+    Summoner: 10
+    other: 0
+
+MushroomBossSwamp_MP:
+  health: 1.1
+  health per star: 0.1
+  attack speed: 1.2
+  movement speed: 1.3
+  damage: [1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
+  damage taken:
+    Bows: 0.5
+    Fire: 0.75
+    Frost: 0.75
+  affix:
+    Enraged: 60
+    Summoner: 20
+    Mending: 20
+    other: 0
+  affix power:
+    Mending: 0.1
+
+MushroomBossDN_MP:
+  health: 1.2
+  health per star: 0.15
+  attack speed: 1.2
+  movement speed: 1.3
+  damage: [1.4, 1.5, 1.6, 1.7, 1.8, 2.0]
+  damage taken:
+    Bows: 0.5
+    Fire: 0.75
+    Frost: 0.75
+    Spirit: 0.75
+  affix:
+    Enraged: 60
+    Elementalist: 20
+    Summoner: 20
     other: 0
   affix power:
     Mending: 0.1
@@ -327,4 +401,141 @@   affix:
     other: 0
   affix power:
-    Mending: 0.1+    Mending: 0.1
+
+FrostDragon:
+  stars: [0, 15, 50, 25, 10]
+  health: 1
+  health per star: 0.02
+  damage: [1.2, 1.3, 1.4, 1.5, 1.6, 1.8]
+  damage taken:
+    Fire: 0.25
+    Bows: 0.5
+  infusion:
+    frost: 100
+
+StoneGolem:
+  stars: [0, 15, 50, 25, 10]
+  damage: [1.15, 1.2, 1.25, 1.3, 1.35, 1.4]
+  damage taken:
+    Fire: 0.1
+  effect:
+    armored: 100
+    other: 0
+
+# Roaming Bosses
+TempestNeck:
+  size: 3
+  health: 1.05
+  health per star: 0.05
+  attack speed: 1.1
+  movement speed: 1.1
+  damage: [1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
+  affix:
+    Enraged: 40
+    Elementalist: 40
+    Summoner: 10
+    Mending: 10
+    other: 0
+  affix power:
+    Mending: 0.1
+
+TollTroll:
+  size: 1.3
+  health: 1.1
+  health per star: 0.1
+  attack speed: 1.1
+  movement speed: 1.1
+  damage: [1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
+  affix:
+    Enraged: 40
+    Elementalist: 40
+    Summoner: 10
+    Mending: 10
+    other: 0
+  affix power:
+    Mending: 0.1
+
+LeechMatron:
+  size: 4
+  health: 1.1
+  health per star: 0.1
+  attack speed: 1.1
+  movement speed: 1
+  damage: [1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
+  affix:
+    Enraged: 40
+    Elementalist: 40
+    Summoner: 10
+    Mending: 10
+    other: 0
+  affix power:
+    Mending: 0.1
+
+RoyalLox:
+  size: 1.6
+  health: 1.2
+  health per star: 0.08
+  attack speed: 1.1
+  movement speed: 1.1
+  damage: [1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
+  affix:
+    Enraged: 40
+    Elementalist: 40
+    Summoner: 10
+    Mending: 10
+    other: 0
+  affix power:
+    Mending: 0.1
+
+WeaverQueen:
+  size: 1.5
+  health: 1.1
+  health per star: 0.05
+  attack speed: 1.1
+  movement speed: 1.1
+  damage: [1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
+  affix:
+    Enraged: 40
+    Elementalist: 40
+    Summoner: 10
+    Mending: 10
+    other: 0
+  affix power:
+    Mending: 0.1
+
+MagmaGolem:
+  size: 2
+  health: 1.2
+  health per star: 0.1
+  attack speed: 1
+  movement speed: 1
+  damage: [1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
+  damage taken:
+    Fire: 0.1
+  affix:
+    Enraged: 40
+    Elementalist: 40
+    Summoner: 10
+    Mending: 10
+    other: 0
+  affix power:
+    Mending: 0.1
+
+FrostWyrm:
+  size: 2
+  health: 1.2
+  health per star: 0.1
+  attack speed: 1.1
+  movement speed: 1.2
+  damage: [1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
+  infusion:
+    Frost: 1
+  affix:
+    Enraged: 40
+    Elementalist: 40
+    Summoner: 10
+    Mending: 10
+    other: 0
+  affix power:
+    Mending: 0.1

```

---


### Custom Raids

*Files in this category with changes from RelicHeim backup:*

#### custom_raids.cfg

**Status**: Modified

**Summary**: ~2 changes

**Key Changes**:

**Total changes**: 2 (showing top 2)

• **EventSystem.EventTriggerChance**: `40` → `25` (-15)
• **EventSystem.EventCheckInterval**: `60` → `90` (+30)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| EventSystem.EventCheckInterval | 60 | 90 | +30 |
| EventSystem.EventTriggerChance | 40 | 25 | -15 |

**Full Diff**:

```diff
--- backup/custom_raids.cfg+++ current/custom_raids.cfg@@ -56,13 +56,13 @@ ## When the interval has passed, all raids are checked for valid conditions and a random valid one is selected. Chance is then rolled for if it should start.
 # Setting type: Single
 # Default value: 46
-EventCheckInterval = 60
+EventCheckInterval = 90
 
 ## Chance of raid, per check interval. 100 is 100%.
 ## Note: Not used if UseIndividualRaidChecks is enabled, each raid will have their own chance in that case.
 # Setting type: Single
 # Default value: 20
-EventTriggerChance = 40
+EventTriggerChance = 25
 
 [General]
 

```

---

#### custom_raids.raids.cfg

**Status**: Modified

**Summary**: -18 changes

**Key Changes**:

**Total changes**: 18 (showing top 8)

• **EventSystem.EventTriggerChance**: `40` *(removed)*
• **General.GeneratePresetRaids**: `true` *(removed)*
• **General.PauseEventTimersWhileOffline**: `true` *(removed)*
• **IndividualRaids.MinimumTimeBetweenRaids**: `120` *(removed)*
• **Debug.DebugFileFolder**: `Debug` *(removed)*
• **Debug.DebugOn**: `false` *(removed)*
• **Debug.TraceLogging**: `false` *(removed)*
• **Debug.WriteDefaultEventDataToDisk**: `false` *(removed)*
• ... and 10 more changes

**Full Diff**:

```diff
--- backup/custom_raids.raids.cfg+++ current/custom_raids.raids.cfg@@ -1,109 +0,0 @@-[Debug]
-
-## Enables debug logging.
-# Setting type: Boolean
-# Default value: false
-DebugOn = false
-
-## Enables trace logging. Note, this will generate a LOT of log entries.
-# Setting type: Boolean
-# Default value: false
-TraceLogging = false
-
-## If enabled, scans existing raid event data, and writes to a file.
-# Setting type: Boolean
-# Default value: false
-WriteDefaultEventDataToDisk = false
-
-## If enabled, dumps raid event data after applying configuration to a file.
-# Setting type: Boolean
-# Default value: false
-WritePostChangeEventDataToDisk = false
-
-## If enabled, scans existing environment (weather) data, and writes to a file.
-# Setting type: Boolean
-# Default value: false
-WriteEnvironmentDataToDisk = false
-
-## If enabled, scans for possible global keys from creture kills, and writes to a file.
-# Setting type: Boolean
-# Default value: false
-WriteGlobalKeyDataToDisk = false
-
-## If enabled, scans existing locations (aka. points of interest) and writes to a file.
-# Setting type: Boolean
-# Default value: false
-WriteLocationsToDisk = false
-
-## Folder path to write debug files to. Root folder is BepInEx.
-# Setting type: String
-# Default value: Debug
-DebugFileFolder = Debug
-
-[EventSystem]
-
-## If enabled, removes all existing raids and only allows configured. Will only remove non-random events, leaving boss events as is.
-# Setting type: Boolean
-# Default value: false
-RemoveAllExistingRaids = false
-
-## Enable/disable override of existing events when event names match.
-# Setting type: Boolean
-# Default value: true
-OverrideExisting = true
-
-## Minutes between checks for starting raids.
-## When the interval has passed, all raids are checked for valid conditions and a random valid one is selected. Chance is then rolled for if it should start.
-# Setting type: Single
-# Default value: 46
-EventCheckInterval = 60
-
-## Chance of raid, per check interval. 100 is 100%.
-## Note: Not used if UseIndividualRaidChecks is enabled, each raid will have their own chance in that case.
-# Setting type: Single
-# Default value: 20
-EventTriggerChance = 40
-
-[General]
-
-## Loads raid configurations from supplemental files.
-## Eg. custom_raid.supplemental.my_raid.cfg will be included on load.
-# Setting type: Boolean
-# Default value: true
-LoadSupplementalRaids = true
-
-## Generates pre-defined supplemental raids. The generated raids are disabled by default.
-# Setting type: Boolean
-# Default value: true
-GeneratePresetRaids = true
-
-## Disables automatic updating and saving of raid configurations on loadup.
-## This mainly means no comments or missing options will be added, but.. allows you to keep things compact.
-## Note: This also has a massive impact upon load time.
-# Setting type: Boolean
-# Default value: true
-StopTouchingMyConfigs = true
-
-## Server option. If enabled, pauses the event timers when no players are online. 
-## This means if a raid happened a minute before everyone logged out, and everyone logs in an hour later, the game will consider the last raid as having happened one minute before the login.
-# Setting type: Boolean
-# Default value: true
-PauseEventTimersWhileOffline = true
-
-[IndividualRaids]
-
-## If enabled, Custom Raids will overhaul the games way of checking for raids.
-## EventTriggerChance will no longer be used, as the chance will be set per raid.
-## This allows for setting individual frequences and chances for each raid.
-## This overhaul gives each raid it's own timer, independent of each other and can therefore cause a LOT of raids.
-## EventCheckInterval will still be used to indicate time between checks. 
-## MinTimeBetweenRaids can be used to ensure they don't happen too often.
-# Setting type: Boolean
-# Default value: false
-UseIndividualRaidChecks = false
-
-## If overhaul is enabled, ensures a minimum amount of minutes between each raid.
-# Setting type: Single
-# Default value: 46
-MinimumTimeBetweenRaids = 120
-

```

---

#### custom_raids.supplemental.deathsquitoseason.cfg

**Status**: Modified

**Summary**: +23, -819 changes

**Key Changes**:

**Total changes**: 842 (showing top 8)

• **BoarParty_JH.0.GroupRadius**: `15` *(removed)*
• **BoarParty_JH.0.GroupSizeMax**: `3` *(removed)*
• **BoarParty_JH.0.GroupSizeMin**: `2` *(removed)*
• **BoarParty_JH.0.SpawnChancePerInterval**: `100` *(removed)*
• **BoarParty_JH.0.SpawnDistance**: `10` *(removed)*
• **Cultist_Hunt_JH.0.GroupSizeMax**: `1` *(removed)*
• **Cultist_Hunt_JH.0.GroupSizeMin**: `1` *(removed)*
• **Cultist_Hunt_JH.0.SpawnChancePerInterval**: `100` *(removed)*
• ... and 834 more changes

**Full Diff**:

```diff
--- backup/custom_raids.supplemental.deathsquitoseason.cfg+++ current/custom_raids.supplemental.deathsquitoseason.cfg@@ -1,970 +1,27 @@-/////////Eikthyr_Resistance/////////
 
-[Eikthyr_Resistance_JH]
-Name=Eikthyr_Resistance
+[DeathsquitoSeason]
+Name = DeathsquitoSeason
+Duration=3600
+NearBaseOnly=true
+StartMessage=Deathsquito season
+EndMessage=The season has ended
+Enabled=false
+RequiredGlobalKeys=defeated_bonemass
+
+[DeathsquitoSeason.0]
+Name=Deathsquito
 Enabled=True
-Random=True
-Biomes=Meadows, BlackForest
-Duration=90
-StartMessage= Eikthyr's death has enraged those still loyal to him.
-EndMessage= The resistance has been quenched.
-NearBaseOnly=False
-RequiredGlobalKeys= defeated_eikthyr
-NotRequiredGlobalKeys=defeated_gdking
-PauseIfNoPlayerInArea=False
-ForceEnvironment= Eikthyr
-ForceMusic=CombatEventL4
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_eikthyr
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=defeated_gdking
-InsidePlayerBase=true
-
-[Eikthyr_Resistance_JH.0]
-Name=Neck
-Enabled=true
-PrefabName=Neck
-MaxSpawned=3
-SpawnInterval=20
-SpawnChancePerInterval=100
+PrefabName=Deathsquito
+MaxSpawned=10
+SpawnInterval=10
 SpawnDistance=0
-GroupSizeMin=2
+SpawnRadiusMin=0
+SpawnRadiusMax=1
+GroupSizeMin=3
 GroupSizeMax=3
 SpawnAtNight=True
 SpawnAtDay=True
 HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
-
-[Eikthyr_Resistance_JH.1]
-Name=Boar
-Enabled=true
-PrefabName=Boar
-MaxSpawned=3
-SpawnInterval=20
-SpawnChancePerInterval=100
-SpawnDistance=0
-GroupSizeMin=2
-GroupSizeMax=3
-SpawnAtNight=True
-SpawnAtDay=True
-HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
-
-[Eikthyr_Resistance_JH.2]
-Name=Greyling
-Enabled=true
-PrefabName=Greyling
-MaxSpawned=3
-SpawnInterval=20
-SpawnChancePerInterval=100
-SpawnDistance=0
-GroupSizeMin=2
-GroupSizeMax=3
-SpawnAtNight=True
-SpawnAtDay=True
-HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
-
-/////////BoarParty/////////
-
-[BoarParty_JH]
-Name=BoarParty
-Enabled=True
-Random=True
-Biomes=Meadows, BlackForest
-Duration=90
-StartMessage= Stampeeeeede.
-EndMessage= The stampede has ended.
-NearBaseOnly=False
-RequiredGlobalKeys=
-NotRequiredGlobalKeys=defeated_gdking
-PauseIfNoPlayerInArea=False
-ForceEnvironment= Eikthyr
-ForceMusic=CombatEventL4
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=defeated_gdking
-InsidePlayerBase=true
-
-[BoarParty_JH.0]
-Name=Boar
-Enabled=true
-PrefabName=Boar
-MaxSpawned=3
-SpawnInterval=15
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=2
-GroupSizeMax=3
-GroupRadius=15
-SpawnAtNight=True
-SpawnAtDay=True
-HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
-
-/////////Troll_Scare/////////
-
-[Troll_Scare_JH]
-Name=Troll_Scare
-Enabled=True
-Random=True
-Biomes=Meadows, BlackForest
-Duration=90
-StartMessage= You hear loud stomps.
-EndMessage= The rumbling ends.
-NearBaseOnly=False
-RequiredGlobalKeys=KilledTroll, defeated_eikthyr
-PauseIfNoPlayerInArea=False
-ForceEnvironment= Misty
-ForceMusic=boss_queen
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=KilledTroll, defeated_eikthyr
-InsidePlayerBase=true
-
-[Troll_Scare_JH.0]
-Name=Troll
-Enabled=true
-PrefabName=Troll
-MaxSpawned=2
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-GroupSizeMin=1
-GroupSizeMax=2
-SpawnAtNight=True
-SpawnAtDay=True
-HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
-
-/////////Forest_Healers/////////
-
-[Forest_Healers_JH]
-Name=Forest_Healers
-Enabled=True
-Random=True
-Biomes=Meadows, BlackForest
-Duration=90
-StartMessage= The Elder, sends out his healers.
-EndMessage= The Elder accepts your survival.
-NearBaseOnly=False
-RequiredGlobalKeys= defeated_eikthyr
-PauseIfNoPlayerInArea=False
-ForceEnvironment= DeepForest Mist
-ForceMusic=CombatEventL3
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_eikthyr
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Forest_Healers_JH.0]
-Name=GreydwarfShaman
-Enabled=true
-PrefabName=Greydwarf_Shaman
-MaxSpawned=2
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-SpawnAtNight=True
-SpawnAtDay=True
-HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
-
-[Forest_Healers_JH.1]
-Name=Greydwarf
-Enabled=true
-PrefabName=Greydwarf
-MaxSpawned=3
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=2
-GroupSizeMax=4
-SpawnAtNight=True
-SpawnAtDay=True
-HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
-
-/////////Elders Wrath/////////
-
-[Elders_Wrath_JH]
-Name=Elders_Wrath
-Enabled=True
-Random=True
-Biomes=Meadows, BlackForest
-Duration=90
-StartMessage= The Elder, sends out his brutes.
-EndMessage= The Elder accepts your survival.
-NearBaseOnly=False
-RequiredGlobalKeys= defeated_eikthyr
-PauseIfNoPlayerInArea=False
-ForceEnvironment= ThunderStorm
-ForceMusic=CombatEventL4
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_eikthyr
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Elders_Wrath_JH.0]
-Name=Greydwarf_Elite
-Enabled=true
-PrefabName=Greydwarf_Elite
-MaxSpawned=2
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-SpawnAtNight=True
-SpawnAtDay=True
-HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
-
-[Elders_Wrath_JH.1]
-Name=Greydwarf
-Enabled=true
-PrefabName=Greydwarf
-MaxSpawned=3
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=2
-GroupSizeMax=4
-SpawnAtNight=True
-SpawnAtDay=True
-HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
-
-
-/////////Ghost_Town/////////
-
-[Ghost_Town_JH]
-Name=Ghost_Town
-Enabled=True
-Random=True
-Biomes= Meadows, BlackForest
-Duration=90
-StartMessage= The souls of the dead have been set free.
-EndMessage= The souls can finally rest.
-NearBaseOnly=False
-RequiredGlobalKeys= defeated_eikthyr
-NotRequiredGlobalKeys=defeated_gdking
-PauseIfNoPlayerInArea=False
-ForceEnvironment= Misty
-ForceMusic=CombatEventL4
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_eikthyr
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=defeated_gdking
-InsidePlayerBase=true
-
-[Ghost_Town_JH.0]
-Name=Ghost
-Enabled=true
-PrefabName=Ghost
-MaxSpawned=3
-SpawnInterval=20
-SpawnChancePerInterval=100
-SpawnDistance=5
-GroupSizeMin=2
-GroupSizeMax=3
-SpawnAtNight=True
-SpawnAtDay=True
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-
-/////////Revulting_Remains/////////
-
-[Revulting_Remains_JH]
-Name=Revulting_Remains
-Enabled=True
-Random=True
-Biomes=Meadows, BlackForest
-Duration=90
-StartMessage= You see a light flickering in the distance.
-EndMessage= The light goes dim.
-NearBaseOnly=False
-RequiredGlobalKeys= defeated_eikthyr
-PauseIfNoPlayerInArea=False
-ForceEnvironment= GDKing
-ForceMusic=CombatEventL4
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_eikthyr
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Revulting_Remains_JH.0]
-Name=Skeleton_Poison
-Enabled=true
-PrefabName=Skeleton_Poison
-MaxSpawned=2
-SpawnInterval=20
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=2
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-
-/////////Draugr_Daddy/////////
-
-[Draugr_Daddy_JH]
-Name=Draugr_Daddy
-Enabled=True
-Random=True
-Biomes=Meadows, Swamp
-Duration=90
-StartMessage= You spot glowing eyes staring at you.
-EndMessage= You're no longer being watched.
-NearBaseOnly=False
-RequiredGlobalKeys= defeated_gdking
-NotRequiredGlobalKeys= defeated_dragon
-PauseIfNoPlayerInArea=False
-ForceEnvironment= SwampRain
-ForceMusic=CombatEventL4
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_gdking
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=defeated_dragon
-InsidePlayerBase=true
-
-[Draugr_Daddy_JH.0]
-Name=DraugrElite
-Enabled=true
-PrefabName=Draugr_Elite
-MaxSpawned=2
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-
-[Draugr_Daddy_JH.1]
-Name=Draugr_Ranged
-Enabled=true
-PrefabName=Draugr_Ranged
-MaxSpawned=2
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-
-[Draugr_Daddy_JH.2]
-Name=Draugr
-Enabled=true
-PrefabName=Draugr
-MaxSpawned=2
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-
-/////////Floating_Death/////////
-
-[Floating_Death_JH]
-Name=Floating_Death
-Enabled=True
-Random=True
-Biomes=Swamp
-Duration=90
-StartMessage= The Spirits of this realm have unfinished business.
-EndMessage= The Spirits fade back to Hell.
-NearBaseOnly=False
-RequiredGlobalKeys= defeated_gdking
-PauseIfNoPlayerInArea=False
-ForceEnvironment= SunkenCrypt
-ForceMusic=CombatEventL4
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_gdking
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Floating_Death_JH.0]
-Name=Wraith
-Enabled=true
-PrefabName=Wraith
-MaxSpawned=2
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=5
-GroupSizeMin=2
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-
-/////////Cultist_Hunt/////////
-
-[Cultist_Hunt_JH]
-Name=Cultist_Hunt
-Enabled=True
-Random=True
-Biomes=Meadows, Mountain, DeepNorth
-Duration=90
-StartMessage= You've walked to close to their den, now perish.
-EndMessage= The creatures head back to their den.
-NearBaseOnly=False
-RequiredGlobalKeys= KilledBat
-PauseIfNoPlayerInArea=False
-ForceEnvironment= GoblinKing
-ForceMusic=CombatEventL4
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=KilledBat
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Cultist_Hunt_JH.0]
-Name=Fenring_Cultist
-Enabled=true
-PrefabName=Fenring_Cultist
-MaxSpawned=1
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=1
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-
-[Cultist_Hunt_JH.1]
-Name=Ulv
-Enabled=true
-PrefabName=Ulv
-MaxSpawned=3
-SpawnInterval=15
-SpawnChancePerInterval=100
-SpawnDistance=5
-GroupSizeMin=2
-GroupSizeMax=3
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-
-/////////TarParty/////////
-
-[TarParty_JH]
-Name=TarParty
-Enabled=True
-Random=True
-Biomes=Plains
-Duration=60
-StartMessage= Some sticky black blobs 
-EndMessage= I'm covered in tar...
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_dragon
-PauseIfNoPlayerInArea=False
-ForceMusic=CombatEventL2
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_dragon
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[TarParty_JH.0]
-Name=TarMob
-Enabled=true
-PrefabName=BlobTar
-MaxSpawned=3
-SpawnInterval=20
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=2
-GroupSizeMax=3
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-
-/////////Serpent_Rush/////////
-
-[Serpent_Rush_JH]
-Name=Serpent_Rush
-Enabled=True
-Random=True
-Biomes=Ocean
-Duration=90
-StartMessage= What's that shining light under the water?!
-EndMessage= The serpents swim to the depths
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_gdking
-PauseIfNoPlayerInArea=False
-ForceMusic=boss_queen
-ForceEnvironment= ThunderStorm
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_gdking
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Serpent_Rush_JH.0]
-Name=Serpent
-Enabled=true
-PrefabName=Serpent
-MaxSpawned=2
-SpawnInterval=60
-SpawnChancePerInterval=100
-SpawnDistance=15
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-GroupSizeMin=2
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = -75
-AltitudeMax = 1000
-GroupRadius= 20
-
-/////////Mosquitos/////////
-
-[Mosquitos_JH]
-Name=Mosquitos
-Enabled=True
-Random=True
-Biomes=Meadows, Plains
-Duration=90
-StartMessage= The Air Screams With Wings and Death…
-EndMessage= The Buzzing Fades… But Your Heart Still Races.
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_dragon
-PauseIfNoPlayerInArea=False
-ForceMusic=CombatEventL2
-ForceEnvironment= Misty
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_dragon
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Mosquitos_JH.0]
-Name=Mosquitos
-Enabled=true
-PrefabName=Deathsquito
-MaxSpawned=4
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=30
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-GroupSizeMin=2
-GroupSizeMax=4
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-GroupRadius= 10
-
-[RootedAlive_JH]
-Name=RootedAlive
-Enabled=True
-Random=True
-Biomes= Meadows, Swamp
-Duration=90
-StartMessage= The land Groans With Unnatural Life…
-EndMessage= You survived the land's wrath. But its heart still beats.
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_gdking
-PauseIfNoPlayerInArea=False
-ForceMusic=boss_queen
-ForceEnvironment= SwampRain
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_gdking
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[RootedAlive_JH.0]
-Name=RootedAlive
-Enabled=true
-PrefabName=Abomination
-MaxSpawned=1
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=1
-HuntPlayer=True
-AltitudeMin=-2
-AltitudeMax=1000
-GroupRadius=10
-
-/////////Stony/////////
-
-[Stony_JH]
-Name=Stony
-Enabled=True
-Random=True
-Biomes=Meadows, Mountain
-Duration=90
-StartMessage= The Mountain Walks…
-EndMessage= The Stones Fall Silent Once More.
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_bonemass
-PauseIfNoPlayerInArea=False
-ForceMusic=CombatEventL4
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_bonemass
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Stony_JH.0]
-Name=Stony
-Enabled=true
-PrefabName=StoneGolem
-MaxSpawned=2
-SpawnInterval=45
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-GroupRadius= 10
-
-/////////FurryMadness/////////
-[FurryMadness_JH]
-Name=FurryMadness
-Enabled=True
-Random=True
-Biomes=Meadows, Plains
-Duration=90
-StartMessage= The Land Itself Begins to Move…
-EndMessage= The Thundering Steps Grow Distant.
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_dragon
-NotRequiredGlobalKeys=
-PauseIfNoPlayerInArea=False
-ForceMusic=CombatEventL4
-ForceEnvironment= 
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_dragon
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[FurryMadness_JH.0]
-Name=FurryMadness
-Enabled=true
-PrefabName=Lox
-MaxSpawned=2
-SpawnInterval=20
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-GroupRadius= 10
-
-/////////Rage/////////
-
-[Rage_JH]
-Name=Rage
-Enabled=True
-Random=True
-Biomes=Meadows, Plains
-Duration=90
-StartMessage= The Brutes have come to smash, burn, and bellow.
-EndMessage= This was a warning — and the Brutes never grunt alone.
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_dragon
-NotRequiredGlobalKeys=
-PauseIfNoPlayerInArea=False
-ForceMusic=CombatEventL4
-ForceEnvironment= Misty
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_dragon
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Rage_JH.0]
-Name=Rage
-Enabled=true
-PrefabName=GoblinBrute
-MaxSpawned=2
-SpawnInterval=20
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-GroupRadius= 10
-
-/////////MutatedNecks/////////
-
-[MutatedNecks_JH]
-Name=MutatedNecks
-Enabled=True
-Random=True
-Biomes=Meadows, AshLands
-Duration=90
-StartMessage= a horde of bulky necks?
-EndMessage= the mutated necks retreat
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_queen
-NotRequiredGlobalKeys=
-PauseIfNoPlayerInArea=False
-ForceMusic=CombatEventL4
-ForceEnvironment= 
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_queen
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[MutatedNecks_JH.0]
-Name=MutatedNecks
-Enabled=true
-PrefabName=Asksvin
-MaxSpawned=2
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=2
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-GroupRadius= 10
-
-/////////Valkyrie/////////
-
-[Valkyrie_JH]
-Name=Valkyrie
-Enabled=True
-Random=True
-Biomes=Meadows, AshLands
-Duration=90
-StartMessage= You were chosen once. Now you are judged
-EndMessage= They return to the void between worlds — until Valhalla weeps again
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_queen
-NotRequiredGlobalKeys=
-PauseIfNoPlayerInArea=False
-ForceMusic=CombatEventL4
-ForceEnvironment= 
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_queen
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Valkyrie_JH.0]
-Name=Valkyrie
-Enabled=true
-PrefabName=FallenValkyrie
-MaxSpawned=1
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-GroupRadius= 10
-
-/////////Surtling/////////
-
-[Surtling_JH]
-Name=Surtling_JH
-Enabled=True
-Random=True
-Biomes=Meadows, Swamp, BlackForest
-Duration=120
-StartMessage= The land burns — and they dance in its ashes.
-EndMessage= The fire sleeps. But it always dreams of burning again.
-NearBaseOnly=False
-RequiredGlobalKeys=killed_surtling
-NotRequiredGlobalKeys=
-PauseIfNoPlayerInArea=False
-ForceEnvironment=Ashlands_CinderRain
-ForceMusic=CombatEventL3
-ConditionPlayerMustHaveAnyOfPlayerKeys=killed_surtling
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-InsidePlayerBase=true
-
-[Surtling_JH.0]
-Name=Surtling_JH
-Enabled=True
-PrefabName=Surtling
-HuntPlayer=True
-MaxSpawned=4
-SpawnInterval=20
-SpawnChancePerInterval=100
-SpawnDistance=10
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=
-RequiredEnvironments=
-GroupSizeMin=3
-GroupSizeMax=4
-GroupRadius=1
-GroundOffset=0
-SpawnAtDay=True
-SpawnAtNight=True
-AltitudeMin=1
-AltitudeMax=1000
-TerrainTiltMin=0
-TerrainTiltMax=35
-InForest=True
-OutsideForest=True
-OceanDepthMin=0
-OceanDepthMax=0
-
-/////////MegaBugs_JH/////////
-
-[MegaBugs_JH]
-Name=MegaBugs_JH
-Enabled=True
-Random=True
-Biomes=Meadows, Mistlands
-Duration=90
-StartMessage= The Mist Thickens… and the Hive Marches.
-EndMessage= The March Ends… But the Hive Never Sleeps.
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_goblinking
-NotRequiredGlobalKeys=
-PauseIfNoPlayerInArea=False
-ForceMusic=CombatEventL4
-ForceEnvironment= Mistlands_thunder
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_goblinking
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[MegaBugs_JH.0]
-Name=MegaBugs_JH
-Enabled=true
-PrefabName=SeekerBrute
-MaxSpawned=2
-SpawnInterval=60
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin=0
-AltitudeMax=1000
-GroupRadius=5
-
-[MegaBugs_JH.1]
-Name=Seekers
-Enabled=True
-PrefabName=Seeker
-MaxSpawned=3
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin=0
-AltitudeMax=1000
-GroupRadius=5
-
-/////////Dvergrs/////////
-
-[Dvergrs_JH]
-Name=Dvergrs_JH
-Enabled=True
-Random=True
-Biomes=Meadows, Mistlands
-Duration=90
-StartMessage= The Dvergrs Have Turned against you
-EndMessage= The Mist Closes Around Their Shadows.
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_goblinking
-NotRequiredGlobalKeys=
-PauseIfNoPlayerInArea=False
-ForceMusic=CombatEventL4
-ForceEnvironment= Mistlands_thunder
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_goblinking
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Dvergrs_JH.0]
-Name=Dvergrs_JH
-Enabled=true
-PrefabName=Dverger
-MaxSpawned=2
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin=0
-AltitudeMax=1000
-GroupRadius=5
-
-[Dvergrs_JH.1]
-Name=DvergerMageFire
-Enabled=True
-PrefabName=DvergerMageFire
-MaxSpawned=1
-SpawnInterval=40
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin=0
-AltitudeMax=1000
-GroupRadius=5
-
-[Dvergrs_JH.2]
-Name=DvergerMageIce
-Enabled=True
-PrefabName=DvergerMageIce
-MaxSpawned=1
-SpawnInterval=20
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin=0
-AltitudeMax=1000
-GroupRadius=5
-
-[Dvergrs_JH.3]
-Name=DvergerMageSupport
-Enabled=True
-PrefabName=DvergerMageSupport
-MaxSpawned=1
-SpawnInterval=60
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin=0
-AltitudeMax=1000
-GroupRadius=5
+GroundOffset=5
+MaxLevel=1
+MinLevel=1

```

---

#### custom_raids.supplemental.ragnarok.cfg

**Status**: Modified

**Summary**: +148, -819 changes

**Key Changes**:

**Total changes**: 967 (showing top 8)

• **BoarParty_JH.0.GroupRadius**: `15` *(removed)*
• **BoarParty_JH.0.GroupSizeMax**: `3` *(removed)*
• **BoarParty_JH.0.GroupSizeMin**: `2` *(removed)*
• **BoarParty_JH.0.SpawnChancePerInterval**: `100` *(removed)*
• **BoarParty_JH.0.SpawnDistance**: `10` *(removed)*
• **Cultist_Hunt_JH.0.GroupSizeMax**: `1` *(removed)*
• **Cultist_Hunt_JH.0.GroupSizeMin**: `1` *(removed)*
• **Cultist_Hunt_JH.0.SpawnChancePerInterval**: `100` *(removed)*
• ... and 959 more changes

**Full Diff**:

```diff
--- backup/custom_raids.supplemental.ragnarok.cfg+++ current/custom_raids.supplemental.ragnarok.cfg@@ -1,970 +1,166 @@-/////////Eikthyr_Resistance/////////
 
-[Eikthyr_Resistance_JH]
-Name=Eikthyr_Resistance
+[Ragnarok]
+Name = Ragnarok
+Duration=300
+NearBaseOnly=true
+PauseIfNoPlayerInArea=True
+ForceEnvironment=ThunderStorm
+ForceMusic=CombatEventL2
+StartMessage=Ragnarök has come! The endtimes have begun
+EndMessage=The war has settled... for a while
+Enabled=false
+RequiredGlobalKeys=defeated_dragon
+
+[Ragnarok.0]
+Name=Eikthyr
 Enabled=True
-Random=True
-Biomes=Meadows, BlackForest
-Duration=90
-StartMessage= Eikthyr's death has enraged those still loyal to him.
-EndMessage= The resistance has been quenched.
-NearBaseOnly=False
-RequiredGlobalKeys= defeated_eikthyr
-NotRequiredGlobalKeys=defeated_gdking
-PauseIfNoPlayerInArea=False
-ForceEnvironment= Eikthyr
-ForceMusic=CombatEventL4
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_eikthyr
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=defeated_gdking
-InsidePlayerBase=true
-
-[Eikthyr_Resistance_JH.0]
-Name=Neck
-Enabled=true
-PrefabName=Neck
-MaxSpawned=3
-SpawnInterval=20
-SpawnChancePerInterval=100
+PrefabName=Eikthyr
+MaxSpawned=1
+SpawnInterval=1
+SpawnChancePerInterval=95
 SpawnDistance=0
-GroupSizeMin=2
-GroupSizeMax=3
+SpawnRadiusMin=0
+SpawnRadiusMax=1
+GroupSizeMin=1
+GroupSizeMax=1
 SpawnAtNight=True
 SpawnAtDay=True
 HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
+GroundOffset=0.5
+MaxLevel=1
+MinLevel=1
 
-[Eikthyr_Resistance_JH.1]
-Name=Boar
-Enabled=true
-PrefabName=Boar
-MaxSpawned=3
-SpawnInterval=20
-SpawnChancePerInterval=100
+[Ragnarok.1]
+Name=Bonemass
+Enabled=True
+PrefabName=Bonemass
+MaxSpawned=1
+SpawnInterval=1
+SpawnChancePerInterval=95
 SpawnDistance=0
-GroupSizeMin=2
-GroupSizeMax=3
+SpawnRadiusMin=0
+SpawnRadiusMax=1
+GroupSizeMin=1
+GroupSizeMax=1
 SpawnAtNight=True
 SpawnAtDay=True
 HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
+GroundOffset=0.5
+MaxLevel=1
+MinLevel=1
 
-[Eikthyr_Resistance_JH.2]
-Name=Greyling
-Enabled=true
-PrefabName=Greyling
-MaxSpawned=3
-SpawnInterval=20
-SpawnChancePerInterval=100
+[Ragnarok.2]
+Name=Dragon
+Enabled=True
+PrefabName=Dragon
+MaxSpawned=1
+SpawnInterval=1
+SpawnChancePerInterval=95
 SpawnDistance=0
-GroupSizeMin=2
-GroupSizeMax=3
+SpawnRadiusMin=0
+SpawnRadiusMax=1
+GroupSizeMin=1
+GroupSizeMax=1
 SpawnAtNight=True
 SpawnAtDay=True
 HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
+GroundOffset=0.5
+MaxLevel=1
+MinLevel=1
 
-/////////BoarParty/////////
-
-[BoarParty_JH]
-Name=BoarParty
+[Ragnarok.3]
+Name=gd_king
 Enabled=True
-Random=True
-Biomes=Meadows, BlackForest
-Duration=90
-StartMessage= Stampeeeeede.
-EndMessage= The stampede has ended.
-NearBaseOnly=False
-RequiredGlobalKeys=
-NotRequiredGlobalKeys=defeated_gdking
-PauseIfNoPlayerInArea=False
-ForceEnvironment= Eikthyr
-ForceMusic=CombatEventL4
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=defeated_gdking
-InsidePlayerBase=true
-
-[BoarParty_JH.0]
-Name=Boar
-Enabled=true
-PrefabName=Boar
-MaxSpawned=3
-SpawnInterval=15
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=2
-GroupSizeMax=3
-GroupRadius=15
+PrefabName=gd_king
+MaxSpawned=1
+SpawnInterval=1
+SpawnChancePerInterval=95
+SpawnDistance=0
+SpawnRadiusMin=0
+SpawnRadiusMax=1
+GroupSizeMin=1
+GroupSizeMax=1
 SpawnAtNight=True
 SpawnAtDay=True
 HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
+GroundOffset=0.5
+MaxLevel=1
+MinLevel=1
 
-/////////Troll_Scare/////////
-
-[Troll_Scare_JH]
-Name=Troll_Scare
+[Ragnarok.4]
+Name=Draugr Troopers
 Enabled=True
-Random=True
-Biomes=Meadows, BlackForest
-Duration=90
-StartMessage= You hear loud stomps.
-EndMessage= The rumbling ends.
-NearBaseOnly=False
-RequiredGlobalKeys=KilledTroll, defeated_eikthyr
-PauseIfNoPlayerInArea=False
-ForceEnvironment= Misty
-ForceMusic=boss_queen
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=KilledTroll, defeated_eikthyr
-InsidePlayerBase=true
-
-[Troll_Scare_JH.0]
-Name=Troll
-Enabled=true
-PrefabName=Troll
-MaxSpawned=2
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
+PrefabName=Draugr
+MaxSpawned=30
+SpawnInterval=1
+SpawnChancePerInterval=95
+SpawnDistance=0
 SpawnRadiusMin=0
-SpawnRadiusMax=0
-GroupSizeMin=1
-GroupSizeMax=2
+SpawnRadiusMax=10
+GroupSizeMin=5
+GroupSizeMax=5
+GroupSizeRadius=2
 SpawnAtNight=True
 SpawnAtDay=True
 HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
+GroundOffset=0.5
+MaxLevel=1
+MinLevel=1
 
-/////////Forest_Healers/////////
-
-[Forest_Healers_JH]
-Name=Forest_Healers
+[Ragnarok.5]
+Name=Skelly Troopers
 Enabled=True
-Random=True
-Biomes=Meadows, BlackForest
-Duration=90
-StartMessage= The Elder, sends out his healers.
-EndMessage= The Elder accepts your survival.
-NearBaseOnly=False
-RequiredGlobalKeys= defeated_eikthyr
-PauseIfNoPlayerInArea=False
-ForceEnvironment= DeepForest Mist
-ForceMusic=CombatEventL3
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_eikthyr
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Forest_Healers_JH.0]
-Name=GreydwarfShaman
-Enabled=true
-PrefabName=Greydwarf_Shaman
-MaxSpawned=2
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
+PrefabName=Skeleton
+MaxSpawned=30
+SpawnInterval=1
+SpawnChancePerInterval=95
+SpawnDistance=0
+SpawnRadiusMin=0
+SpawnRadiusMax=10
+GroupSizeMin=5
+GroupSizeMax=5
+GroupSizeRadius=2
 SpawnAtNight=True
 SpawnAtDay=True
 HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
+GroundOffset=0.5
+MaxLevel=1
+MinLevel=1
 
-[Forest_Healers_JH.1]
-Name=Greydwarf
-Enabled=true
-PrefabName=Greydwarf
-MaxSpawned=3
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=2
-GroupSizeMax=4
+[Ragnarok.6]
+Name=Fenring
+Enabled=True
+PrefabName=Fenring
+MaxSpawned=1
+SpawnInterval=1
+SpawnChancePerInterval=95
+SpawnDistance=0
+SpawnRadiusMin=0
+SpawnRadiusMax=1
+GroupSizeMin=1
+GroupSizeMax=1
 SpawnAtNight=True
 SpawnAtDay=True
 HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
+GroundOffset=0.5
+MaxLevel=1
+MinLevel=1
 
-/////////Elders Wrath/////////
-
-[Elders_Wrath_JH]
-Name=Elders_Wrath
+[Ragnarok.7]
+Name=Yagluth
 Enabled=True
-Random=True
-Biomes=Meadows, BlackForest
-Duration=90
-StartMessage= The Elder, sends out his brutes.
-EndMessage= The Elder accepts your survival.
-NearBaseOnly=False
-RequiredGlobalKeys= defeated_eikthyr
-PauseIfNoPlayerInArea=False
-ForceEnvironment= ThunderStorm
-ForceMusic=CombatEventL4
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_eikthyr
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Elders_Wrath_JH.0]
-Name=Greydwarf_Elite
-Enabled=true
-PrefabName=Greydwarf_Elite
-MaxSpawned=2
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
+PrefabName=GoblinKing
+MaxSpawned=1
+SpawnInterval=1
+SpawnChancePerInterval=95
+SpawnDistance=0
+SpawnRadiusMin=0
+SpawnRadiusMax=1
 GroupSizeMin=1
-GroupSizeMax=2
+GroupSizeMax=1
 SpawnAtNight=True
 SpawnAtDay=True
 HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
-
-[Elders_Wrath_JH.1]
-Name=Greydwarf
-Enabled=true
-PrefabName=Greydwarf
-MaxSpawned=3
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=2
-GroupSizeMax=4
-SpawnAtNight=True
-SpawnAtDay=True
-HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
-
-
-/////////Ghost_Town/////////
-
-[Ghost_Town_JH]
-Name=Ghost_Town
-Enabled=True
-Random=True
-Biomes= Meadows, BlackForest
-Duration=90
-StartMessage= The souls of the dead have been set free.
-EndMessage= The souls can finally rest.
-NearBaseOnly=False
-RequiredGlobalKeys= defeated_eikthyr
-NotRequiredGlobalKeys=defeated_gdking
-PauseIfNoPlayerInArea=False
-ForceEnvironment= Misty
-ForceMusic=CombatEventL4
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_eikthyr
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=defeated_gdking
-InsidePlayerBase=true
-
-[Ghost_Town_JH.0]
-Name=Ghost
-Enabled=true
-PrefabName=Ghost
-MaxSpawned=3
-SpawnInterval=20
-SpawnChancePerInterval=100
-SpawnDistance=5
-GroupSizeMin=2
-GroupSizeMax=3
-SpawnAtNight=True
-SpawnAtDay=True
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-
-/////////Revulting_Remains/////////
-
-[Revulting_Remains_JH]
-Name=Revulting_Remains
-Enabled=True
-Random=True
-Biomes=Meadows, BlackForest
-Duration=90
-StartMessage= You see a light flickering in the distance.
-EndMessage= The light goes dim.
-NearBaseOnly=False
-RequiredGlobalKeys= defeated_eikthyr
-PauseIfNoPlayerInArea=False
-ForceEnvironment= GDKing
-ForceMusic=CombatEventL4
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_eikthyr
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Revulting_Remains_JH.0]
-Name=Skeleton_Poison
-Enabled=true
-PrefabName=Skeleton_Poison
-MaxSpawned=2
-SpawnInterval=20
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=2
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-
-/////////Draugr_Daddy/////////
-
-[Draugr_Daddy_JH]
-Name=Draugr_Daddy
-Enabled=True
-Random=True
-Biomes=Meadows, Swamp
-Duration=90
-StartMessage= You spot glowing eyes staring at you.
-EndMessage= You're no longer being watched.
-NearBaseOnly=False
-RequiredGlobalKeys= defeated_gdking
-NotRequiredGlobalKeys= defeated_dragon
-PauseIfNoPlayerInArea=False
-ForceEnvironment= SwampRain
-ForceMusic=CombatEventL4
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_gdking
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=defeated_dragon
-InsidePlayerBase=true
-
-[Draugr_Daddy_JH.0]
-Name=DraugrElite
-Enabled=true
-PrefabName=Draugr_Elite
-MaxSpawned=2
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-
-[Draugr_Daddy_JH.1]
-Name=Draugr_Ranged
-Enabled=true
-PrefabName=Draugr_Ranged
-MaxSpawned=2
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-
-[Draugr_Daddy_JH.2]
-Name=Draugr
-Enabled=true
-PrefabName=Draugr
-MaxSpawned=2
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-
-/////////Floating_Death/////////
-
-[Floating_Death_JH]
-Name=Floating_Death
-Enabled=True
-Random=True
-Biomes=Swamp
-Duration=90
-StartMessage= The Spirits of this realm have unfinished business.
-EndMessage= The Spirits fade back to Hell.
-NearBaseOnly=False
-RequiredGlobalKeys= defeated_gdking
-PauseIfNoPlayerInArea=False
-ForceEnvironment= SunkenCrypt
-ForceMusic=CombatEventL4
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_gdking
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Floating_Death_JH.0]
-Name=Wraith
-Enabled=true
-PrefabName=Wraith
-MaxSpawned=2
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=5
-GroupSizeMin=2
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-
-/////////Cultist_Hunt/////////
-
-[Cultist_Hunt_JH]
-Name=Cultist_Hunt
-Enabled=True
-Random=True
-Biomes=Meadows, Mountain, DeepNorth
-Duration=90
-StartMessage= You've walked to close to their den, now perish.
-EndMessage= The creatures head back to their den.
-NearBaseOnly=False
-RequiredGlobalKeys= KilledBat
-PauseIfNoPlayerInArea=False
-ForceEnvironment= GoblinKing
-ForceMusic=CombatEventL4
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=KilledBat
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Cultist_Hunt_JH.0]
-Name=Fenring_Cultist
-Enabled=true
-PrefabName=Fenring_Cultist
-MaxSpawned=1
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=1
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-
-[Cultist_Hunt_JH.1]
-Name=Ulv
-Enabled=true
-PrefabName=Ulv
-MaxSpawned=3
-SpawnInterval=15
-SpawnChancePerInterval=100
-SpawnDistance=5
-GroupSizeMin=2
-GroupSizeMax=3
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-
-/////////TarParty/////////
-
-[TarParty_JH]
-Name=TarParty
-Enabled=True
-Random=True
-Biomes=Plains
-Duration=60
-StartMessage= Some sticky black blobs 
-EndMessage= I'm covered in tar...
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_dragon
-PauseIfNoPlayerInArea=False
-ForceMusic=CombatEventL2
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_dragon
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[TarParty_JH.0]
-Name=TarMob
-Enabled=true
-PrefabName=BlobTar
-MaxSpawned=3
-SpawnInterval=20
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=2
-GroupSizeMax=3
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-
-/////////Serpent_Rush/////////
-
-[Serpent_Rush_JH]
-Name=Serpent_Rush
-Enabled=True
-Random=True
-Biomes=Ocean
-Duration=90
-StartMessage= What's that shining light under the water?!
-EndMessage= The serpents swim to the depths
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_gdking
-PauseIfNoPlayerInArea=False
-ForceMusic=boss_queen
-ForceEnvironment= ThunderStorm
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_gdking
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Serpent_Rush_JH.0]
-Name=Serpent
-Enabled=true
-PrefabName=Serpent
-MaxSpawned=2
-SpawnInterval=60
-SpawnChancePerInterval=100
-SpawnDistance=15
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-GroupSizeMin=2
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = -75
-AltitudeMax = 1000
-GroupRadius= 20
-
-/////////Mosquitos/////////
-
-[Mosquitos_JH]
-Name=Mosquitos
-Enabled=True
-Random=True
-Biomes=Meadows, Plains
-Duration=90
-StartMessage= The Air Screams With Wings and Death…
-EndMessage= The Buzzing Fades… But Your Heart Still Races.
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_dragon
-PauseIfNoPlayerInArea=False
-ForceMusic=CombatEventL2
-ForceEnvironment= Misty
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_dragon
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Mosquitos_JH.0]
-Name=Mosquitos
-Enabled=true
-PrefabName=Deathsquito
-MaxSpawned=4
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=30
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-GroupSizeMin=2
-GroupSizeMax=4
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-GroupRadius= 10
-
-[RootedAlive_JH]
-Name=RootedAlive
-Enabled=True
-Random=True
-Biomes= Meadows, Swamp
-Duration=90
-StartMessage= The land Groans With Unnatural Life…
-EndMessage= You survived the land's wrath. But its heart still beats.
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_gdking
-PauseIfNoPlayerInArea=False
-ForceMusic=boss_queen
-ForceEnvironment= SwampRain
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_gdking
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[RootedAlive_JH.0]
-Name=RootedAlive
-Enabled=true
-PrefabName=Abomination
-MaxSpawned=1
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=1
-HuntPlayer=True
-AltitudeMin=-2
-AltitudeMax=1000
-GroupRadius=10
-
-/////////Stony/////////
-
-[Stony_JH]
-Name=Stony
-Enabled=True
-Random=True
-Biomes=Meadows, Mountain
-Duration=90
-StartMessage= The Mountain Walks…
-EndMessage= The Stones Fall Silent Once More.
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_bonemass
-PauseIfNoPlayerInArea=False
-ForceMusic=CombatEventL4
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_bonemass
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Stony_JH.0]
-Name=Stony
-Enabled=true
-PrefabName=StoneGolem
-MaxSpawned=2
-SpawnInterval=45
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-GroupRadius= 10
-
-/////////FurryMadness/////////
-[FurryMadness_JH]
-Name=FurryMadness
-Enabled=True
-Random=True
-Biomes=Meadows, Plains
-Duration=90
-StartMessage= The Land Itself Begins to Move…
-EndMessage= The Thundering Steps Grow Distant.
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_dragon
-NotRequiredGlobalKeys=
-PauseIfNoPlayerInArea=False
-ForceMusic=CombatEventL4
-ForceEnvironment= 
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_dragon
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[FurryMadness_JH.0]
-Name=FurryMadness
-Enabled=true
-PrefabName=Lox
-MaxSpawned=2
-SpawnInterval=20
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-GroupRadius= 10
-
-/////////Rage/////////
-
-[Rage_JH]
-Name=Rage
-Enabled=True
-Random=True
-Biomes=Meadows, Plains
-Duration=90
-StartMessage= The Brutes have come to smash, burn, and bellow.
-EndMessage= This was a warning — and the Brutes never grunt alone.
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_dragon
-NotRequiredGlobalKeys=
-PauseIfNoPlayerInArea=False
-ForceMusic=CombatEventL4
-ForceEnvironment= Misty
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_dragon
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Rage_JH.0]
-Name=Rage
-Enabled=true
-PrefabName=GoblinBrute
-MaxSpawned=2
-SpawnInterval=20
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-GroupRadius= 10
-
-/////////MutatedNecks/////////
-
-[MutatedNecks_JH]
-Name=MutatedNecks
-Enabled=True
-Random=True
-Biomes=Meadows, AshLands
-Duration=90
-StartMessage= a horde of bulky necks?
-EndMessage= the mutated necks retreat
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_queen
-NotRequiredGlobalKeys=
-PauseIfNoPlayerInArea=False
-ForceMusic=CombatEventL4
-ForceEnvironment= 
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_queen
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[MutatedNecks_JH.0]
-Name=MutatedNecks
-Enabled=true
-PrefabName=Asksvin
-MaxSpawned=2
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=2
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-GroupRadius= 10
-
-/////////Valkyrie/////////
-
-[Valkyrie_JH]
-Name=Valkyrie
-Enabled=True
-Random=True
-Biomes=Meadows, AshLands
-Duration=90
-StartMessage= You were chosen once. Now you are judged
-EndMessage= They return to the void between worlds — until Valhalla weeps again
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_queen
-NotRequiredGlobalKeys=
-PauseIfNoPlayerInArea=False
-ForceMusic=CombatEventL4
-ForceEnvironment= 
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_queen
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Valkyrie_JH.0]
-Name=Valkyrie
-Enabled=true
-PrefabName=FallenValkyrie
-MaxSpawned=1
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin = 0
-AltitudeMax = 1000
-GroupRadius= 10
-
-/////////Surtling/////////
-
-[Surtling_JH]
-Name=Surtling_JH
-Enabled=True
-Random=True
-Biomes=Meadows, Swamp, BlackForest
-Duration=120
-StartMessage= The land burns — and they dance in its ashes.
-EndMessage= The fire sleeps. But it always dreams of burning again.
-NearBaseOnly=False
-RequiredGlobalKeys=killed_surtling
-NotRequiredGlobalKeys=
-PauseIfNoPlayerInArea=False
-ForceEnvironment=Ashlands_CinderRain
-ForceMusic=CombatEventL3
-ConditionPlayerMustHaveAnyOfPlayerKeys=killed_surtling
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-InsidePlayerBase=true
-
-[Surtling_JH.0]
-Name=Surtling_JH
-Enabled=True
-PrefabName=Surtling
-HuntPlayer=True
-MaxSpawned=4
-SpawnInterval=20
-SpawnChancePerInterval=100
-SpawnDistance=10
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=
-RequiredEnvironments=
-GroupSizeMin=3
-GroupSizeMax=4
-GroupRadius=1
-GroundOffset=0
-SpawnAtDay=True
-SpawnAtNight=True
-AltitudeMin=1
-AltitudeMax=1000
-TerrainTiltMin=0
-TerrainTiltMax=35
-InForest=True
-OutsideForest=True
-OceanDepthMin=0
-OceanDepthMax=0
-
-/////////MegaBugs_JH/////////
-
-[MegaBugs_JH]
-Name=MegaBugs_JH
-Enabled=True
-Random=True
-Biomes=Meadows, Mistlands
-Duration=90
-StartMessage= The Mist Thickens… and the Hive Marches.
-EndMessage= The March Ends… But the Hive Never Sleeps.
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_goblinking
-NotRequiredGlobalKeys=
-PauseIfNoPlayerInArea=False
-ForceMusic=CombatEventL4
-ForceEnvironment= Mistlands_thunder
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_goblinking
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[MegaBugs_JH.0]
-Name=MegaBugs_JH
-Enabled=true
-PrefabName=SeekerBrute
-MaxSpawned=2
-SpawnInterval=60
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin=0
-AltitudeMax=1000
-GroupRadius=5
-
-[MegaBugs_JH.1]
-Name=Seekers
-Enabled=True
-PrefabName=Seeker
-MaxSpawned=3
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin=0
-AltitudeMax=1000
-GroupRadius=5
-
-/////////Dvergrs/////////
-
-[Dvergrs_JH]
-Name=Dvergrs_JH
-Enabled=True
-Random=True
-Biomes=Meadows, Mistlands
-Duration=90
-StartMessage= The Dvergrs Have Turned against you
-EndMessage= The Mist Closes Around Their Shadows.
-NearBaseOnly=False
-RequiredGlobalKeys=defeated_goblinking
-NotRequiredGlobalKeys=
-PauseIfNoPlayerInArea=False
-ForceMusic=CombatEventL4
-ForceEnvironment= Mistlands_thunder
-ConditionMustNotBeNearPrefab=RDSkeletonPole, RDSittingSkeleton, RDCross
-ConditionPlayerMustHaveAnyOfPlayerKeys=defeated_goblinking
-ConditionPlayerMustNotHaveAnyOfPlayerKeys=
-InsidePlayerBase=true
-
-[Dvergrs_JH.0]
-Name=Dvergrs_JH
-Enabled=true
-PrefabName=Dverger
-MaxSpawned=2
-SpawnInterval=30
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin=0
-AltitudeMax=1000
-GroupRadius=5
-
-[Dvergrs_JH.1]
-Name=DvergerMageFire
-Enabled=True
-PrefabName=DvergerMageFire
-MaxSpawned=1
-SpawnInterval=40
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin=0
-AltitudeMax=1000
-GroupRadius=5
-
-[Dvergrs_JH.2]
-Name=DvergerMageIce
-Enabled=True
-PrefabName=DvergerMageIce
-MaxSpawned=1
-SpawnInterval=20
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin=0
-AltitudeMax=1000
-GroupRadius=5
-
-[Dvergrs_JH.3]
-Name=DvergerMageSupport
-Enabled=True
-PrefabName=DvergerMageSupport
-MaxSpawned=1
-SpawnInterval=60
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=1
-GroupSizeMax=2
-HuntPlayer=True
-AltitudeMin=0
-AltitudeMax=1000
-GroupRadius=5
+GroundOffset=0.5
+MaxLevel=1
+MinLevel=1

```

---


### Drop That

*Files in this category with changes from RelicHeim backup:*

#### drop_that.cfg

**Status**: Modified

**Summary**: ~1 changes

**Key Changes**:

**Total changes**: 1 (showing top 1)

• **Performance.AlwaysAutoStack**: `false` → `true`

**Full Diff**:

```diff
--- backup/drop_that.cfg+++ current/drop_that.cfg@@ -85,7 +85,7 @@ ## Eg. 35 coin stack, instead of 35 individual 1 coin drops.
 # Setting type: Boolean
 # Default value: false
-AlwaysAutoStack = false
+AlwaysAutoStack = true
 
 ## When greater than 0, will limit the maximum number of items dropped at a time. This is intended for guarding against multipliers.
 ## Eg. if limit is 100, and attempting to drop 200 coins, only 100 will be dropped.

```

---

#### drop_that.character_drop.cfg

**Status**: Modified

**Summary**: +693, -870 changes

**Key Changes**:

**Total changes**: 1563 (showing top 8)

• **Abomination.0.AmountMax**: `1` *(removed)*
• **Abomination.0.AmountMin**: `1` *(removed)*
• **Abomination.0.ChanceToDrop**: `15` *(removed)*
• **Abomination.0.ScaleByLevel**: `False` *(removed)*
• **Abomination.1.AmountLimit**: `20` *(removed)*
• **Abomination.1.AmountMax**: `5` *(removed)*
• **Abomination.1.AmountMin**: `5` *(removed)*
• **Abomination.1.ChanceToDrop**: `100` *(removed)*
• ... and 1555 more changes

**Full Diff**:

```diff
--- backup/drop_that.character_drop.cfg+++ current/drop_that.character_drop.cfg@@ -1,1171 +1,894 @@-########################
-# IDs: Vanilla and 50-59
-########################
-
-####################
-# Meadows
-####################
-
-[Greyling.50]
-PrefabName=Flint
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-[Greyling.51]
-PrefabName=Wood
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-####################
-
-[Deer.2]
-PrefabName=TrophyDeer
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=25
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Deer.50]
-PrefabName=CookedDeerMeat
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-AmountLimit=1
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=False
-ConditionKilledWithStatuses=Burning
-ConditionKilledByDamageType= Fire
-DisableResourceModifierScaling=True
-
-####################
-
-[Boar.50]
-PrefabName=CookedMeat
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-AmountLimit=1
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=False
-ConditionKilledWithStatuses=Burning
-ConditionKilledByDamageType= Fire
-DisableResourceModifierScaling=True
-
-####################
-
-[Neck.50]
-PrefabName=NeckTailGrilled
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-AmountLimit=1
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=False
-ConditionKilledWithStatuses=Burning
-ConditionKilledByDamageType= Fire
-DisableResourceModifierScaling=True
-
-####################
-# BlackForest
-####################
-
-[Ghost.0]
-PrefabName=Amber
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Ghost.1]
-PrefabName=Ruby
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Ghost.2]
-PrefabName=AncientArtifact_TW
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=25
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[Greydwarf.0]
-PrefabName=GreydwarfEye
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=True
-ConditionKilledByEntityType=Player
-DisableResourceModifierScaling=True
-
-[Greydwarf.4]
-PrefabName=TrophyGreydwarf
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-ConditionKilledByEntityType=Player
-DisableResourceModifierScaling=True
-
-[Greydwarf.50]
-PrefabName=GreydwarfEye
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=True
-ConditionKilledWithStatus=Burning
-ConditionKilledByDamageType=Fire
-DisableResourceModifierScaling=True
-
-[Greydwarf.51]
-PrefabName=AncientSeed
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=0.2
-DropOnePerPlayer=False
-ScaleByLevel=True
-ConditionKilledByEntityType=Player
-DisableResourceModifierScaling=True
-
-####################
-
-[Greydwarf_Elite.0]
-PrefabName=GreydwarfEye
-EnableConfig=True
-AmountMin=2
-AmountMax=2
-ChanceToDrop=75
-DropOnePerPlayer=False
-ScaleByLevel=True
-ConditionKilledByEntityType=Player
-DisableResourceModifierScaling=True
-
-####################
-
-[Greydwarf_Shaman.0]
-PrefabName=GreydwarfEye
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=75
-DropOnePerPlayer=False
-ScaleByLevel=True
-ConditionKilledByEntityType=Player
-DisableResourceModifierScaling=True
-
-####################
-
-[Troll.0]
-PrefabName=Ruby
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[Troll.1]
-PrefabName=TrophyFrostTroll
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Troll.2]
-PrefabName=TrollHide
-EnableConfig=True
-AmountMin=3
-AmountMax=5
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-####################
-# Swamp
-####################
-
-[Leech.50]
-PrefabName=FishRaw
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=20
-DropOnePerPlayer=False
-ScaleByLevel=true
-AmountLimit=1
-DisableResourceModifierScaling=True
-
-####################
-
-[BlobElite.1]
-PrefabName=IronScrap
-EnableConfig=True
-AmountMin=2
-AmountMax=2
-ChanceToDrop=33
-DropOnePerPlayer=False
-ScaleByLevel=True
-ConditionGlobalKeys=defeated_gdking
-DisableResourceModifierScaling=True
-
-####################
-
-[Abomination.0]
-PrefabName=TrophyAbomination
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Abomination.1]
-PrefabName=Root
-EnableConfig=True
-AmountMin=5
-AmountMax=5
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=20
-DisableResourceModifierScaling=True
-
-[Abomination.52]
-PrefabName=ElderBark
-EnableConfig=True
-AmountMin=2
-AmountMax=4
-ChanceToDrop=20
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-####################
-
-[Draugr.2]
-PrefabName=RottenPelt_TW
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=25
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-[Draugr.50]
-PrefabName=TrophyDraugrElite
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=0.2
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=1
-DisableResourceModifierScaling=True
-
-[Draugr.51]
-PrefabName=WitheredBone
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=5
-DropOnePerPlayer=False
-ScaleByLevel=False
-AmountLimit=3
-DisableResourceModifierScaling=True
-
-####################
-
-[Draugr_Ranged.2]
-PrefabName=RottenPelt_TW
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=25
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-[Draugr_Ranged.50]
-PrefabName=TrophyDraugrElite
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=0.2
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=1
-DisableResourceModifierScaling=True
-
-[Draugr_Ranged.51]
-PrefabName=WitheredBone
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=5
-DropOnePerPlayer=False
-ScaleByLevel=False
-AmountLimit=3
-DisableResourceModifierScaling=True
-
-####################
-
-[Draugr_Elite.2]
-PrefabName=RottenPelt_TW
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-[Draugr_Elite.50]
-PrefabName=WitheredBone
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=5
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[Wraith.0]
-PrefabName=TrophyWraith
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Wraith.1]
-PrefabName=Chain
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Wraith.50]
-PrefabName=TurnipSeeds
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[Surtling.0]
-PrefabName=Coal
-Enable=true
-EnableConfig=true
-AmountMin=4
-AmountMax=5
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[Surtling.1]
-PrefabName=SurtlingCore
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=1
-ChanceToDrop=75
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-ConditionKilledByEntityType=Player
-
-[Surtling.2]
-PrefabName=TrophySurtling
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Surtling.50]
-PrefabName=SurtlingCore
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=1
-ChanceToDrop=25
-DropOnePerPlayer=false
-ScaleByLevel=true
-ConditionKilledWithStatuses=Wet
-
-[BogWitchKvastur.2]
-PrefabName=TrophyKvastur
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=1
-ChanceToDrop=50
-DropOnePerPlayer=false
-ScaleByLevel=false
-DisableResourceModifierScaling=false
-ConditionNotDay=false
-ConditionNotAfternoon=false
-ConditionNotNight=false
-
-####################
-# Mountain
-####################
-
-[Wolf.51]
-PrefabName=WolfClaw
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-ConditionNotCreatureStates=Tamed
-DisableResourceModifierScaling=True
-
-####################
-
-[Bat.50]
-PrefabName=Bloodbag
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-####################
-
-[Fenring.51]
-PrefabName=WolfHairBundle
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Fenring.52]
-PrefabName=WolfClaw
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=20
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[Ulv.50]
-PrefabName=WolfHairBundle
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Ulv.51]
-PrefabName=WolfClaw
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[Fenring_Cultist.51]
-PrefabName=WolfHairBundle
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Fenring_Cultist.52]
-PrefabName=WolfClaw
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[StoneGolem.0]
-PrefabName=TrophySGolem
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[StoneGolem.51]
-PrefabName=SilverOre
-EnableConfig=True
-AmountMin=2
-AmountMax=4
-ChanceToDrop=20
-DropOnePerPlayer=False
-ScaleByLevel=False
-ConditionGlobalKeys=defeated_bonemass
-DisableResourceModifierScaling=True
-
-####################
-
-[Hatchling.50]
-PrefabName=DragonEgg
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=0.5
-DropOnePerPlayer=False
-ScaleByLevel=False
-AmountLimit=1
-DisableResourceModifierScaling=False
-
-###################
-# Plains
-###################
-
-[Lox.0]
-PrefabName=LoxMeat
-EnableConfig=True
-AmountMin=2
-AmountMax=4
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-
-####################
-
-[Goblin.0]
-PrefabName=AmberPearl
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=1
-ChanceToDrop=25
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[Goblin.1]
-PrefabName=BlackMetalScrap
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=10
-ConditionGlobalKeys=defeated_dragon
-DisableResourceModifierScaling=True
-
-[Goblin.2]
-PrefabName=TrophyGoblin
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Goblin.50]
-PrefabName=GoblinScraps_TW
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=25
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=10
-ConditionGlobalKeys=defeated_dragon
-DisableResourceModifierScaling=True
-
-####################
-
-[GoblinArcher.0]
-PrefabName=AmberPearl
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=1
-ChanceToDrop=25
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[GoblinArcher.1]
-PrefabName=BlackMetalScrap
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=10
-ConditionGlobalKeys=defeated_dragon
-DisableResourceModifierScaling=True
-
-[GoblinArcher.2]
-PrefabName=TrophyGoblin
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[GoblinArcher.50]
-PrefabName=GoblinScraps_TW
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=25
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=10
-ConditionGlobalKeys=defeated_dragon
-DisableResourceModifierScaling=True
-
-####################
-
-[GoblinBrute.0]
-PrefabName=AmberPearl
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=25
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[GoblinBrute.1]
-PrefabName=BlackMetalScrap
-EnableConfig=True
-AmountMin=2
-AmountMax=4
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=20
-DisableResourceModifierScaling=False
-ConditionGlobalKeys=defeated_dragon
-
-[GoblinBrute.2]
-PrefabName=GoblinTotem
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=False
-
-[GoblinBrute.3]
-PrefabName=TrophyGoblinBrute
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=False
-
-[GoblinBrute.51]
-PrefabName=GoblinScraps_TW
-EnableConfig=True
-AmountMin=2
-AmountMax=4
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=20
-ConditionGlobalKeys=defeated_dragon
-DisableResourceModifierScaling=True
-
-####################
-
-[GoblinShaman.0]
-PrefabName=Ruby
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=25
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[GoblinShaman.1]
-PrefabName=BlackMetalScrap
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=10
-ConditionGlobalKeys=defeated_dragon
-DisableResourceModifierScaling=True
-
-[GoblinShaman.50]
-PrefabName=GoblinScraps_TW
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=10
-ConditionGlobalKeys=defeated_dragon
-DisableResourceModifierScaling=True
-
-[GoblinShaman.51]
-PrefabName=GoblinTotem
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=20
-DropOnePerPlayer=False
-ScaleByLevel=False
-ConditionGlobalKeys=defeated_dragon
-DisableResourceModifierScaling=True
-
-####################
-# Ocean
-####################
-
-[Serpent.0]
-PrefabName=TrophySerpent
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=33
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Serpent.1]
-PrefabName=SerpentMeat
-EnableConfig=True
-AmountMin=4
-AmountMax=6
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=18
-DisableResourceModifierScaling=True
-
-[Serpent.2]
-PrefabName=SerpentScale
-EnableConfig=True
-AmountMin=4
-AmountMax=6
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=18
-DisableResourceModifierScaling=True
-
-####################
-# Mistlands
-####################
-
-[Gjall.0]
-PrefabName=Bilebag
-EnableConfig=True
-AmountMin=2
-AmountMax=4
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-
-[Gjall.1]
-PrefabName=TrophyGjall
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[SeekerBrute.2]
-PrefabName=TrophySeekerBrute
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[Dverger.0]
-PrefabName=Softtissue
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[Dverger.1]
-PrefabName=BlackMarble
-Enable=false
-EnableConfig=true
-AmountMin=1
-AmountMax=2
-ChanceToDrop=50
-DropOnePerPlayer=false
-ScaleByLevel=false
-DisableResourceModifierScaling=True
-
-[Dverger.2]
-PrefabName=Amber
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[Dverger.3]
-PrefabName=TrophyDvergr
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Dverger.50]
-PrefabName=JuteBlue
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-[Dverger.51]
-PrefabName=BlackCore
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=5
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[DvergerMage.0]
-PrefabName=Softtissue
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[DvergerMage.2]
-PrefabName=Amber
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[DvergerMage.50]
-PrefabName=JuteBlue
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-[DvergerMage.51]
-PrefabName=BlackCore
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=5
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[DvergerMageFire.2]
-PrefabName=Amber
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-####################
-
-[DvergerMageIce.2]
-PrefabName=Amber
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-####################
-
-[DvergerMageSupport.2]
-PrefabName=Amber
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[DvergerMageSupport.50]
-PrefabName=DvergrKeyFragment
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=1
-ChanceToDrop=5
-DropOnePerPlayer=false
-ScaleByLevel=false
-AmountLimit=1
-DisableResourceModifierScaling=false
-
-####################
-# Ashlands
-####################
-
-[BonemawSerpent.0]
-PrefabName=TrophyBonemawSerpent
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=33
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[BonemawSerpent.1]
-PrefabName=BoneMawSerpentMeat
-EnableConfig=True
-AmountMin=4
-AmountMax=6
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=18
-DisableResourceModifierScaling=True
-
-[BonemawSerpent.2]
-PrefabName=BonemawSerpentTooth
-EnableConfig=True
-AmountMin=4
-AmountMax=6
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=18
-DisableResourceModifierScaling=True
-
-[BonemawSerpent.50]
-PrefabName=GemstoneGreen
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-ConditionGlobalKeys=defeated_queen
-ConditionKilledByEntityType=Player
-AmountLimit=1
-
-####################
-
-[FallenValkyrie.50]
-PrefabName=BlackCore
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-[FallenValkyrie.51]
-PrefabName=GemstoneBlue
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-ConditionGlobalKeys=defeated_queen
-ConditionKilledByEntityType=Player
-AmountLimit=1
-
-####################
-
-[Morgen.50]
-PrefabName=GemstoneRed
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-ConditionGlobalKeys=defeated_queen
-AmountLimit=1
-
-[Morgen_NonSleeping.50]
-PrefabName=GemstoneRed
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-ConditionGlobalKeys=defeated_queen
-AmountLimit=1
-
-####################
-
-[BlobLava.50]
-PrefabName=MoltenCore
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-ConditionKilledByEntityType=Player
-
-####################
-
-[DvergerAshlands.1]
-PrefabName=BlackMarble
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=2
-ChanceToDrop=50
-DropOnePerPlayer=false
-ScaleByLevel=false
-DisableResourceModifierScaling=false
-
-[DvergerAshlands.2]
-PrefabName=Amber
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True+# Auto-generated file for adding CharacterDrop configurations.
+# This file is empty by default. It is intended to contains changes only, to avoid unintentional modifications as well as to reduce unnecessary performance cost.
+# Full documentation can be found at https://github.com/ASharpPen/Valheim.DropThat/wiki.
+
+[Leech.1]
+PrefabName = Ooze
+EnableConfig = true
+SetAmountMin = 2
+SetAmountMax = 4
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Leech.2]
+PrefabName = BloodPearl
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Leech.3]
+PrefabName = ReagentRare
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.05
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Leech.4]
+PrefabName = Bloodbag
+EnableConfig = true
+SetAmountMin = 2
+SetAmountMax = 5
+SetChanceToDrop = 0.8
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Leech.5]
+PrefabName = TrophyLeech
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Leech.6]
+PrefabName = Entrails
+EnableConfig = true
+SetAmountMin = 2
+SetAmountMax = 4
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Leech.7]
+PrefabName = AmberPearl
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.2
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Leech.8]
+PrefabName = SwordIron
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.05
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Fox_TW.1]
+PrefabName = LeatherScraps
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Fox_TW.2]
+PrefabName = RawMeat
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Sheep_TW.1]
+PrefabName = DeerHide
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Sheep_TW.2]
+PrefabName = RawMeat
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Razorback_TW.1]
+PrefabName = LeatherScraps
+EnableConfig = true
+SetAmountMin = 2
+SetAmountMax = 3
+SetChanceToDrop = 0.75
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Razorback_TW.2]
+PrefabName = RawMeat
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[BlackBear_TW.1]
+PrefabName = DeerHide
+EnableConfig = true
+SetAmountMin = 2
+SetAmountMax = 3
+SetChanceToDrop = 0.75
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[BlackBear_TW.2]
+PrefabName = RawMeat
+EnableConfig = true
+SetAmountMin = 2
+SetAmountMax = 4
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[GDAncientShaman_TW.1]
+PrefabName = GreydwarfEye
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[GDAncientShaman_TW.2]
+PrefabName = Resin
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[GreydwarfMage_TW.1]
+PrefabName = GreydwarfEye
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[GreydwarfMage_TW.2]
+PrefabName = Coal
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[RottingElk_TW.1]
+PrefabName = Entrails
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[RottingElk_TW.2]
+PrefabName = LeatherScraps
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Crawler_TW.1]
+PrefabName = Chitin
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Crawler_TW.2]
+PrefabName = Coins
+EnableConfig = true
+SetAmountMin = 5
+SetAmountMax = 20
+SetChanceToDrop = 0.2
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[HelWraith_TW.1]
+PrefabName = Chain
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[HelWraith_TW.2]
+PrefabName = TrophyWraith
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.1
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[SkeletonMage_TW.1]
+PrefabName = BoneFragments
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 3
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[SkeletonMage_TW.2]
+PrefabName = Ruby
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[ObsidianGolem_TW.1]
+PrefabName = Obsidian
+EnableConfig = true
+SetAmountMin = 2
+SetAmountMax = 5
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[ObsidianGolem_TW.2]
+PrefabName = Crystal
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 3
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[GrizzlyBear_TW.1]
+PrefabName = WolfPelt
+EnableConfig = true
+SetAmountMin = 2
+SetAmountMax = 3
+SetChanceToDrop = 0.75
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[GrizzlyBear_TW.2]
+PrefabName = RawMeat
+EnableConfig = true
+SetAmountMin = 2
+SetAmountMax = 4
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[FenringMage_TW.1]
+PrefabName = WolfFang
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.75
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[FenringMage_TW.2]
+PrefabName = FreezeGland
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Prowler_TW.1]
+PrefabName = WolfPelt
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.75
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Prowler_TW.2]
+PrefabName = Coins
+EnableConfig = true
+SetAmountMin = 10
+SetAmountMax = 30
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[GoblinMage_TW.1]
+PrefabName = BlackMetalScrap
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.75
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[GoblinMage_TW.2]
+PrefabName = Coins
+EnableConfig = true
+SetAmountMin = 5
+SetAmountMax = 20
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[CorruptedDvergerMage_TW.1]
+PrefabName = BlackCore
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[CorruptedDvergerMage_TW.2]
+PrefabName = Softtissue
+EnableConfig = true
+SetAmountMin = 2
+SetAmountMax = 3
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[SummonedSeeker_TW.1]
+PrefabName = Chitin
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.75
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[SummonedSeeker_TW.2]
+PrefabName = Mandible
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[TempestNeck.1]
+PrefabName = NeckTail
+EnableConfig = true
+SetAmountMin = 5
+SetAmountMax = 10
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[TempestNeck.2]
+PrefabName = kg_EnchantSkillScroll_F
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[TempestNeck.3]
+PrefabName = Coins
+EnableConfig = true
+SetAmountMin = 40
+SetAmountMax = 80
+SetChanceToDrop = 0.75
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[TempestNeck.4]
+PrefabName = kg_EnchantSkillScroll_B
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.35
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[TempestNeck.5]
+PrefabName = Thunderstone
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[TempestNeck.6]
+PrefabName = kg_EnchantSkillScroll_A
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.2
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Dragon.1]
+PrefabName = FrostScale
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 3
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Dragon.2]
+PrefabName = Silver
+EnableConfig = true
+SetAmountMin = 10
+SetAmountMax = 20
+SetChanceToDrop = 0.3
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Dragon.3]
+PrefabName = LegendaryWeaponSchematic
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.05
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Dragon.4]
+PrefabName = mmo_orb7
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[MagmaGolem.1]
+PrefabName = FlametalNew
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.75
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[MagmaGolem.2]
+PrefabName = Obsidian
+EnableConfig = true
+SetAmountMin = 2
+SetAmountMax = 5
+SetChanceToDrop = 0.75
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[MagmaGolem.3]
+PrefabName = MagmaCore
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.05
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[MagmaGolem.4]
+PrefabName = mmo_orb7
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.1
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[SeekerQueen.1]
+PrefabName = Silk
+EnableConfig = true
+SetAmountMin = 3
+SetAmountMax = 5
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[SeekerQueen.2]
+PrefabName = TrophySeekerQueen
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[SeekerQueen.3]
+PrefabName = DustRare
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 3
+SetChanceToDrop = 0.1
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[SeekerQueen.4]
+PrefabName = RunestoneRare
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.05
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[SeekerQueen.5]
+PrefabName = EssenceRare
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.05
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[SeekerQueen.6]
+PrefabName = mmo_orb7
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.1
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[SeekerQueen.7]
+PrefabName = DustEpic
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.05
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[SeekerQueen.8]
+PrefabName = mmo_orb8
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.05
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[TempestSerpent.1]
+PrefabName = SerpentScale
+EnableConfig = true
+SetAmountMin = 10
+SetAmountMax = 15
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[TempestSerpent.2]
+PrefabName = Chitin
+EnableConfig = true
+SetAmountMin = 10
+SetAmountMax = 20
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[TempestSerpent.3]
+PrefabName = Harpoon
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.03
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[TempestSerpent.4]
+PrefabName = SpearChitin
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.03
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[TempestSerpent.5]
+PrefabName = TrophySerpent
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[TempestSerpent.6]
+PrefabName = SerpentMeat
+EnableConfig = true
+SetAmountMin = 10
+SetAmountMax = 20
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[TempestSerpent.7]
+PrefabName = Coins
+EnableConfig = true
+SetAmountMin = 50
+SetAmountMax = 100
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[TempestSerpent.8]
+PrefabName = Thunderstone
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.2
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[RoyalLox.1]
+PrefabName = RoyalLoxPelt
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[RoyalLox.2]
+PrefabName = LoxMeat
+EnableConfig = true
+SetAmountMin = 6
+SetAmountMax = 10
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[RoyalLox.3]
+PrefabName = Coins
+EnableConfig = true
+SetAmountMin = 50
+SetAmountMax = 100
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[RoyalLox.4]
+PrefabName = BlackMetalScrap
+EnableConfig = true
+SetAmountMin = 10
+SetAmountMax = 20
+SetChanceToDrop = 0.75
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[RoyalLox.5]
+PrefabName = LinenThread
+EnableConfig = true
+SetAmountMin = 10
+SetAmountMax = 20
+SetChanceToDrop = 0.75
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[RoyalLox.6]
+PrefabName = TrophyLox
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[AvalancheDrake.1]
+PrefabName = FreezeGland
+EnableConfig = true
+SetAmountMin = 2
+SetAmountMax = 4
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[AvalancheDrake.2]
+PrefabName = Crystal
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.3
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[AvalancheDrake.3]
+PrefabName = DragonTear
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[AvalancheDrake.4]
+PrefabName = DustEpic
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.2
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[AvalancheDrake.5]
+PrefabName = RunestoneEpic
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.025
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[AvalancheDrake.6]
+PrefabName = EssenceEpic
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.025
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[AvalancheDrake.7]
+PrefabName = mmo_orb5
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.2
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[AvalancheDrake.8]
+PrefabName = mmo_orb6
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[AvalancheDrake.9]
+PrefabName = mmo_orb7
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.1
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[CoinTroll.1]
+PrefabName = TrophyTroll
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[CoinTroll.2]
+PrefabName = Coins
+EnableConfig = true
+SetAmountMin = 250
+SetAmountMax = 500
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[CoinTroll.3]
+PrefabName = FineWood
+EnableConfig = true
+SetAmountMin = 10
+SetAmountMax = 20
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[CoinTroll.4]
+PrefabName = RunestoneEpic
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[CoinTroll.5]
+PrefabName = IronScrap
+EnableConfig = true
+SetAmountMin = 5
+SetAmountMax = 10
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[CoinTroll.6]
+PrefabName = YggdrasilWood
+EnableConfig = true
+SetAmountMin = 10
+SetAmountMax = 20
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[WeaverQueen.1]
+PrefabName = Silk
+EnableConfig = true
+SetAmountMin = 5
+SetAmountMax = 8
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[WeaverQueen.2]
+PrefabName = TrophySeekerQueen
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[WeaverQueen.3]
+PrefabName = DustRare
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.1
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[FrostWyrm.1]
+PrefabName = FreezeGland
+EnableConfig = true
+SetAmountMin = 2
+SetAmountMax = 4
+SetChanceToDrop = 0.75
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[FrostWyrm.2]
+PrefabName = FrostScale
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 3
+SetChanceToDrop = 1.0
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[FrostWyrm.3]
+PrefabName = Coins
+EnableConfig = true
+SetAmountMin = 100
+SetAmountMax = 200
+SetChanceToDrop = 0.5
+SetDropOnePerPlayer = false
+SetScaleByLevel = false

```

---

#### drop_that.drop_table.cfg

**Status**: Modified

**Summary**: -357 changes

**Key Changes**:

**Total changes**: 357 (showing top 8)

• **Beech1.0.SetAmountMax**: `2` *(removed)*
• **Beech1.0.SetAmountMin**: `1` *(removed)*
• **Beech1.1.SetAmountMax**: `2` *(removed)*
• **Beech1.1.SetAmountMin**: `1` *(removed)*
• **Beech1.10.SetAmountMax**: `1` *(removed)*
• **Beech1.10.SetAmountMin**: `1` *(removed)*
• **Beech1.2.SetAmountMax**: `3` *(removed)*
• **Beech1.2.SetAmountMin**: `2` *(removed)*
• ... and 349 more changes

**Full Diff**:

```diff
--- backup/drop_that.drop_table.cfg+++ current/drop_that.drop_table.cfg@@ -1,564 +1,10 @@-###################
-#Meadows
-###################
+# Auto-generated file for adding DropTable configurations.
+# This file is empty by default. It is intended to contains changes only, to avoid unintentional modifications as well as to reduce unnecessary performance cost.
+# Full documentation can be found at https://github.com/ASharpPen/Valheim.DropThat/wiki.
+# To get started: 
+#     1. Generate default configs in BepInEx/Debug folder, by enabling WriteDropTablesToFiles in 'drop_that.cfg'.
+#     2. Start game and enter a world, and wait a short moment for files to generate.
+#     3. Go to generated file, and copy the drops you want to modify from there into this file
+#     4. Make your changes.
+# To find modded configs and change those, enable WriteLoadedConfigsToFile in 'drop_that.cfg', and do as described above.
 
-[Beech_Stub]
-SetDropChance=100
-SetDropOnlyOnce=False
-SetDropMin=10
-SetDropMax=10
-
-[Beech_Stub.0]
-PrefabName=Wood
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-###########
-
-[Beech1]
-SetDropChance=50
-SetDropOnlyOnce=False
-SetDropMin=2
-SetDropMax=2
-
-[Beech1.0]
-PrefabName=Resin
-SetTemplateWeight=0.25
-SetAmountMin=1
-SetAmountMax=2
-DisableResourceModifierScaling=False
-
-[Beech1.1]
-PrefabName=Feathers
-SetTemplateWeight=0.25
-SetAmountMin=1
-SetAmountMax=2
-DisableResourceModifierScaling=False
-
-[Beech1.2]
-PrefabName=BeechSeeds
-SetTemplateWeight=1
-SetAmountMin=2
-SetAmountMax=3
-DisableResourceModifierScaling=False
-
-[Beech1.10]
-PrefabName=QueenBee
-SetTemplateWeight=0.1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-###########
-
-[BirchStub]
-SetDropChance=100
-SetDropOnlyOnce=False
-SetDropMin=10
-SetDropMax=10
-
-[BirchStub.0]
-PrefabName=Wood
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-[BirchStub.1]
-PrefabName=FineWood
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-###########
-
-[Birch_log_half]
-SetDropChance=100
-SetDropOnlyOnce=False
-SetDropMin=10
-SetDropMax=10
-
-[Birch_log_half.0]
-PrefabName=Wood
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-[Birch_log_half.1]
-PrefabName=FineWood
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-[Birch_log_half.100]
-PrefabName=EnchantedWoodPlains_TW
-SetTemplateWeight=0.2
-SetAmountMin=1
-SetAmountMax=1
-ConditionBiomes=Plains
-DisableResourceModifierScaling=False
-
-###########
-
-[OakStub]
-SetDropChance=100
-SetDropOnlyOnce=False
-SetDropMin=10
-SetDropMax=10
-
-[OakStub.0]
-PrefabName=Wood
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-[OakStub.1]
-PrefabName=FineWood
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-###################
-#BlackForest
-###################
-
-[FirTree_Stub]
-SetDropChance=100
-SetDropOnlyOnce=False
-SetDropMin=10
-SetDropMax=10
-
-[FirTree_Stub.0]
-PrefabName=Wood
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-###########
-
-[FirTree]
-SetDropChance=50
-SetDropOnlyOnce=False
-SetDropMin=1
-SetDropMax=2
-
-[FirTree.0]
-PrefabName=FirCone
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-[FirTree.1]
-PrefabName=Feathers
-SetTemplateWeight=0.25
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-[FirTree.2]
-PrefabName=Resin
-SetTemplateWeight=0.25
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-[FirTree.10]
-PrefabName=Mushroom
-SetTemplateWeight=0.25
-SetAmountMin=2
-SetAmountMax=3
-DisableResourceModifierScaling=False
-
-###########
-
-[FirTree_log_half]
-SetDropChance=100
-SetDropOnlyOnce=False
-SetDropMin=10
-SetDropMax=10
-
-[FirTree_log_half.0]
-PrefabName=Wood
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-[FirTree_log_half.100]
-PrefabName=EnchantedWoodMountain_TW
-SetTemplateWeight=0.2
-SetAmountMin=1
-SetAmountMax=1
-ConditionBiomes=Mountain
-DisableResourceModifierScaling=False
-
-###########
-
-[Pinetree_01_Stub]
-SetDropChance=100
-SetDropOnlyOnce=False
-SetDropMin=10
-SetDropMax=10
-
-[Pinetree_01_Stub.0]
-PrefabName=Wood
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-[Pinetree_01_Stub.1]
-PrefabName=RoundLog
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-###########
-
-[PineTree_log_half]
-SetDropChance=100
-SetDropOnlyOnce=False
-SetDropMin=15
-SetDropMax=15
-
-[PineTree_log_half.0]
-PrefabName=Wood
-SetTemplateWeight=0.75
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-[PineTree_log_half.1]
-PrefabName=RoundLog
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-[PineTree_log_half.100]
-PrefabName=EnchantedWoodBlackForest_TW
-SetTemplateWeight=0.2
-SetAmountMin=1
-SetAmountMax=1
-ConditionBiomes=BlackForest
-DisableResourceModifierScaling=False
-
-###########
-
-[Spawner_GreydwarfNest]
-SetDropChance=100
-SetDropOnlyOnce=True
-SetDropMin=2
-SetDropMax=2
-
-[Spawner_GreydwarfNest.0]
-PrefabName=AncientSeed
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=3
-DisableResourceModifierScaling=False
-
-[Spawner_GreydwarfNest.10]
-PrefabName=GDAncientShaman_rootspawn_TW
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=2
-DisableResourceModifierScaling=False
-
-###################
-#Swamp
-###################
-
-[SwampTree1_log]
-SetDropChance=100
-SetDropOnlyOnce=False
-SetDropMin=10
-SetDropMax=10
-
-[SwampTree1_log.0]
-PrefabName=Wood
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-
-[SwampTree1_log.1]
-PrefabName=ElderBark
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-
-[SwampTree1_log.2]
-PrefabName=FineWood
-SetTemplateWeight=0.5
-SetAmountMin=1
-SetAmountMax=1
-
-[SwampTree1_log.100]
-PrefabName=EnchantedWoodSwamp_TW
-SetTemplateWeight=0.2
-SetAmountMin=1
-SetAmountMax=1
-ConditionBiomes=Swamp
-
-###########
-
-[SwampTree1]
-SetDropChance=50
-SetDropOnlyOnce=False
-SetDropMin=1
-SetDropMax=2
-
-[SwampTree1.0]
-PrefabName=Resin
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=2
-
-[SwampTree1.1]
-PrefabName=Feathers
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=2
-
-[SwampTree1.10]
-PrefabName=AncientSeed
-SetTemplateWeight=0.25
-SetAmountMin=1
-SetAmountMax=1
-ConditionBiomes=Swamp
-
-[SwampTree1.11]
-PrefabName=Abomination
-SetTemplateWeight=0.10
-SetAmountMin=1
-SetAmountMax=1
-ConditionBiomes=Swamp
-
-###########
-
-[SwampTree1_Stub]
-SetDropChance=100
-SetDropOnlyOnce=False
-SetDropMin=10
-SetDropMax=10
-
-[SwampTree1_Stub.0]
-PrefabName=Wood
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-[SwampTree1_Stub.1]
-PrefabName=ElderBark
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-###################
-#Mountain
-###################
-
-[MountainGraveStone01]
-SetDropChance=100
-SetDropOnlyOnce=False
-SetDropMin=3
-SetDropMax=4
-
-[MountainGraveStone01.0]
-PrefabName=Stone
-SetTemplateWeight=0.9
-SetAmountMin=1
-SetAmountMax=1
-
-[MountainGraveStone01.1]
-PrefabName=SilverOre
-SetTemplateWeight=0.1
-SetAmountMin=1
-SetAmountMax=1
-ConditionGlobalKeys=defeated_bonemass
-
-###################
-#Plains
-###################
-
-[lox_ribs]
-SetDropChance=100
-SetDropOnlyOnce=False
-SetDropMin=2
-SetDropMax=3
-
-[lox_ribs.0]
-PrefabName=BoneFragments
-SetTemplateWeight=1
-SetAmountMin=2
-SetAmountMax=3
-
-[lox_ribs.1]
-PrefabName=LoxBone_TW
-SetTemplateWeight=0.1
-ConditionBiomes=Plains
-SetAmountMin=1
-SetAmountMax=1
-
-[lox_ribs.2]
-PrefabName=Bloodbag
-SetTemplateWeight=0.5
-SetAmountMin=2
-SetAmountMax=3
-
-###################
-#Mistlands
-###################
-
-[yggashoot_log_half]
-SetDropChance=100
-SetDropOnlyOnce=False
-SetDropMin=10
-SetDropMax=10
-
-[yggashoot_log_half.0]
-PrefabName=Wood
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-[yggashoot_log_half.1]
-PrefabName=YggdrasilWood
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-[yggashoot_log_half.100]
-PrefabName=EnchantedWoodMistlands_TW
-SetTemplateWeight=0.2
-SetAmountMin=1
-SetAmountMax=1
-ConditionBiomes=Mountain
-DisableResourceModifierScaling=False
-
-###################
-#MistlandsDungeonChest
-###################
-
-[TreasureChest_dvergrtown]
-SetDropChance=100
-SetDropOnlyOnce=True
-SetDropMin=3
-SetDropMax=4
-
-[TreasureChest_dvergrtown.0]
-PrefabName=MeadHealthMinor
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=2
-DisableResourceModifierScaling=False
-
-[TreasureChest_dvergrtown.1]
-PrefabName=MeadStaminaMinor
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=2
-DisableResourceModifierScaling=False
-
-[TreasureChest_dvergrtown.2]
-PrefabName=MisthareSupreme
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-[TreasureChest_dvergrtown.3]
-PrefabName=Carapace
-SetTemplateWeight=1
-SetAmountMin=2
-SetAmountMax=4
-DisableResourceModifierScaling=False
-
-[TreasureChest_dvergrtown.4]
-PrefabName=Tankard_dvergr
-SetTemplateWeight=0.1
-SetAmountMin=1
-SetAmountMax=1
-DisableResourceModifierScaling=False
-
-[TreasureChest_dvergrtown.5]
-PrefabName=JuteBlue
-SetTemplateWeight=1
-SetAmountMin=2
-SetAmountMax=4
-DisableResourceModifierScaling=False
-
-[TreasureChest_dvergrtown.6]
-PrefabName=JuteBlack_TW
-SetTemplateWeight=1
-SetAmountMin=2
-SetAmountMax=4
-DisableResourceModifierScaling=False
-
-[TreasureChest_dvergrtown.7]
-PrefabName=Coins
-SetTemplateWeight=1
-SetAmountMin=33
-SetAmountMax=66
-DisableResourceModifierScaling=False
-
-[TreasureChest_dvergrtown.10]
-PrefabName=ShardQueen_TW
-SetTemplateWeight=1
-SetAmountMin=2
-SetAmountMax=3
-DisableResourceModifierScaling=False
-
-###################
-#Misc.
-###################
-
-[shipwreck_karve_chest]
-SetDropChance=100
-SetDropOnlyOnce=True
-SetDropMin=2
-SetDropMax=3
-
-[shipwreck_karve_chest.0]
-PrefabName=Coins
-SetTemplateWeight=5
-SetAmountMin=50
-SetAmountMax=100
-
-[shipwreck_karve_chest.1]
-PrefabName=AmberPearl
-SetTemplateWeight=2
-SetAmountMin=1
-SetAmountMax=10
-
-[shipwreck_karve_chest.2]
-PrefabName=Ruby
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=2
-
-[shipwreck_karve_chest.10]
-PrefabName=FishingRod
-SetTemplateWeight=0.2
-SetAmountMin=1
-SetAmountMax=1
-
-[shipwreck_karve_chest.11]
-PrefabName=Thunderstone
-SetTemplateWeight=1
-SetAmountMin=1
-SetAmountMax=1
```

---

#### drop_that.character_drop.elite_additions.cfg

**Status**: Modified

**Summary**: +420, -870 changes

**Key Changes**:

**Total changes**: 1290 (showing top 8)

• **Abomination.0.AmountMax**: `1` *(removed)*
• **Abomination.0.AmountMin**: `1` *(removed)*
• **Abomination.0.ChanceToDrop**: `15` *(removed)*
• **Abomination.0.ScaleByLevel**: `False` *(removed)*
• **Abomination.1.AmountLimit**: `20` *(removed)*
• **Abomination.1.AmountMax**: `5` *(removed)*
• **Abomination.1.AmountMin**: `5` *(removed)*
• **Abomination.1.ChanceToDrop**: `100` *(removed)*
• ... and 1282 more changes

**Full Diff**:

```diff
--- backup/drop_that.character_drop.elite_additions.cfg+++ current/drop_that.character_drop.elite_additions.cfg@@ -1,1171 +1,582 @@-########################
-# IDs: Vanilla and 50-59
-########################
-
-####################
-# Meadows
-####################
-
-[Greyling.50]
-PrefabName=Flint
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-[Greyling.51]
-PrefabName=Wood
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-####################
-
-[Deer.2]
-PrefabName=TrophyDeer
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=25
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Deer.50]
-PrefabName=CookedDeerMeat
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-AmountLimit=1
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=False
-ConditionKilledWithStatuses=Burning
-ConditionKilledByDamageType= Fire
-DisableResourceModifierScaling=True
-
-####################
-
-[Boar.50]
-PrefabName=CookedMeat
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-AmountLimit=1
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=False
-ConditionKilledWithStatuses=Burning
-ConditionKilledByDamageType= Fire
-DisableResourceModifierScaling=True
-
-####################
-
-[Neck.50]
-PrefabName=NeckTailGrilled
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-AmountLimit=1
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=False
-ConditionKilledWithStatuses=Burning
-ConditionKilledByDamageType= Fire
-DisableResourceModifierScaling=True
-
-####################
-# BlackForest
-####################
-
-[Ghost.0]
-PrefabName=Amber
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Ghost.1]
-PrefabName=Ruby
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Ghost.2]
-PrefabName=AncientArtifact_TW
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=25
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[Greydwarf.0]
-PrefabName=GreydwarfEye
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=True
-ConditionKilledByEntityType=Player
-DisableResourceModifierScaling=True
-
-[Greydwarf.4]
-PrefabName=TrophyGreydwarf
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-ConditionKilledByEntityType=Player
-DisableResourceModifierScaling=True
-
-[Greydwarf.50]
-PrefabName=GreydwarfEye
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=True
-ConditionKilledWithStatus=Burning
-ConditionKilledByDamageType=Fire
-DisableResourceModifierScaling=True
-
-[Greydwarf.51]
-PrefabName=AncientSeed
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=0.2
-DropOnePerPlayer=False
-ScaleByLevel=True
-ConditionKilledByEntityType=Player
-DisableResourceModifierScaling=True
-
-####################
-
-[Greydwarf_Elite.0]
-PrefabName=GreydwarfEye
-EnableConfig=True
-AmountMin=2
-AmountMax=2
-ChanceToDrop=75
-DropOnePerPlayer=False
-ScaleByLevel=True
-ConditionKilledByEntityType=Player
-DisableResourceModifierScaling=True
-
-####################
-
-[Greydwarf_Shaman.0]
-PrefabName=GreydwarfEye
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=75
-DropOnePerPlayer=False
-ScaleByLevel=True
-ConditionKilledByEntityType=Player
-DisableResourceModifierScaling=True
-
-####################
-
-[Troll.0]
-PrefabName=Ruby
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[Troll.1]
-PrefabName=TrophyFrostTroll
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Troll.2]
-PrefabName=TrollHide
-EnableConfig=True
-AmountMin=3
-AmountMax=5
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-####################
-# Swamp
-####################
-
-[Leech.50]
-PrefabName=FishRaw
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=20
-DropOnePerPlayer=False
-ScaleByLevel=true
-AmountLimit=1
-DisableResourceModifierScaling=True
-
-####################
-
-[BlobElite.1]
-PrefabName=IronScrap
-EnableConfig=True
-AmountMin=2
-AmountMax=2
-ChanceToDrop=33
-DropOnePerPlayer=False
-ScaleByLevel=True
-ConditionGlobalKeys=defeated_gdking
-DisableResourceModifierScaling=True
-
-####################
-
-[Abomination.0]
-PrefabName=TrophyAbomination
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Abomination.1]
-PrefabName=Root
-EnableConfig=True
-AmountMin=5
-AmountMax=5
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=20
-DisableResourceModifierScaling=True
-
-[Abomination.52]
-PrefabName=ElderBark
-EnableConfig=True
-AmountMin=2
-AmountMax=4
-ChanceToDrop=20
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-####################
-
-[Draugr.2]
-PrefabName=RottenPelt_TW
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=25
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-[Draugr.50]
-PrefabName=TrophyDraugrElite
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=0.2
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=1
-DisableResourceModifierScaling=True
-
-[Draugr.51]
-PrefabName=WitheredBone
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=5
-DropOnePerPlayer=False
-ScaleByLevel=False
-AmountLimit=3
-DisableResourceModifierScaling=True
-
-####################
-
-[Draugr_Ranged.2]
-PrefabName=RottenPelt_TW
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=25
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-[Draugr_Ranged.50]
-PrefabName=TrophyDraugrElite
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=0.2
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=1
-DisableResourceModifierScaling=True
-
-[Draugr_Ranged.51]
-PrefabName=WitheredBone
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=5
-DropOnePerPlayer=False
-ScaleByLevel=False
-AmountLimit=3
-DisableResourceModifierScaling=True
-
-####################
-
-[Draugr_Elite.2]
-PrefabName=RottenPelt_TW
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-[Draugr_Elite.50]
-PrefabName=WitheredBone
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=5
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[Wraith.0]
-PrefabName=TrophyWraith
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Wraith.1]
-PrefabName=Chain
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Wraith.50]
-PrefabName=TurnipSeeds
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[Surtling.0]
-PrefabName=Coal
-Enable=true
-EnableConfig=true
-AmountMin=4
-AmountMax=5
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[Surtling.1]
-PrefabName=SurtlingCore
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=1
-ChanceToDrop=75
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-ConditionKilledByEntityType=Player
-
-[Surtling.2]
-PrefabName=TrophySurtling
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Surtling.50]
-PrefabName=SurtlingCore
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=1
-ChanceToDrop=25
-DropOnePerPlayer=false
-ScaleByLevel=true
-ConditionKilledWithStatuses=Wet
-
-[BogWitchKvastur.2]
-PrefabName=TrophyKvastur
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=1
-ChanceToDrop=50
-DropOnePerPlayer=false
-ScaleByLevel=false
-DisableResourceModifierScaling=false
-ConditionNotDay=false
-ConditionNotAfternoon=false
-ConditionNotNight=false
-
-####################
-# Mountain
-####################
-
-[Wolf.51]
-PrefabName=WolfClaw
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-ConditionNotCreatureStates=Tamed
-DisableResourceModifierScaling=True
-
-####################
-
-[Bat.50]
-PrefabName=Bloodbag
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-####################
-
-[Fenring.51]
-PrefabName=WolfHairBundle
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Fenring.52]
-PrefabName=WolfClaw
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=20
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[Ulv.50]
-PrefabName=WolfHairBundle
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Ulv.51]
-PrefabName=WolfClaw
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[Fenring_Cultist.51]
-PrefabName=WolfHairBundle
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Fenring_Cultist.52]
-PrefabName=WolfClaw
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[StoneGolem.0]
-PrefabName=TrophySGolem
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[StoneGolem.51]
-PrefabName=SilverOre
-EnableConfig=True
-AmountMin=2
-AmountMax=4
-ChanceToDrop=20
-DropOnePerPlayer=False
-ScaleByLevel=False
-ConditionGlobalKeys=defeated_bonemass
-DisableResourceModifierScaling=True
-
-####################
-
-[Hatchling.50]
-PrefabName=DragonEgg
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=0.5
-DropOnePerPlayer=False
-ScaleByLevel=False
-AmountLimit=1
-DisableResourceModifierScaling=False
-
-###################
-# Plains
-###################
-
-[Lox.0]
-PrefabName=LoxMeat
-EnableConfig=True
-AmountMin=2
-AmountMax=4
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-
-####################
-
-[Goblin.0]
-PrefabName=AmberPearl
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=1
-ChanceToDrop=25
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[Goblin.1]
-PrefabName=BlackMetalScrap
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=10
-ConditionGlobalKeys=defeated_dragon
-DisableResourceModifierScaling=True
-
-[Goblin.2]
-PrefabName=TrophyGoblin
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Goblin.50]
-PrefabName=GoblinScraps_TW
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=25
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=10
-ConditionGlobalKeys=defeated_dragon
-DisableResourceModifierScaling=True
-
-####################
-
-[GoblinArcher.0]
-PrefabName=AmberPearl
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=1
-ChanceToDrop=25
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[GoblinArcher.1]
-PrefabName=BlackMetalScrap
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=10
-ConditionGlobalKeys=defeated_dragon
-DisableResourceModifierScaling=True
-
-[GoblinArcher.2]
-PrefabName=TrophyGoblin
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[GoblinArcher.50]
-PrefabName=GoblinScraps_TW
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=25
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=10
-ConditionGlobalKeys=defeated_dragon
-DisableResourceModifierScaling=True
-
-####################
-
-[GoblinBrute.0]
-PrefabName=AmberPearl
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=25
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[GoblinBrute.1]
-PrefabName=BlackMetalScrap
-EnableConfig=True
-AmountMin=2
-AmountMax=4
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=20
-DisableResourceModifierScaling=False
-ConditionGlobalKeys=defeated_dragon
-
-[GoblinBrute.2]
-PrefabName=GoblinTotem
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=False
-
-[GoblinBrute.3]
-PrefabName=TrophyGoblinBrute
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=False
-
-[GoblinBrute.51]
-PrefabName=GoblinScraps_TW
-EnableConfig=True
-AmountMin=2
-AmountMax=4
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=20
-ConditionGlobalKeys=defeated_dragon
-DisableResourceModifierScaling=True
-
-####################
-
-[GoblinShaman.0]
-PrefabName=Ruby
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=25
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[GoblinShaman.1]
-PrefabName=BlackMetalScrap
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=10
-ConditionGlobalKeys=defeated_dragon
-DisableResourceModifierScaling=True
-
-[GoblinShaman.50]
-PrefabName=GoblinScraps_TW
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=10
-ConditionGlobalKeys=defeated_dragon
-DisableResourceModifierScaling=True
-
-[GoblinShaman.51]
-PrefabName=GoblinTotem
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=20
-DropOnePerPlayer=False
-ScaleByLevel=False
-ConditionGlobalKeys=defeated_dragon
-DisableResourceModifierScaling=True
-
-####################
-# Ocean
-####################
-
-[Serpent.0]
-PrefabName=TrophySerpent
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=33
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Serpent.1]
-PrefabName=SerpentMeat
-EnableConfig=True
-AmountMin=4
-AmountMax=6
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=18
-DisableResourceModifierScaling=True
-
-[Serpent.2]
-PrefabName=SerpentScale
-EnableConfig=True
-AmountMin=4
-AmountMax=6
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=18
-DisableResourceModifierScaling=True
-
-####################
-# Mistlands
-####################
-
-[Gjall.0]
-PrefabName=Bilebag
-EnableConfig=True
-AmountMin=2
-AmountMax=4
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-
-[Gjall.1]
-PrefabName=TrophyGjall
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[SeekerBrute.2]
-PrefabName=TrophySeekerBrute
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[Dverger.0]
-PrefabName=Softtissue
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[Dverger.1]
-PrefabName=BlackMarble
-Enable=false
-EnableConfig=true
-AmountMin=1
-AmountMax=2
-ChanceToDrop=50
-DropOnePerPlayer=false
-ScaleByLevel=false
-DisableResourceModifierScaling=True
-
-[Dverger.2]
-PrefabName=Amber
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[Dverger.3]
-PrefabName=TrophyDvergr
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[Dverger.50]
-PrefabName=JuteBlue
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-[Dverger.51]
-PrefabName=BlackCore
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=5
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[DvergerMage.0]
-PrefabName=Softtissue
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[DvergerMage.2]
-PrefabName=Amber
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[DvergerMage.50]
-PrefabName=JuteBlue
-EnableConfig=True
-AmountMin=1
-AmountMax=3
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-[DvergerMage.51]
-PrefabName=BlackCore
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=5
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-####################
-
-[DvergerMageFire.2]
-PrefabName=Amber
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-####################
-
-[DvergerMageIce.2]
-PrefabName=Amber
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-####################
-
-[DvergerMageSupport.2]
-PrefabName=Amber
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-[DvergerMageSupport.50]
-PrefabName=DvergrKeyFragment
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=1
-ChanceToDrop=5
-DropOnePerPlayer=false
-ScaleByLevel=false
-AmountLimit=1
-DisableResourceModifierScaling=false
-
-####################
-# Ashlands
-####################
-
-[BonemawSerpent.0]
-PrefabName=TrophyBonemawSerpent
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=33
-DropOnePerPlayer=False
-ScaleByLevel=False
-DisableResourceModifierScaling=True
-
-[BonemawSerpent.1]
-PrefabName=BoneMawSerpentMeat
-EnableConfig=True
-AmountMin=4
-AmountMax=6
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=18
-DisableResourceModifierScaling=True
-
-[BonemawSerpent.2]
-PrefabName=BonemawSerpentTooth
-EnableConfig=True
-AmountMin=4
-AmountMax=6
-ChanceToDrop=100
-DropOnePerPlayer=False
-ScaleByLevel=True
-AmountLimit=18
-DisableResourceModifierScaling=True
-
-[BonemawSerpent.50]
-PrefabName=GemstoneGreen
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-ConditionGlobalKeys=defeated_queen
-ConditionKilledByEntityType=Player
-AmountLimit=1
-
-####################
-
-[FallenValkyrie.50]
-PrefabName=BlackCore
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=50
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-
-[FallenValkyrie.51]
-PrefabName=GemstoneBlue
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-ConditionGlobalKeys=defeated_queen
-ConditionKilledByEntityType=Player
-AmountLimit=1
-
-####################
-
-[Morgen.50]
-PrefabName=GemstoneRed
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-ConditionGlobalKeys=defeated_queen
-AmountLimit=1
-
-[Morgen_NonSleeping.50]
-PrefabName=GemstoneRed
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=15
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-ConditionGlobalKeys=defeated_queen
-AmountLimit=1
-
-####################
-
-[BlobLava.50]
-PrefabName=MoltenCore
-EnableConfig=True
-AmountMin=1
-AmountMax=1
-ChanceToDrop=10
-DropOnePerPlayer=False
-ScaleByLevel=True
-DisableResourceModifierScaling=True
-ConditionKilledByEntityType=Player
-
-####################
-
-[DvergerAshlands.1]
-PrefabName=BlackMarble
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=2
-ChanceToDrop=50
-DropOnePerPlayer=false
-ScaleByLevel=false
-DisableResourceModifierScaling=false
-
-[DvergerAshlands.2]
-PrefabName=Amber
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True+## Elite Creature Item Additions for RelicHeim
+## Multiple items per elite with very small individual chances for "jackpot" feeling
+## Total drop chance per elite: ~1-2% (multiple items, very low individual rates)
+## World progression: Early biomes = more items/lower rates, Late biomes = fewer items/higher rates
+
+# =============================================================================
+# CREATURE ASSIGNMENTS (Multiple Rare Items Per Elite)
+# =============================================================================
+
+# Meadows Elite (Boar_Elite) - Multiple survival items + basic armor (Total: ~2% chance)
+[Boar_Elite.5]
+PrefabName = SpearFlint
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Boar_Elite.6]
+PrefabName = AxeFlint
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Boar_Elite.7]
+PrefabName = KnifeFlint
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Boar_Elite.8]
+PrefabName = ShieldWood
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Boar_Elite.9]
+PrefabName = BowCrude
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Boar_Elite.10]
+PrefabName = MeadHealthMinor
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 3
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Boar_Elite.11]
+PrefabName = ArmorLeatherChest
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Boar_Elite.12]
+PrefabName = ArmorLeatherLegs
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+# Black Forest Elite (Greydwarf_Elite) - Multiple bronze items + bronze armor (Total: ~1.75% chance)
+[Greydwarf_Elite.5]
+PrefabName = SwordBronze
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Greydwarf_Elite.6]
+PrefabName = MaceBronze
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Greydwarf_Elite.7]
+PrefabName = SpearBronze
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Greydwarf_Elite.8]
+PrefabName = ShieldBronzeBuckler
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Greydwarf_Elite.9]
+PrefabName = MeadStaminaMinor
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Greydwarf_Elite.10]
+PrefabName = ArmorBronzeChest
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Greydwarf_Elite.11]
+PrefabName = ArmorBronzeLegs
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+# Swamp Elite (Draugr_Elite) - Multiple iron items + iron armor (Total: ~1.5% chance)
+[Draugr_Elite.5]
+PrefabName = SwordIron
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Draugr_Elite.6]
+PrefabName = MaceIron
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Draugr_Elite.7]
+PrefabName = SpearElderbark
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Draugr_Elite.8]
+PrefabName = MeadHealthMedium
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Draugr_Elite.9]
+PrefabName = ArmorIronChest
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Draugr_Elite.10]
+PrefabName = ArmorIronLegs
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+# Mountain Elite (Wolf_Elite) - Multiple silver items + wolf armor (Total: ~1.5% chance)
+[Wolf_Elite.5]
+PrefabName = SwordSilver
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Wolf_Elite.6]
+PrefabName = MaceSilver
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Wolf_Elite.7]
+PrefabName = SpearWolfFang
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Wolf_Elite.8]
+PrefabName = MeadStaminaMedium
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Wolf_Elite.9]
+PrefabName = ArmorWolfChest
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Wolf_Elite.10]
+PrefabName = ArmorWolfLegs
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+# Ocean Elite (Serpent_Elite) - Multiple maritime items + wolf armor (Total: ~1.5% chance)
+[Serpent_Elite.5]
+PrefabName = SwordSilver
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Serpent_Elite.6]
+PrefabName = BowDraugrFang
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Serpent_Elite.7]
+PrefabName = ArmorWolfChest
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Serpent_Elite.8]
+PrefabName = MeadHealthMajor
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Serpent_Elite.9]
+PrefabName = ArmorWolfLegs
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Serpent_Elite.10]
+PrefabName = ArmorWolfHelmet
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+# Plains Elite (GoblinBrute) - Multiple black metal items + padded armor (Total: ~1.25% chance)
+[GoblinBrute.5]
+PrefabName = SwordBlackmetal
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[GoblinBrute.6]
+PrefabName = MaceNeedle
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[GoblinBrute.7]
+PrefabName = AtgeirBlackmetal
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[GoblinBrute.8]
+PrefabName = ArmorPaddedChest
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[GoblinBrute.9]
+PrefabName = ArmorPaddedLegs
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+# Mistlands Elite (Seeker_Elite) - Multiple mystical items + carapace armor (Total: ~1.25% chance)
+[Seeker_Elite.5]
+PrefabName = SwordMistwalker
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Seeker_Elite.6]
+PrefabName = AtgeirHimminAfl
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Seeker_Elite.7]
+PrefabName = SpearCarapace
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Seeker_Elite.8]
+PrefabName = ArmorCarapaceChest
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Seeker_Elite.9]
+PrefabName = ArmorCarapaceLegs
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+# Ashlands Elite (Charred_Elite) - Multiple legendary items + ashlands armor (Total: ~1.25% chance)
+[Charred_Elite.5]
+PrefabName = SwordNiedhogg
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Charred_Elite.6]
+PrefabName = THSwordSlayer
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Charred_Elite.7]
+PrefabName = SwordDyrnwyn
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Charred_Elite.8]
+PrefabName = ArmorAshlandsChest
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Charred_Elite.9]
+PrefabName = ArmorAshlandsLegs
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+# Deep North Elite (Fenring_Elite) - Multiple divine items + surtr armor (Total: ~1.25% chance)
+[Fenring_Elite.5]
+PrefabName = AxeSurtr_TW
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Fenring_Elite.6]
+PrefabName = AtgeirSurtr_TW
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Fenring_Elite.7]
+PrefabName = SwordSurtr_TW
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Fenring_Elite.8]
+PrefabName = ArmorSurtrChest_TW
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Fenring_Elite.9]
+PrefabName = ArmorSurtrLegs_TW
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+# Troll - Multiple enhanced bronze items + bronze armor (Total: ~1.75% chance)
+[Troll.5]
+PrefabName = BattleaxeBronze_TW
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Troll.6]
+PrefabName = ClaymoreBronze_TW
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Troll.7]
+PrefabName = CrossbowBronze_TW
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Troll.8]
+PrefabName = MeadHealthMinor
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 3
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Troll.9]
+PrefabName = MeadStaminaMinor
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 2
+SetChanceToDrop = 0.25
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Troll.10]
+PrefabName = ArmorBronzeChest
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+[Troll.11]
+PrefabName = ArmorBronzeLegs
+EnableConfig = true
+SetAmountMin = 1
+SetAmountMax = 1
+SetChanceToDrop = 0.15
+SetDropOnePerPlayer = false
+SetScaleByLevel = false
+
+# =============================================================================
+# DROP RATE PHILOSOPHY
+# =============================================================================
+
+# Drop rates are VERY SMALL for that "jackpot" feeling:
+# - Weapons/Consumables: 0.25% chance (extremely rare individual drops)
+# - Armor pieces: 0.15% chance (even rarer due to higher value)
+# - Early biomes: More items (7-8) = higher total chance (~1.75-2%)
+# - Late biomes: Fewer items (5-6) = lower total chance (~1.25-1.5%)
+# - Each star level rolls separately, so higher stars = more chances
+# - This creates excitement without economy flooding
+# - When any item drops, it's a memorable "jackpot" moment
+
+# ENHANCED SYSTEM BENEFITS:
+# - More variety per elite (weapons, armor, consumables)
+# - World progression reflected in item tiers and quantities
+# - Early biomes get more chances but lower-tier items
+# - Late biomes get fewer chances but higher-tier items
+# - Armor pieces provide long-term value and excitement
+# - Consumables provide immediate value and excitement
+# - Easy to modify individual items or add more
+
+# This creates excitement without overwhelming the material-focused economy 
```

---


### Enchantment System

*Files in this category with changes from RelicHeim backup:*

#### kg.ValheimEnchantmentSystem.cfg

**Status**: Modified

**Summary**: No changes detected

**Full Diff**:

```diff
--- backup/kg.ValheimEnchantmentSystem.cfg+++ current/kg.ValheimEnchantmentSystem.cfg@@ -1,4 +1,4 @@-## Settings file was created by plugin Valheim Enchantment System v1.7.3
+## Settings file was created by plugin Valheim Enchantment System v1.7.4
 ## Plugin GUID: kg.ValheimEnchantmentSystem
 
 [Notifications]

```

---

#### ValheimEnchantmentSystem/kg.ValheimEnchantmentSystem.cfg

**Status**: Modified

**Summary**: ~2 changes

**Key Changes**:

**Total changes**: 2 (showing top 2)

• **skill_1254459142.Skill effect factor**: `1` → `1.3` (+0.3)
• **skill_1254459142.Skill gain factor**: `1` → `0.55` (-0.45)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| skill_1254459142.Skill effect factor | 1 | 1.3 | +0.3 |
| skill_1254459142.Skill gain factor | 1 | 0.55 | -0.45 |

**Full Diff**:

```diff
--- backup/ValheimEnchantmentSystem/kg.ValheimEnchantmentSystem.cfg+++ current/ValheimEnchantmentSystem/kg.ValheimEnchantmentSystem.cfg@@ -196,13 +196,13 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill gain factor = 1
+Skill gain factor = 0.55
 
 ## The power of the skill, based on the default power.
 # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill effect factor = 1
+Skill effect factor = 1.3
 
 ## How much experience to lose on death.
 # Setting type: Int32

```

---


### EpicLoot

*Files in this category with changes from RelicHeim backup:*

#### randyknapp.mods.epicloot.cfg

**Status**: Modified

**Summary**: No changes detected

**Full Diff**:

```diff
--- backup/randyknapp.mods.epicloot.cfg+++ current/randyknapp.mods.epicloot.cfg@@ -1,4 +1,4 @@-## Settings file was created by plugin Epic Loot v0.10.6
+## Settings file was created by plugin Epic Loot v0.11.4
 ## Plugin GUID: randyknapp.mods.epicloot
 
 [Abilities]
@@ -137,9 +137,6 @@ 
 [Config Sync]
 
-## [Server Only] The configuration is locked and may not be changed by clients once it has been synced from the server. Only valid for server config, will have no effect on clients.
-# Setting type: Boolean
-# Default value: true
 Lock Config = true
 
 [Crafting UI]

```

---


### EpicMMO

*Files in this category with changes from RelicHeim backup:*

#### WackyMole.EpicMMOSystem.cfg

**Status**: Modified

**Summary**: ~29 changes

**Key Changes**:

**Total changes**: 29 (showing top 8)

• **1.LevelSystem Dexterity---.StaminaAttack**: `0.3` → `0.2` (-0.1)
• **1.LevelSystem Dexterity---.StaminaReduction**: `0.3` → `0.1` (-0.2)
• **1.LevelSystem Endurance------.AddStamina**: `1` → `1.8` (+0.8)
• **1.LevelSystem Endurance------.StaminaReg**: `0.5` → `0.35` (-0.15)
• **1.LevelSystem Strength-----.StaminaBlock**: `0.3` → `0.15` (-0.15)
• **1.LevelSystem Vigour------.AddHp**: `1` → `2.3` (+1.3)
• **1.LevelSystem-----------.BonusLevelPoints**: `5:2,10:2,15:2,20:3,25:2,30:2,35:2,40:3,45:2,50:2,55:2,60:3,65:2,70:2,75:2,80:4,85:5,90:5` → `5:4,10:4,15:5,20:6,25:4,30:5,35:4,40:7,45:5,50:6,55:5,60:8,65:5,70:6,75:5,80:9,85:7,90:7,95:7,100:9,105:8,110:8,115:8,120:12`
• **1.LevelSystem-----------.FreePointForLevel**: `2` → `4` (+2)
• ... and 21 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| 1.LevelSystem Dexterity---.StaminaAttack | 0.3 | 0.2 | -0.1 |
| 1.LevelSystem Dexterity---.StaminaReduction | 0.3 | 0.1 | -0.2 |
| 1.LevelSystem Endurance------.AddStamina | 1 | 1.8 | +0.8 |
| 1.LevelSystem Endurance------.StaminaReg | 0.5 | 0.35 | -0.15 |
| 1.LevelSystem Strength-----.StaminaBlock | 0.3 | 0.15 | -0.15 |
| 1.LevelSystem Vigour------.AddHp | 1 | 2.3 | +1.3 |
| 1.LevelSystem-----------.FreePointForLevel | 2 | 4 | +2 |
| 1.LevelSystem-----------.GroupExp | 0.7 | 0.90 | +0.2 |
| 1.LevelSystem-----------.MaxLevel | 90 | 120 | +30 |
| 1.LevelSystem-----------.MaxLossExp | 0.5 | 0.04 | -0.46 |
| 1.LevelSystem-----------.MinLossExp | 0.25 | 0.01 | -0.24 |
| 1.LevelSystem-----------.MultiplyNextLevelExperience | 1.043 | 1.048 | +0.005 |
| 1.LevelSystem-----------.PriceResetPoints | 55 | 5 | -50 |
| 1.LevelSystem-----------.RateExp | 1 | 1.15 | +0.15 |
| 1.LevelSystem-----------.maxValueDexterity | 50 | 100 | +50 |
| 1.LevelSystem-----------.maxValueEndurance | 50 | 100 | +50 |
| 1.LevelSystem-----------.maxValueIntelligence | 50 | 100 | +50 |
| 1.LevelSystem-----------.maxValueSpecializing | 50 | 100 | +50 |
| 1.LevelSystem-----------.maxValueStrength | 50 | 100 | +50 |
| 1.LevelSystem-----------.maxValueVigour | 50 | 100 | +50 |
| 2.Creature level control.Low_damage_config | 0 | 3 | +3 |
| 5.Optional perk---------.AddDefaultHealth | 0 | 25 | +25 |

**Full Diff**:

```diff
--- backup/WackyMole.EpicMMOSystem.cfg+++ current/WackyMole.EpicMMOSystem.cfg@@ -20,17 +20,17 @@ ## Maximum level. Максимальный уровень [Synced with Server]
 # Setting type: Int32
 # Default value: 100
-MaxLevel = 90
+MaxLevel = 120
 
 ## Reset price per point. Цена сброса за один поинт [Synced with Server]
 # Setting type: Int32
 # Default value: 3
-PriceResetPoints = 55
+PriceResetPoints = 5
 
 ## Free points per level. Свободных поинтов за один уровень [Synced with Server]
 # Setting type: Int32
 # Default value: 5
-FreePointForLevel = 2
+FreePointForLevel = 4
 
 ## Additional free points start. Дополнительных свободных поинтов [Synced with Server]
 # Setting type: Int32
@@ -50,7 +50,7 @@ ## Experience multiplier for the next level - Should never go below 1.00. Умножитель опыта для следующего уровня [Synced with Server]
 # Setting type: Single
 # Default value: 1.05
-MultiplyNextLevelExperience = 1.043
+MultiplyNextLevelExperience = 1.048
 
 ## Extra experience (from the sum of the basic experience) for the level of the monster. Доп опыт (из суммы основного опыта) за уровень монстра [Synced with Server]
 # Setting type: Single
@@ -60,22 +60,22 @@ ## Experience multiplier. Множитель опыта [Synced with Server]
 # Setting type: Single
 # Default value: 1
-RateExp = 1
+RateExp = 1.15
 
 ## Experience multiplier that the other players in the group get. Множитель опыта который получают остальные игроки в группе [Synced with Server]
 # Setting type: Single
 # Default value: 0.7
-GroupExp = 0.7
+GroupExp = 0.90
 
 ## Minimum Loss Exp if player death, default 5% loss [Synced with Server]
 # Setting type: Single
 # Default value: 0.05
-MinLossExp = 0.25
+MinLossExp = 0.01
 
 ## Maximum Loss Exp if player death, default 25% loss [Synced with Server]
 # Setting type: Single
 # Default value: 0.25
-MaxLossExp = 0.5
+MaxLossExp = 0.04
 
 ## Enabled exp loss [Synced with Server]
 # Setting type: Boolean
@@ -85,7 +85,7 @@ ## Added bonus point for level. Example(level:points): 5:10,15:20 add all 30 points  [Synced with Server]
 # Setting type: String
 # Default value: 5:5,10:5
-BonusLevelPoints = 5:2,10:2,15:2,20:3,25:2,30:2,35:2,40:3,45:2,50:2,55:2,60:3,65:2,70:2,75:2,80:4,85:5,90:5
+BonusLevelPoints = 5:4,10:4,15:5,20:6,25:4,30:5,35:4,40:7,45:5,50:6,55:5,60:8,65:5,70:6,75:5,80:9,85:7,90:7,95:7,100:9,105:8,110:8,115:8,120:12
 
 ## The range at which people in a group (Group MOD ONLY) get XP, relative to player who killed mob - only works if the killer gets xp. - Default 70f, a large number like 999999999999f, will probably cover map [Synced with Server]
 # Setting type: Single
@@ -120,32 +120,32 @@ ## Maximum number of points you can put into Strength [Synced with Server]
 # Setting type: Int32
 # Default value: 200
-maxValueStrength = 50
+maxValueStrength = 100
 
 ## Maximum number of points you can put into Dexterity [Synced with Server]
 # Setting type: Int32
 # Default value: 200
-maxValueDexterity = 50
+maxValueDexterity = 100
 
 ## Maximum number of points you can put into Intelleigence [Synced with Server]
 # Setting type: Int32
 # Default value: 200
-maxValueIntelligence = 50
+maxValueIntelligence = 100
 
 ## Maximum number of points you can put into Endurance [Synced with Server]
 # Setting type: Int32
 # Default value: 200
-maxValueEndurance = 50
+maxValueEndurance = 100
 
 ## Maximum number of points you can put into Vigour [Synced with Server]
 # Setting type: Int32
 # Default value: 200
-maxValueVigour = 50
+maxValueVigour = 100
 
 ## Maximum number of points you can put into Specializing [Synced with Server]
 # Setting type: Int32
 # Default value: 200
-maxValueSpecializing = 50
+maxValueSpecializing = 100
 
 ## You get normal xp amount, times this number for taming a creature [Synced with Server]
 # Setting type: Int32
@@ -167,24 +167,24 @@ ## Reduces attack stamina consumption.  [Synced with Server]
 # Setting type: Single
 # Default value: 0.1
-StaminaAttack = 0.3
+StaminaAttack = 0.2
 
 ## Decrease stamina consumption for running, jumping for one point. [Synced with Server]
 # Setting type: Single
 # Default value: 0.15
-StaminaReduction = 0.3
+StaminaReduction = 0.1
 
 [1.LevelSystem Endurance------]
 
 ## One Point Stamina Increase. [Synced with Server]
 # Setting type: Single
 # Default value: 1
-AddStamina = 1
+AddStamina = 1.8
 
 ## Increase stamina regeneration per point. [Synced with Server]
 # Setting type: Single
 # Default value: 0.4
-StaminaReg = 0.5
+StaminaReg = 0.35
 
 ## Increase in physical protection per point. [Synced with Server]
 # Setting type: Single
@@ -250,7 +250,7 @@ ## Decrease stamina consumption per unit per point. [Synced with Server]
 # Setting type: Single
 # Default value: 0.2
-StaminaBlock = 0.3
+StaminaBlock = 0.15
 
 ## Amount of Critical Dmg done per point [Synced with Server]
 # Setting type: Single
@@ -262,7 +262,7 @@ ## One Point Health Increase.  [Synced with Server]
 # Setting type: Single
 # Default value: 1
-AddHp = 1
+AddHp = 2.3
 
 ## Increase health regeneration per point. [Synced with Server]
 # Setting type: Single
@@ -324,7 +324,7 @@ ## Extra paramater to low damage config - for reference(float)(playerLevel + lowDamageConfig) / monsterLevel; when player is below lvl [Synced with Server]
 # Setting type: Int32
 # Default value: 0
-Low_damage_config = 0
+Low_damage_config = 3
 
 ## Character level - MinLevelRange is less than the level of the monster, then you will receive reduced experience. Уровень персонажа - MinLevelRange меньше уровня монстра, то вы будете получать урезанный опыт [Synced with Server]
 # Setting type: Int32
@@ -388,7 +388,7 @@ ## Add health by default [Synced with Server]
 # Setting type: Single
 # Default value: 0
-AddDefaultHealth = 0
+AddDefaultHealth = 25
 
 ## Add weight by default [Synced with Server]
 # Setting type: Single
@@ -507,17 +507,17 @@ ## Disables Piece XP. You only get xp for once per building, then you have to change to another piece. It still could be abused. [Synced with Server]
 # Setting type: Boolean
 # Default value: false
-Disable Piece XP = false
+Disable Piece XP = true
 
 ## Disables XP for tames. [Synced with Server]
 # Setting type: Boolean
 # Default value: false
-Disable Tame XP = false
+Disable Tame XP = true
 
 ## Disable Fish pickup XP, you still get xp for catching fish. [Synced with Server]
 # Setting type: Boolean
 # Default value: false
-Disable Fish Pickup XP = false
+Disable Fish Pickup XP = true
 
 ## Disable XP for mining. [Synced with Server]
 # Setting type: Boolean
@@ -527,7 +527,7 @@ ## Disable XP for pickables. [Synced with Server]
 # Setting type: Boolean
 # Default value: false
-Disable Pickup XP = false
+Disable Pickup XP = true
 
 ## Disable XP for Chopping Trees. [Synced with Server]
 # Setting type: Boolean
@@ -537,7 +537,7 @@ ## Disable XP Destructables. [Synced with Server]
 # Setting type: Boolean
 # Default value: false
-Disable Destructables XP = false
+Disable Destructables XP = true
 
 ## Gives a Warning log for various objects names. Don't forgot that (Clone) is added to everything in the jsons. [Not Synced with Server]
 # Setting type: Boolean
@@ -569,7 +569,7 @@ ## Use @, to display the how long the player has been alive in days. Blank for nothing. [Synced with Server]
 # Setting type: String
 # Default value:  <color=red>(@ Days Alive)</color>
-Display Days Alive = 
+Display Days Alive = @
 
 ## Enable PVP XP, victor gets XP of fallen player. [Synced with Server]
 # Setting type: Boolean

```

---


### Item Config

*Files in this category with changes from RelicHeim backup:*

#### ItemConfig_Base.yml

**Status**: Modified

**Summary**: -39 changes

**Key Changes**:

**Total changes**: 39 (showing top 8)

• **Blackwood**: `` *(removed)*
• **BorealPineWood_TW**: `` *(removed)*
• **BorealWood_TW**: `` *(removed)*
• **Coins**: `` *(removed)*
• **CryptKey**: `` *(removed)*
• **DragonEgg**: `` *(removed)*
• **ElderBark**: `` *(removed)*
• **EnchantedWoodBlackForest_TW**: `` *(removed)*
• ... and 31 more changes

**Full Diff**:

```diff
--- backup/ItemConfig_Base.yml+++ current/ItemConfig_Base.yml@@ -1,4 +1,24 @@ groups:
+  CustomFood:
+  - HoneyGlazedDeer
+  - HoneyGlazedMeat
+  - HoneyGlazedNeck
+  - HoneyGlazedLox
+  - HoneyGlazedFish
+  - HoneyGlazedWolf
+  - JellyGlazedHare
+  - JellyGlazedSeeker
+  - CookedEntrails
+  - ElkJerky
+  - LoxJerky_JH
+  - SeekerJerky_JH
+  - FishJerky_JH
+  - FishStew_JH
+  - NeckJerky_JH
+  - SerpentJerky_JH
+  - FishNLoxSkewer
+  - FishMeatSkewer
+  - DandelionTea_JH
   MeadBase:
   - BarleyWineBase
   - MeadBaseTamer
@@ -25,26 +45,14 @@   - MeadBaseLingeringStaminaMedium_TW
   - MeadBaseEitrBlackForest_TW
   - MeadBaseEitrMountain_TW
-  CustomFood:
-  - HoneyGlazedDeer
-  - HoneyGlazedMeat
-  - HoneyGlazedNeck
-  - HoneyGlazedLox
-  - HoneyGlazedFish
-  - HoneyGlazedWolf
-  - JellyGlazedHare
-  - JellyGlazedSeeker
-  - CookedEntrails
-  - ElkJerky
-  - LoxJerky_JH
-  - SeekerJerky_JH
-  - FishJerky_JH
-  - FishStew_JH
-  - NeckJerky_JH
-  - SerpentJerky_JH
-  - FishNLoxSkewer
-  - FishMeatSkewer
-  - DandelionTea_JH
+  MetalsDeepNorth:
+  - RagnoriteBar_TW
+  - TyraniumBar_TW
+  - ThoradusBar_TW
+  - LokvyrBar_TW
+  - RagnoriteOre_TW
+  - TyraniumOre_TW
+  - LokvyrOre_TW
   ReduceWeight:
   - Stone
   - BlackMarble
@@ -61,122 +69,3 @@   - ArcaneScroll_SpeedBuff_TW
   - ArcaneScroll_JumpBuff_TW
   - ArcaneScroll_SlowfallBuff_TW
-  MetalsDeepNorth:
-  - RagnoriteBar_TW
-  - TyraniumBar_TW
-  - ThoradusBar_TW
-  - LokvyrBar_TW
-  - RagnoriteOre_TW
-  - TyraniumOre_TW
-  - LokvyrOre_TW
-#
-all:
-    floating: yes
-    pickup: yes
-# stuff floats in water; everything is pickable
-NeckTailGrilled:
-    floating: no
-SeekerAspic:
-    floating: no
-HoneyGlazedNeck:
-    floating: no
-# NeckTailGrilled doesnt float till its fixed due to floating in air very high.
-Stackable:
-    stack: 200
-WizardryScrolls:
-    stack: 10
-DragonEgg:
-    stack: 3
-    weight: 100
-SurtrDrakeEgg_TW:
-    teleportable: yes
-    weight: 100
-CryptKey:
-    stack: 10
-MeadBase:
-    stack: 100
-mmo_mead_minor:
-    stack: 100
-mmo_mead_med:
-    stack: 100
-mmo_mead_greater:
-    stack: 100
-Food:
-    stack: 200
-    loss: no
-CustomFood:
-    stack: 200
-    loss: no
-Food Backpack:
-    loss: no
-# food stacks to 200 and doesn't be removed from inventory on death
-metal:
-    teleportable: no
-    stack: 100
-    Weight: 10
-ore:
-    teleportable: no
-    stack: 100
-    Weight: 10
-MetalsDeepNorth:
-    teleportable: no
-    stack: 200
-    Weight: 10
-# ores and metals are not teleportable, stack to 100 and metals weight only 10
-ReduceWeight:
-    stack: 200
-    Weight: 1
-# stones stack to 100 and weight only 1
-trophy:
-    stack: 100
-    Weight: 2
-boss trophy:
-    stack: 100
-    Weight: 2
-# trophys stack up to 100 and weight only 2
-Coins:
-    stack: 9999
-valuable:
-    stack: 100
-    weight: 0.05
-# make coins, valuables lighter
-Wood:
-  stack: 200
-  weight: 1
-FineWood:
-    stack: 200
-    weight: 1
-RoundLog:
-    stack: 200
-    weight: 1
-ElderBark:
-    stack: 200
-    weight: 1
-YggdrasilWood:
-    stack: 200
-    weight: 1
-Blackwood:
-    stack: 200
-    weight: 1
-BorealWood_TW:
-    stack: 200
-    weight: 1
-BorealPineWood_TW:
-    stack: 200
-    weight: 1
-EnchantedWoodBlackForest_TW:
-    stack: 200
-    weight: 1
-EnchantedWoodSwamp_TW:
-    stack: 200
-    weight: 1
-EnchantedWoodMountain_TW:
-    stack: 200
-    weight: 1
-EnchantedWoodPlains_TW:
-    stack: 200
-    weight: 1
-EnchantedWoodMistlands_TW:
-    stack: 200
-    weight: 1
-# All Wood types stack to 100 and weight half
```

---


### Mushroom Monsters

*Files in this category with changes from RelicHeim backup:*

#### horemvore.MushroomMonsters.cfg

**Status**: Modified

**Summary**: +2, -72 changes

**Key Changes**:

**Total changes**: 74 (showing top 8)

• **attack speed**: `0.8` *(removed)*
• **count**: `5` *(removed)*
• **damage**: `0.6` *(removed)*
• **damage per star**: `0.1` *(removed)*
• **damage taken**: `` *(removed)*
• **health**: `1.2` *(removed)*
• **health per star**: `0.3` *(removed)*
• **movement speed**: `1.2` *(removed)*
• ... and 66 more changes

**Full Diff**:

```diff
--- backup/horemvore.MushroomMonsters.cfg+++ current/horemvore.MushroomMonsters.cfg@@ -1,276 +1,17 @@-#Meadows
-Greyling:
-  health: 1.5
-  damage: 2
-  damage per star: 0.6
-Neck:
-  damage: 2
-  health: 4
-  health per star: 2
-Boar:
-  health: 3
-  health per star: 1
-#BlackForest
-Greydwarf:
-  health: 1.25
-  damage: 1.6
-Greydwarf_Shaman:
-  damage: 1.66
-  health: 1.66
-Skeleton_Poison:
- BlackForest:
-  health: 1.5
-  health per star: 0.4
-  attack speed: 1.5
- Swamp:
-  health: 1.8
-  health per star: 0.4
-  attack speed: 1.5
-Skeleton:
- Swamp:
-  health: 2.2
-  damage: 2.2
-  damage per star: 0.4
-  attack speed: 1.1
- Mountain:
-  health: 2.5
-  damage: 3.2
-  damage per star: 0.6
-  attack speed: 1.15
- Plains:
-  health: 2.7
-  damage: 4.2
-  damage per star: 0.8
-  attack speed: 1.2
-Skeleton_NoArcher:
- Swamp:
-  health: 2.2
-  damage: 2.2
-  damage per star: 0.4
-  attack speed: 1.1
- Mountain:
-  health: 2.5
-  damage: 3.2
-  damage per star: 0.6
-  attack speed: 1.15
- Plains:
-  health: 2.7
-  damage: 4.2
-  damage per star: 0.8
-  attack speed: 1.2
-TentaRoot:
-  health: 2.5
-  infusion:
-   Chaos: 25
-#Swamp
-Surtling:
- attack speed: 0.8
- movement speed: 0.6
- Meadows:
-  damage: 0.6
-  damage per star: 0.2
-  health: 4
-  health per star: 2
-  effect:
-   splitting: 0
- BlackForest:
-  damage: 0.6
-  damage per star: 0.2
-  health: 4
-  health per star: 2
-  effect:
-   splitting: 0
- Swamp:
-  health: 6
-  health per star: 4
- Ashlands:
-  health: 15
-  health per star: 3
-#Mountains
-Ulv:
-  health: 2.2
-  health per star: 2.2
-Wolf:
-  health per star: 1
-  damage per star: 0.2
-  tamed:
-   damage: 0.01
-   damage per star: 0
-   health: 0.25
-   health per star: 0
-  key_defeated_Bonemass:
-   tamed:
-    damage: 0.6
-    damage per star: 0.1
-    health: 1.2
-    health per star: 0.5
-   infusion:
-    Other: 0
-   effect:
-    Quick: 0
-    Curious: 0
-    Splitting: 0
-#Ocean
-Serpent:
-  effect:
-   splitting: 0
-#Plains
-Deathsquito:
-  movement speed: 0.9
-  health: 5.2
-  damage taken:
-    Bows: 0.75
-    Crossbows: 0.75
-##Adjusted Elite Mobs 
-Troll:
-  health per star: 0.5
-  damage per star: 0.25
-  effect power:
-    Regenerating: 0.5
-  sector:
-    count: 5
-# Swamp
-Abomination:
-  health per star: 0.5
-  damage per star: 0.25
-  effect power:
-    Regenerating: 0.5
-  sector:
-    count: 5
-# Mountain
-StoneGolem:
-  health per star: 0.5
-  damage per star: 0.25
-  effect:
-    Splitting: 0
-  effect power:
-    Regenerating: 0.5
-    Splitting: 0
-  sector:
-    count: 5
-# Plains
-GoblinBrute:
-  health per star: 0.5
-  damage per star: 0.25
-  effect power:
-    Regenerating: 0.5
-  sector:
-    count: 5
-# Mistlands
-SeekerBrood:
-  health: 5.2
-  damage: 1.4
-  damage taken:
-    Fire: 0.25
-Seeker:
-  damage taken:
-    Fire: 0.5
-Gjall:
-  health per star: 0.5
-  damage per star: 0.25
-  movement speed: 1.2
-  effect:
-   Quick: 0
-  effect power:
-    Regenerating: 0.5
-  sector:
-    count: 5
-    
-SeekerBrute:
-  health per star: 0.5
-  damage per star: 0.25
-  damage taken:
-    Fire: 0.5
-  effect power:
-    Regenerating: 0.5
-  sector:
-    count: 5
-# Ashlands
-Dverger:
-  AshLands:
-   health: 0.62
-   health per star: 0.32
-   damage per star: 0.2
-FallenValkyrie:
-  health per star: 0.5
-  damage per star: 0.2
-  effect power:
-    Regenerating: 0.5
-  sector:
-    count: 5
-Morgen_NonSleeping:
-  health per star: 0.5
-  damage per star: 0.2
-  effect power:
-    Regenerating: 0.5
-  sector:
-    count: 5
-BonemawSerpent:
-  health per star: 0.5
-  damage per star: 0.2
-  effect power:
-    Regenerating: 0.5
-Asksvin:
-  health per star: 0.5
-  damage per star: 0.2
-  effect power:
-    Regenerating: 0.5
-Charred_Archer:
-  damage per star: 0.2
-  effect power:
-    Regenerating: 0.5
-Charred_Melee:
-  damage per star: 0.2
-  effect power:
-    Regenerating: 0.5
-Charred_Mage:
-  damage per star: 0.2
-  effect power:
-    Regenerating: 0.5
-Charred_Twitcher:
-  damage per star: 0.2
-  effect power:
-    Regenerating: 0.5
-Troll_Summoned:
-  infusion:
-   Other: 0
-  effect:
-   Other: 0
-##Lox Adjustments and Tamed
-Lox:
- health per star: 0.5
- damage per star: 0.25
- sector:
-  count: 5
- effect power:
-  Regenerating: 0.5
- tamed:
-  damage: 0.6
-  damage per star: 0.1
-  health: 1.2
-  health per star: 0.3
-  infusion:
-   Other: 0
-  effect:
-   Quick: 0
-   Curious: 0
-   Splitting: 0
-## Tamed
-All:
- tamed:
-  size: 0
-  effect:
-    Armored: 0
-    Splitting: 0
-    Curious: 0
-    Aggressive: 0
-    Quick: 0
-    Other: 10
-  infusion:
-    Poison: 0
-    Chaos: 0
-    Fire: 0
-    Frost: 0
-    Lightning: 0
-    Spirit: 0
-    Other: 0+## Settings file was created by plugin Mushroom Monsters v1.0.2
+## Plugin GUID: horemvore.MushroomMonsters
+
+[0 Mushroom Monsters]
+
+## Admin only, Enables this mod
+# Setting type: Boolean
+# Default value: true
+Enable = true
+
+[1 Boss Locations, Runestones and Vegvisirs]
+
+## Admin only, Enables Mon Mon and Non Non locations, works on World Generation or with a mod like Upgrade World
+# Setting type: Boolean
+# Default value: false
+Enable = true
+

```

---


### Other

*Files in this category with changes from RelicHeim backup:*

#### _RelicHeimFiles/Drop,Spawn_That/spawn_that.spawnarea_spawners.PilesNests.cfg

**Status**: Modified

**Summary**: ~15 changes

**Key Changes**:

**Total changes**: 15 (showing top 8)

• **BonePileSpawnerSwamp.ConditionPlayerWithinDistance**: `20` → `30` (+10)
• **Spawner_DraugrPile.ConditionPlayerWithinDistance**: `20` → `30` (+10)
• **BonePileSpawner.SpawnInterval**: `15` → `25` (+10)
• **BonePileSpawnerMountain.ConditionMaxCloseCreatures**: `3` → `2` (-1)
• **BonePileSpawnerMountain.SpawnInterval**: `15` → `45` (+30)
• **BonePileSpawnerSwamp.ConditionMaxCloseCreatures**: `2` → `1` (-1)
• **BonePileSpawnerSwamp.ConditionMaxCreatures**: `100` → `40` (-60)
• **BonePileSpawnerSwamp.SpawnInterval**: `15` → `120` (+105)
• ... and 7 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| BonePileSpawner.SpawnInterval | 15 | 25 | +10 |
| BonePileSpawnerMountain.ConditionMaxCloseCreatures | 3 | 2 | -1 |
| BonePileSpawnerMountain.SpawnInterval | 15 | 45 | +30 |
| BonePileSpawnerSwamp.ConditionMaxCloseCreatures | 2 | 1 | -1 |
| BonePileSpawnerSwamp.ConditionMaxCreatures | 100 | 40 | -60 |
| BonePileSpawnerSwamp.ConditionPlayerWithinDistance | 20 | 30 | +10 |
| BonePileSpawnerSwamp.SpawnInterval | 15 | 120 | +105 |
| Spawner_DraugrPile.0.SpawnWeight | 4 | 3.5 | -0.5 |
| Spawner_DraugrPile.1.SpawnWeight | 4 | 2.5 | -1.5 |
| Spawner_DraugrPile.2.SpawnWeight | 1 | 0.8 | -0.2 |
| Spawner_DraugrPile.ConditionMaxCloseCreatures | 3 | 1 | -2 |
| Spawner_DraugrPile.ConditionMaxCreatures | 100 | 40 | -60 |
| Spawner_DraugrPile.ConditionPlayerWithinDistance | 20 | 30 | +10 |
| Spawner_DraugrPile.SpawnInterval | 15 | 120 | +105 |
| Spawner_GreydwarfNest.SpawnInterval | 15 | 45 | +30 |

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Drop,Spawn_That/spawn_that.spawnarea_spawners.PilesNests.cfg+++ current/_RelicHeimFiles/Drop,Spawn_That/spawn_that.spawnarea_spawners.PilesNests.cfg@@ -5,7 +5,7 @@ [Spawner_GreydwarfNest]
 IdentifyByName=Spawner_GreydwarfNest
 LevelUpChance=15
-SpawnInterval=15
+SpawnInterval=45
 SetPatrol=True
 ConditionPlayerWithinDistance=60
 ConditionMaxCloseCreatures=2
@@ -44,7 +44,7 @@ IdentifyByName=BonePileSpawner
 IdentifyByBiome=BlackForest
 LevelUpChance=15
-SpawnInterval=15
+SpawnInterval=25
 SetPatrol=True
 ConditionPlayerWithinDistance=20
 ConditionMaxCloseCreatures=2
@@ -79,11 +79,11 @@ IdentifyByName=BonePileSpawner
 IdentifyByBiome=Swamp
 LevelUpChance=15
-SpawnInterval=15
+SpawnInterval=120
 SetPatrol=True
-ConditionPlayerWithinDistance=20
-ConditionMaxCloseCreatures=2
-ConditionMaxCreatures=100
+ConditionPlayerWithinDistance=30
+ConditionMaxCloseCreatures=1
+ConditionMaxCreatures=40
 DistanceConsideredClose=20
 DistanceConsideredFar=1000
 OnGroundOnly=False
@@ -111,11 +111,11 @@ [Spawner_DraugrPile]
 IdentifyByName=Spawner_DraugrPile
 LevelUpChance=15
-SpawnInterval=15
+SpawnInterval=120
 SetPatrol=True
-ConditionPlayerWithinDistance=20
-ConditionMaxCloseCreatures=3
-ConditionMaxCreatures=100
+ConditionPlayerWithinDistance=30
+ConditionMaxCloseCreatures=1
+ConditionMaxCreatures=40
 DistanceConsideredClose=20
 DistanceConsideredFar=1000
 OnGroundOnly=False
@@ -124,19 +124,19 @@ Enabled=True
 TemplateEnabled=True
 PrefabName=Draugr
-SpawnWeight=4
+SpawnWeight=3.5
 
 [Spawner_DraugrPile.1]
 Enabled=True
 TemplateEnabled=True
 PrefabName=Draugr_Ranged
-SpawnWeight=4
+SpawnWeight=2.5
 
 [Spawner_DraugrPile.2]
 Enabled=True
 TemplateEnabled=True
 PrefabName=Draugr_Elite
-SpawnWeight=1
+SpawnWeight=0.8
 
 [Spawner_DraugrPile.3]
 Enabled=True
@@ -152,10 +152,10 @@ IdentifyByName=BonePileSpawner
 IdentifyByBiome=Mountain
 LevelUpChance=15
-SpawnInterval=15
+SpawnInterval=45
 SetPatrol=True
 ConditionPlayerWithinDistance=20
-ConditionMaxCloseCreatures=3
+ConditionMaxCloseCreatures=2
 ConditionMaxCreatures=100
 DistanceConsideredClose=20
 DistanceConsideredFar=1000

```

---

#### _RelicHeimFiles/Drop,Spawn_That/spawn_that.local_spawners.Locals.cfg

**Status**: Modified

**Summary**: -12, ~27 changes

**Key Changes**:

**Total changes**: 39 (showing top 8)

• **AbandonedLogCabin02.StoneGolem.LevelUpChance**: `50` → `25` (-25)
• **AbandonedLogCabin02.StoneGolem.RespawnTime**: `0` → `1500` (+1500)
• **AbandonedLogCabin03.Skeleton.RespawnTime**: `0` → `1500` (+1500)
• **AbandonedLogCabin03.StoneGolem.LevelMax**: `6` *(removed)*
• **AbandonedLogCabin03.StoneGolem.LevelMin**: `1` *(removed)*
• **AbandonedLogCabin03.StoneGolem.LevelUpChance**: `10` *(removed)*
• **AbandonedLogCabin03.StoneGolem.RespawnTime**: `0` *(removed)*
• **AbandonedLogCabin03.StoneGolem.TriggerDistance**: `60` *(removed)*
• ... and 31 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| AbandonedLogCabin02.StoneGolem.LevelUpChance | 50 | 25 | -25 |
| AbandonedLogCabin02.StoneGolem.RespawnTime | 0 | 1500 | +1500 |
| AbandonedLogCabin03.Skeleton.RespawnTime | 0 | 1500 | +1500 |
| AbandonedLogCabin04.Skeleton.RespawnTime | 0 | 1200 | +1200 |
| FireHole.Surtling.RespawnTime | 15 | 1200 | +1185 |
| Ruin1.Greydwarf_Shaman.RespawnTime | 0 | 1500 | +1500 |
| StoneHenge5.Goblin.RespawnTime | 0 | 900 | +900 |
| StoneTowerRuins04.Draugr.RespawnTime | 0 | 1500 | +1500 |
| StoneTowerRuins04.Skeleton.RespawnTime | 0 | 1200 | +1200 |
| StoneTowerRuins05.Skeleton.RespawnTime | 0 | 1200 | +1200 |
| SunkenCrypt4.BlobElite.RespawnTime | 0 | 1500 | +1500 |
| SunkenCrypt4.Draugr.RespawnTime | 0 | 1500 | +1500 |
| SwampHut3.Wraith.RespawnTime | 0 | 2400 | +2400 |
| SwampHut3.Wraith.TriggerDistance | 60 | 35 | -25 |
| SwampHut4.Draugr.RespawnTime | 0 | 2400 | +2400 |
| SwampHut4.Draugr.TriggerDistance | 60 | 35 | -25 |
| SwampHut4.Draugr_Ranged.RespawnTime | 0 | 2400 | +2400 |
| SwampHut4.Draugr_Ranged.TriggerDistance | 60 | 35 | -25 |
| SwampHut5.Wraith.RespawnTime | 0 | 2400 | +2400 |
| SwampHut5.Wraith.TriggerDistance | 60 | 35 | -25 |
| SwampWell1.Draugr_Elite.RespawnTime | 0 | 2400 | +2400 |
| SwampWell1.Draugr_Elite.TriggerDistance | 60 | 35 | -25 |

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Drop,Spawn_That/spawn_that.local_spawners.Locals.cfg+++ current/_RelicHeimFiles/Drop,Spawn_That/spawn_that.local_spawners.Locals.cfg@@ -10,7 +10,7 @@ LevelMin=1
 LevelMax=6
 LevelUpChance=10
-RespawnTime=0
+RespawnTime=1500
 TriggerDistance=60
 TriggerNoise=0
 SpawnInPlayerBase=False
@@ -28,11 +28,11 @@ LevelMin=1
 LevelMax=6
 LevelUpChance=15
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
+RespawnTime=2400
+TriggerDistance=35
+TriggerNoise=0
+SpawnInPlayerBase=False
+SetPatrolPoint=False
 
 [SwampHut4.Draugr]
 PrefabName=Draugr_Elite
@@ -42,11 +42,11 @@ LevelMin=1
 LevelMax=6
 LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
+RespawnTime=2400
+TriggerDistance=35
+TriggerNoise=0
+SpawnInPlayerBase=False
+SetPatrolPoint=False
 
 [SwampHut4.Draugr_Ranged]
 PrefabName=Draugr_Elite
@@ -56,11 +56,11 @@ LevelMin=1
 LevelMax=6
 LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
+RespawnTime=2400
+TriggerDistance=35
+TriggerNoise=0
+SpawnInPlayerBase=False
+SetPatrolPoint=False
 
 [SwampHut5.Wraith]
 PrefabName=HelWraith_TW
@@ -70,11 +70,11 @@ LevelMin=1
 LevelMax=6
 LevelUpChance=15
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
+RespawnTime=2400
+TriggerDistance=35
+TriggerNoise=0
+SpawnInPlayerBase=False
+SetPatrolPoint=False
 
 [SwampWell1.Draugr_Elite]
 PrefabName=HelWraith_TW
@@ -84,11 +84,11 @@ LevelMin=1
 LevelMax=6
 LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
+RespawnTime=2400
+TriggerDistance=35
+TriggerNoise=0
+SpawnInPlayerBase=False
+SetPatrolPoint=False
 
 [SunkenCrypt4.Draugr]
 PrefabName=Draugr_Elite
@@ -98,7 +98,7 @@ LevelMin=1
 LevelMax=6
 LevelUpChance=10
-RespawnTime=0
+RespawnTime=1500
 TriggerDistance=60
 TriggerNoise=0
 SpawnInPlayerBase=False
@@ -112,7 +112,7 @@ LevelMin=1
 LevelMax=6
 LevelUpChance=10
-RespawnTime=0
+RespawnTime=1500
 TriggerDistance=60
 TriggerNoise=0
 SpawnInPlayerBase=False
@@ -126,7 +126,7 @@ LevelMin=1
 LevelMax=1
 LevelUpChance=10
-RespawnTime=15
+RespawnTime=1200
 TriggerDistance=60
 TriggerNoise=0
 SpawnInPlayerBase=False
@@ -147,8 +147,8 @@ SpawnAtNight=True
 LevelMin=1
 LevelMax=6
-LevelUpChance=50
-RespawnTime=0
+LevelUpChance=25
+RespawnTime=1500
 TriggerDistance=60
 TriggerNoise=0
 SpawnInPlayerBase=False
@@ -162,21 +162,7 @@ LevelMin=1
 LevelMax=6
 LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
-
-[AbandonedLogCabin03.StoneGolem]
-PrefabName=StoneGolem
-Enabled=True
-SpawnAtDay=True
-SpawnAtNight=True
-LevelMin=1
-LevelMax=6
-LevelUpChance=10
-RespawnTime=0
+RespawnTime=1500
 TriggerDistance=60
 TriggerNoise=0
 SpawnInPlayerBase=False
@@ -190,7 +176,7 @@ LevelMin=1
 LevelMax=6
 LevelUpChance=10
-RespawnTime=0
+RespawnTime=1200
 TriggerDistance=60
 TriggerNoise=0
 SpawnInPlayerBase=False
@@ -204,7 +190,7 @@ LevelMin=1
 LevelMax=6
 LevelUpChance=10
-RespawnTime=0
+RespawnTime=1200
 TriggerDistance=60
 TriggerNoise=0
 SpawnInPlayerBase=False
@@ -218,7 +204,7 @@ LevelMin=1
 LevelMax=6
 LevelUpChance=10
-RespawnTime=0
+RespawnTime=1500
 TriggerDistance=60
 TriggerNoise=0
 SpawnInPlayerBase=False
@@ -232,7 +218,7 @@ LevelMin=1
 LevelMax=6
 LevelUpChance=10
-RespawnTime=0
+RespawnTime=1200
 TriggerDistance=60
 TriggerNoise=0
 SpawnInPlayerBase=False
@@ -250,8 +236,8 @@ LevelMin=1
 LevelMax=6
 LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True+RespawnTime=900
+TriggerDistance=60
+TriggerNoise=0
+SpawnInPlayerBase=False
+SetPatrolPoint=True

```

---

#### _RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zVanilla.cfg

**Status**: Modified

**Summary**: ~32 changes

**Key Changes**:

**Total changes**: 32 (showing top 8)

• **WorldSpawner.16.SpawnChance**: `20` → `19` (-1)
• **WorldSpawner.17.SpawnChance**: `15` → `14.25` (-0.75)
• **WorldSpawner.18.SpawnChance**: `30` → `28.5` (-1.5)
• **WorldSpawner.23.SpawnChance**: `20` → `14` (-6)
• **WorldSpawner.25.SpawnChance**: `2` → `1.9` (-0.1)
• **WorldSpawner.27.SpawnChance**: `30` → `28.5` (-1.5)
• **WorldSpawner.30.SpawnChance**: `15` → `14.25` (-0.75)
• **WorldSpawner.32.SpawnChance**: `20` → `14` (-6)
• ... and 24 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| WorldSpawner.16.SpawnChance | 20 | 19 | -1 |
| WorldSpawner.17.SpawnChance | 15 | 14.25 | -0.75 |
| WorldSpawner.18.SpawnChance | 30 | 28.5 | -1.5 |
| WorldSpawner.23.SpawnChance | 20 | 14 | -6 |
| WorldSpawner.25.SpawnChance | 2 | 1.9 | -0.1 |
| WorldSpawner.27.SpawnChance | 30 | 28.5 | -1.5 |
| WorldSpawner.30.SpawnChance | 15 | 14.25 | -0.75 |
| WorldSpawner.32.SpawnChance | 20 | 14 | -6 |
| WorldSpawner.40.SpawnChance | 10 | 6.4 | -3.6 |
| WorldSpawner.41.SpawnChance | 5 | 4.0 | -1 |
| WorldSpawner.41.SpawnInterval | 1000 | 1200 | +200 |
| WorldSpawner.44.SpawnChance | 20 | 12 | -8 |
| WorldSpawner.45.SpawnChance | 25.6 | 15 | -10.6 |
| WorldSpawner.50.SpawnChance | 10 | 9.5 | -0.5 |
| WorldSpawner.51.SpawnChance | 10 | 9.5 | -0.5 |
| WorldSpawner.52.SpawnChance | 35 | 33.25 | -1.75 |
| WorldSpawner.52.SpawnInterval | 2000 | 2400 | +400 |
| WorldSpawner.60.SpawnChance | 5 | 4.0 | -1 |
| WorldSpawner.60.SpawnInterval | 3000 | 3600 | +600 |
| WorldSpawner.61.SpawnChance | 5 | 4.0 | -1 |
| WorldSpawner.61.SpawnInterval | 3000 | 3600 | +600 |
| WorldSpawner.62.SpawnChance | 5 | 4.0 | -1 |
| WorldSpawner.62.SpawnInterval | 3000 | 3600 | +600 |
| WorldSpawner.64.SpawnChance | 20 | 19 | -1 |
| WorldSpawner.65.SpawnChance | 20 | 19 | -1 |
| WorldSpawner.66.SpawnChance | 20 | 19 | -1 |
| WorldSpawner.74.SpawnChance | 30 | 28.5 | -1.5 |
| WorldSpawner.78.SpawnChance | 20 | 19 | -1 |
| WorldSpawner.80.SpawnChance | 5 | 4.0 | -1 |
| WorldSpawner.80.SpawnInterval | 3000 | 3600 | +600 |
| WorldSpawner.81.SpawnChance | 5 | 4.0 | -1 |
| WorldSpawner.81.SpawnInterval | 3000 | 3600 | +600 |

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zVanilla.cfg+++ current/_RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zVanilla.cfg@@ -10,7 +10,7 @@ HuntPlayer=False
 MaxSpawned=4
 SpawnInterval=300
-SpawnChance=20
+SpawnChance=19
 LevelMin=1
 LevelMax=3
 LevelUpChance=-1
@@ -46,7 +46,7 @@ HuntPlayer=False
 MaxSpawned=1
 SpawnInterval=300
-SpawnChance=15
+SpawnChance=14.25
 LevelMin=1
 LevelMax=1
 LevelUpChance=-1
@@ -82,7 +82,7 @@ HuntPlayer=False
 MaxSpawned=0
 SpawnInterval=300
-SpawnChance=30
+SpawnChance=28.5
 LevelMin=1
 LevelMax=3
 LevelUpChance=-1
@@ -118,7 +118,7 @@ HuntPlayer=False
 MaxSpawned=2
 SpawnInterval=300
-SpawnChance=20
+SpawnChance=14
 SpawnDistance=70
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -145,7 +145,7 @@ HuntPlayer=True
 MaxSpawned=1
 SpawnInterval=3000
-SpawnChance=2
+SpawnChance=1.9
 LevelMin=1
 LevelMax=1
 LevelUpChance=-1
@@ -181,7 +181,7 @@ HuntPlayer=False
 MaxSpawned=2
 SpawnInterval=300
-SpawnChance=30
+SpawnChance=28.5
 SpawnDistance=20
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -212,7 +212,7 @@ HuntPlayer=False
 MaxSpawned=1
 SpawnInterval=600
-SpawnChance=15
+SpawnChance=14.25
 LevelMin=1
 LevelMax=3
 LevelUpChance=-1
@@ -247,7 +247,7 @@ HuntPlayer=False
 MaxSpawned=2
 SpawnInterval=400
-SpawnChance=20
+SpawnChance=14
 LevelMin=1
 LevelMax=3
 LevelUpChance=-1
@@ -282,7 +282,7 @@ HuntPlayer=False
 MaxSpawned=1
 SpawnInterval=600
-SpawnChance=10
+SpawnChance=6.4
 LevelMin=1
 LevelMax=3
 LevelUpChance=-1
@@ -314,8 +314,8 @@ PrefabName=Lox
 HuntPlayer=False
 MaxSpawned=3
-SpawnInterval=1000
-SpawnChance=5
+SpawnInterval=1200
+SpawnChance=4.0
 SpawnDistance=100
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -345,7 +345,7 @@ HuntPlayer=False
 MaxSpawned=1
 SpawnInterval=300
-SpawnChance=20
+SpawnChance=12
 SpawnDistance=30
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -375,7 +375,7 @@ HuntPlayer=False
 MaxSpawned=2
 SpawnInterval=300
-SpawnChance=25.6
+SpawnChance=15
 LevelMin=1
 LevelMax=1
 LevelUpChance=-1
@@ -409,7 +409,7 @@ HuntPlayer=False
 MaxSpawned=1
 SpawnInterval=500
-SpawnChance=10
+SpawnChance=9.5
 SpawnDistance=40
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -440,7 +440,7 @@ HuntPlayer=False
 MaxSpawned=1
 SpawnInterval=500
-SpawnChance=10
+SpawnChance=9.5
 SpawnDistance=40
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -470,8 +470,8 @@ PrefabName=Abomination
 HuntPlayer=False
 MaxSpawned=1
-SpawnInterval=2000
-SpawnChance=35
+SpawnInterval=2400
+SpawnChance=33.25
 LevelUpChance=-1
 LevelUpMinCenterDistance=0
 SpawnDistance=30
@@ -502,8 +502,8 @@ PrefabName=Seeker
 HuntPlayer=True
 MaxSpawned=2
-SpawnInterval=3000
-SpawnChance=5
+SpawnInterval=3600
+SpawnChance=4.0
 LevelMin=1
 LevelMax=1
 LevelUpChance=-1
@@ -539,8 +539,8 @@ PrefabName=SeekerBrood
 HuntPlayer=True
 MaxSpawned=5
-SpawnInterval=3000
-SpawnChance=5
+SpawnInterval=3600
+SpawnChance=4.0
 LevelMin=1
 LevelMax=1
 LevelUpChance=-1
@@ -576,8 +576,8 @@ PrefabName=Tick
 HuntPlayer=True
 MaxSpawned=4
-SpawnInterval=3000
-SpawnChance=5
+SpawnInterval=3600
+SpawnChance=4.0
 LevelMin=1
 LevelMax=3
 LevelUpChance=-1
@@ -618,7 +618,7 @@ HuntPlayer=False
 MaxSpawned=0
 SpawnInterval=120
-SpawnChance=20
+SpawnChance=19
 LevelMin=1
 LevelMax=1
 LevelUpChance=-1
@@ -653,7 +653,7 @@ HuntPlayer=False
 MaxSpawned=0
 SpawnInterval=120
-SpawnChance=20
+SpawnChance=19
 LevelMin=1
 LevelMax=1
 LevelUpChance=-1
@@ -688,7 +688,7 @@ HuntPlayer=False
 MaxSpawned=0
 SpawnInterval=120
-SpawnChance=20
+SpawnChance=19
 LevelMin=1
 LevelMax=1
 LevelUpChance=-1
@@ -723,7 +723,7 @@ HuntPlayer=False
 MaxSpawned=3
 SpawnInterval=200
-SpawnChance=30
+SpawnChance=28.5
 LevelUpMinCenterDistance=0
 SpawnDistance=10
 SpawnRadiusMin=50
@@ -755,7 +755,7 @@ HuntPlayer=False
 MaxSpawned=0
 SpawnInterval=120
-SpawnChance=20
+SpawnChance=19
 LevelMin=1
 LevelMax=1
 LevelUpChance=-1
@@ -789,8 +789,8 @@ PrefabName=Charred_Melee
 HuntPlayer=True
 MaxSpawned=2
-SpawnInterval=3000
-SpawnChance=5
+SpawnInterval=3600
+SpawnChance=4.0
 LevelUpMinCenterDistance=0
 SpawnDistance=10
 SpawnRadiusMin=0
@@ -823,8 +823,8 @@ PrefabName=Charred_Archer
 HuntPlayer=True
 MaxSpawned=2
-SpawnInterval=3000
-SpawnChance=5
+SpawnInterval=3600
+SpawnChance=4.0
 LevelUpMinCenterDistance=0
 SpawnDistance=10
 SpawnRadiusMin=0

```

---

#### _RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zBossSpawns.cfg

**Status**: Modified

**Summary**: ~8 changes

**Key Changes**:

**Total changes**: 8 (showing top 8)

• **WorldSpawner.34000.SpawnChance**: `50` → `47.5` (-2.5)
• **WorldSpawner.34001.SpawnChance**: `100` → `95` (-5)
• **WorldSpawner.34002.SpawnChance**: `10` → `9.5` (-0.5)
• **WorldSpawner.34003.SpawnChance**: `50` → `35` (-15)
• **WorldSpawner.34004.SpawnChance**: `50` → `35` (-15)
• **WorldSpawner.34005.SpawnChance**: `100` → `95` (-5)
• **WorldSpawner.34006.SpawnChance**: `100` → `95` (-5)
• **WorldSpawner.34007.SpawnChance**: `50` → `35` (-15)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| WorldSpawner.34000.SpawnChance | 50 | 47.5 | -2.5 |
| WorldSpawner.34001.SpawnChance | 100 | 95 | -5 |
| WorldSpawner.34002.SpawnChance | 10 | 9.5 | -0.5 |
| WorldSpawner.34003.SpawnChance | 50 | 35 | -15 |
| WorldSpawner.34004.SpawnChance | 50 | 35 | -15 |
| WorldSpawner.34005.SpawnChance | 100 | 95 | -5 |
| WorldSpawner.34006.SpawnChance | 100 | 95 | -5 |
| WorldSpawner.34007.SpawnChance | 50 | 35 | -15 |

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zBossSpawns.cfg+++ current/_RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zBossSpawns.cfg@@ -10,7 +10,7 @@ HuntPlayer=True
 MaxSpawned=1
 SpawnInterval=90
-SpawnChance=50
+SpawnChance=47.5
 RequiredEnvironments=Eikthyr
 GroupSizeMin=1
 GroupSizeMax=1
@@ -42,7 +42,7 @@ HuntPlayer=True
 MaxSpawned=5
 SpawnInterval=30
-SpawnChance=100
+SpawnChance=95
 SpawnDistance=5
 SpawnRadiusMin=1
 SpawnRadiusMax=10
@@ -80,7 +80,7 @@ HuntPlayer=True
 MaxSpawned=1
 SpawnInterval=120
-SpawnChance=10
+SpawnChance=9.5
 SpawnDistance=5
 SpawnRadiusMin=20
 SpawnRadiusMax=40
@@ -110,7 +110,7 @@ HuntPlayer=True
 MaxSpawned=2
 SpawnInterval=90
-SpawnChance=50
+SpawnChance=35
 SpawnDistance=5
 SpawnRadiusMin=20
 SpawnRadiusMax=40
@@ -147,7 +147,7 @@ HuntPlayer=True
 MaxSpawned=2
 SpawnInterval=90
-SpawnChance=50
+SpawnChance=35
 LevelUpChance=-1
 LevelUpMinCenterDistance=0
 SpawnDistance=5
@@ -186,7 +186,7 @@ HuntPlayer=True
 MaxSpawned=1
 SpawnInterval=90
-SpawnChance=50
+SpawnChance=35
 LevelUpChance=-1
 LevelUpMinCenterDistance=0
 SpawnDistance=5
@@ -225,7 +225,7 @@ HuntPlayer=True
 MaxSpawned=1
 SpawnInterval=90
-SpawnChance=100
+SpawnChance=95
 SpawnDistance=5
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -262,7 +262,7 @@ HuntPlayer=True
 MaxSpawned=2
 SpawnInterval=60
-SpawnChance=100
+SpawnChance=95
 SpawnDistance=0
 SpawnRadiusMin=1
 SpawnRadiusMax=3

```

---

#### _RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zBase.cfg

**Status**: Modified

**Summary**: ~23 changes

**Key Changes**:

**Total changes**: 23 (showing top 8)

• **WorldSpawner.32000.SpawnChance**: `10` → `7.12` (-2.88)
• **WorldSpawner.32001.SpawnChance**: `15` → `10.69` (-4.31)
• **WorldSpawner.32002.SpawnChance**: `5` → `3.56` (-1.44)
• **WorldSpawner.32003.SpawnChance**: `5` → `3.56` (-1.44)
• **WorldSpawner.32004.SpawnChance**: `5` → `3.56` (-1.44)
• **WorldSpawner.32005.SpawnChance**: `10` → `6.0` (-4)
• **WorldSpawner.32006.SpawnChance**: `10` → `7.12` (-2.88)
• **WorldSpawner.32007.SpawnChance**: `10` → `7.12` (-2.88)
• ... and 15 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| WorldSpawner.32000.SpawnChance | 10 | 7.12 | -2.88 |
| WorldSpawner.32000.SpawnInterval | 600 | 1200 | +600 |
| WorldSpawner.32001.SpawnChance | 15 | 10.69 | -4.31 |
| WorldSpawner.32001.SpawnInterval | 300 | 600 | +300 |
| WorldSpawner.32002.SpawnChance | 5 | 3.56 | -1.44 |
| WorldSpawner.32002.SpawnInterval | 200 | 400 | +200 |
| WorldSpawner.32003.SpawnChance | 5 | 3.56 | -1.44 |
| WorldSpawner.32003.SpawnInterval | 200 | 400 | +200 |
| WorldSpawner.32004.SpawnChance | 5 | 3.56 | -1.44 |
| WorldSpawner.32004.SpawnInterval | 200 | 400 | +200 |
| WorldSpawner.32005.SpawnChance | 10 | 6.0 | -4 |
| WorldSpawner.32005.SpawnInterval | 300 | 600 | +300 |
| WorldSpawner.32006.SpawnChance | 10 | 7.12 | -2.88 |
| WorldSpawner.32006.SpawnInterval | 300 | 600 | +300 |
| WorldSpawner.32007.SpawnChance | 10 | 7.12 | -2.88 |
| WorldSpawner.32007.SpawnInterval | 500 | 1000 | +500 |
| WorldSpawner.32008.SpawnChance | 5 | 3.56 | -1.44 |
| WorldSpawner.32008.SpawnInterval | 2000 | 4000 | +2000 |
| WorldSpawner.32100.SpawnChance | 10 | 7.12 | -2.88 |
| WorldSpawner.32100.SpawnInterval | 600 | 1200 | +600 |
| WorldSpawner.32101.SpawnChance | 10 | 7.12 | -2.88 |
| WorldSpawner.32101.SpawnInterval | 600 | 1200 | +600 |

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zBase.cfg+++ current/_RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zBase.cfg@@ -9,8 +9,8 @@ PrefabName=Skeleton_Poison
 HuntPlayer=False
 MaxSpawned=2
-SpawnInterval=600
-SpawnChance=10
+SpawnInterval=1200
+SpawnChance=7.12
 LevelUpMinCenterDistance=0
 SpawnDistance=64
 SpawnRadiusMin=0
@@ -30,14 +30,14 @@ SetFaction=Boss
 
 [WorldSpawner.32001]
-Name=
+Name=Troll Night
 Enabled=True
 Biomes=BlackForest
 PrefabName=Troll
 HuntPlayer=False
 MaxSpawned=1
-SpawnInterval=300
-SpawnChance=15
+SpawnInterval=600
+SpawnChance=10.69
 SpawnDistance=64
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -66,8 +66,8 @@ PrefabName=HelWraith_TW
 HuntPlayer=False
 MaxSpawned=1
-SpawnInterval=200
-SpawnChance=5
+SpawnInterval=400
+SpawnChance=3.56
 SpawnDistance=100
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -92,8 +92,8 @@ PrefabName=Hatchling
 HuntPlayer=False
 MaxSpawned=1
-SpawnInterval=200
-SpawnChance=5
+SpawnInterval=400
+SpawnChance=3.56
 SpawnDistance=100
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -118,8 +118,8 @@ PrefabName=Deathsquito
 HuntPlayer=False
 MaxSpawned=2
-SpawnInterval=200
-SpawnChance=5
+SpawnInterval=400
+SpawnChance=3.56
 SpawnDistance=100
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -144,8 +144,8 @@ PrefabName=GoblinBrute
 HuntPlayer=False
 MaxSpawned=2
-SpawnInterval=300
-SpawnChance=10
+SpawnInterval=600
+SpawnChance=6.0
 LevelUpMinCenterDistance=0
 SpawnDistance=30
 SpawnRadiusMin=10
@@ -175,8 +175,8 @@ PrefabName=Fox_TW
 HuntPlayer=False
 MaxSpawned=4
-SpawnInterval=300
-SpawnChance=10
+SpawnInterval=600
+SpawnChance=7.12
 LevelUpMinCenterDistance=0
 SpawnDistance=64
 SpawnRadiusMin=10
@@ -206,8 +206,8 @@ PrefabName=Shark_TW
 HuntPlayer=False
 MaxSpawned=1
-SpawnInterval=500
-SpawnChance=10
+SpawnInterval=1000
+SpawnChance=7.12
 SpawnDistance=50
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -238,8 +238,8 @@ PrefabName=Morgen
 HuntPlayer=False
 MaxSpawned=2
-SpawnInterval=2000
-SpawnChance=5
+SpawnInterval=4000
+SpawnChance=3.56
 LevelUpChance=-1
 LevelUpMinCenterDistance=0
 SpawnDistance=60
@@ -275,8 +275,8 @@ PrefabName=Pickable_SeedOnion
 HuntPlayer=False
 MaxSpawned=1
-SpawnInterval=600
-SpawnChance=10
+SpawnInterval=1200
+SpawnChance=7.12
 SpawnDistance=64
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -301,8 +301,8 @@ PrefabName=Pickable_SeedTurnip
 HuntPlayer=False
 MaxSpawned=1
-SpawnInterval=600
-SpawnChance=10
+SpawnInterval=1200
+SpawnChance=7.12
 SpawnDistance=120
 SpawnRadiusMin=0
 SpawnRadiusMax=0

```

---

#### _RelicHeimFiles/Drop,Spawn_That/spawn_that.local_spawners.LocalsDungeons.cfg

**Status**: Modified

**Summary**: -12, ~1 changes

**Key Changes**:

**Total changes**: 13 (showing top 8)

• **cave_new_corridor06.Ulv.LevelMax**: `1` *(removed)*
• **cave_new_corridor06.Ulv.LevelMin**: `1` *(removed)*
• **cave_new_corridor06.Ulv.LevelUpChance**: `10` *(removed)*
• **cave_new_corridor06.Ulv.RespawnTime**: `0` *(removed)*
• **cave_new_corridor06.Ulv.TriggerDistance**: `60` *(removed)*
• **cave_new_corridor06.Ulv.Enabled**: `True` *(removed)*
• **cave_new_corridor06.Ulv.PrefabName**: `GrizzlyBear_TW` *(removed)*
• **cave_new_corridor06.Ulv.SetPatrolPoint**: `True` *(removed)*
• ... and 5 more changes

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Drop,Spawn_That/spawn_that.local_spawners.LocalsDungeons.cfg+++ current/_RelicHeimFiles/Drop,Spawn_That/spawn_that.local_spawners.LocalsDungeons.cfg@@ -100,7 +100,7 @@ SetPatrolPoint=True
 
 [sunkencrypt_new_Room1.Blob]
-PrefabName=BlobElite
+PrefabName=Blob
 Enabled=True
 SpawnAtDay=True
 SpawnAtNight=True
@@ -161,20 +161,6 @@ SpawnInPlayerBase=False
 SetPatrolPoint=True
 
-[cave_new_corridor06.Ulv]
-PrefabName=GrizzlyBear_TW
-Enabled=True
-SpawnAtDay=True
-SpawnAtNight=True
-LevelMin=1
-LevelMax=1
-LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
-
 [cave_new_crossroads03.Ulv]
 PrefabName=GrizzlyBear_TW
 Enabled=True

```

---

#### _RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.Chests.cfg

**Status**: Modified

**Summary**: +296, -33, ~1 changes

**Key Changes**:

**Total changes**: 330 (showing top 8)

• **TreasureChest_CaveDeepNorth_TW.0.AmountMax**: `4` *(new setting)*
• **TreasureChest_CaveDeepNorth_TW.0.AmountMin**: `2` *(new setting)*
• **TreasureChest_CaveDeepNorth_TW.1.AmountMax**: `100` *(new setting)*
• **TreasureChest_CaveDeepNorth_TW.1.AmountMin**: `50` *(new setting)*
• **TreasureChest_CaveDeepNorth_TW.10.SetAmountMax**: `2` *(new setting)*
• **TreasureChest_CaveDeepNorth_TW.10.SetAmountMin**: `2` *(new setting)*
• **TreasureChest_DeepNorth_TW.0.AmountMax**: `4` *(new setting)*
• **TreasureChest_DeepNorth_TW.0.AmountMin**: `2` *(new setting)*
• ... and 322 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| TreasureChest_forestcrypt.10.SetTemplateWeight | 0.2 | 1 | +0.8 |

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.Chests.cfg+++ current/_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.Chests.cfg@@ -1,3 +1,64 @@+####################
+# Meadows
+####################
+
+[shipwreck_karve_chest.10]
+PrefabName=Coins
+SetTemplateWeight=1
+SetAmountMin=10
+SetAmountMax=30
+
+[shipwreck_karve_chest.11]
+PrefabName=LeatherScraps
+SetTemplateWeight=1
+SetAmountMin=2
+SetAmountMax=6
+
+[shipwreck_karve_chest.12]
+PrefabName=Flint
+SetTemplateWeight=1
+SetAmountMin=5
+SetAmountMax=10
+DisableResourceModifierScaling=true
+
+
+[TreasureChest_meadows_buried.10]
+PrefabName=Coins
+SetTemplateWeight=1
+SetAmountMin=5
+SetAmountMax=15
+
+[TreasureChest_meadows_buried.11]
+PrefabName=Amber
+SetTemplateWeight=1
+SetAmountMin=1
+SetAmountMax=2
+
+[TreasureChest_meadows_buried.12]
+PrefabName=ArrowWood
+SetTemplateWeight=0.5
+SetAmountMin=10
+SetAmountMax=20
+DisableResourceModifierScaling=true
+
+[TreasureChest_meadows.10]
+PrefabName=Flint
+SetTemplateWeight=1
+SetAmountMin=2
+SetAmountMax=4
+
+[TreasureChest_meadows.11]
+PrefabName=Resin
+SetTemplateWeight=1
+SetAmountMin=3
+SetAmountMax=6
+
+[TreasureChest_meadows.12]
+PrefabName=LeatherScraps
+SetTemplateWeight=0.5
+SetAmountMin=1
+SetAmountMax=3
+
 ####################
 # BlackForest
 ####################
@@ -10,7 +71,7 @@ 
 [TreasureChest_forestcrypt.10]
 PrefabName=SurtlingCore
-SetTemplateWeight=0.2
+SetTemplateWeight=1
 SetAmountMin=1
 SetAmountMax=2
 DisableResourceModifierScaling=true
@@ -21,15 +82,84 @@ SetAmountMin=2
 SetAmountMax=2
 
-####################
-# Swamp
-####################
-
-[TreasureChest_swamp]
+[TreasureChest_fCrypt]
 SetDropChance=100
 SetDropOnlyOnce=True
 SetDropMin=2
 SetDropMax=4
+
+[TreasureChest_fCrypt.10]
+PrefabName=SurtlingCore
+SetTemplateWeight=1
+SetAmountMin=1
+SetAmountMax=2
+DisableResourceModifierScaling=true
+
+[TreasureChest_fCrypt.11]
+PrefabName=ShardElder_TW
+SetTemplateWeight=1
+SetAmountMin=2
+SetAmountMax=2
+DisableResourceModifierScaling=true
+
+[TreasureChest_forestcrypt_hildir.0]
+PrefabName=Amber
+Weight=1
+AmountMin=2
+AmountMax=4
+
+[TreasureChest_forestcrypt_hildir.1]
+PrefabName=Coins
+Weight=1
+AmountMin=20
+AmountMax=40
+
+[TreasureChest_forestcrypt_hildir.10]
+PrefabName=ShardElder_TW
+SetTemplateWeight=1
+SetAmountMin=2
+SetAmountMax=2
+DisableResourceModifierScaling=true
+
+[TreasureChest_blackforest]
+SetDropChance=100
+SetDropOnlyOnce=True
+SetDropMin=2
+SetDropMax=4
+
+[TreasureChest_blackforest.10]
+PrefabName=CarrotSeeds
+SetTemplateWeight=0.5
+SetAmountMin=1
+SetAmountMax=2
+
+[TreasureChest_blackforest.11]
+PrefabName=Amber
+SetTemplateWeight=1
+SetAmountMin=1
+SetAmountMax=3
+
+[TreasureChest_trollcave]
+SetDropChance=100
+SetDropOnlyOnce=True
+SetDropMin=2
+SetDropMax=4
+
+[TreasureChest_trollcave.10]
+PrefabName=Coins
+SetTemplateWeight=1
+SetAmountMin=20
+SetAmountMax=40
+
+[TreasureChest_trollcave.11]
+PrefabName=TrollHide
+SetTemplateWeight=0.5
+SetAmountMin=1
+SetAmountMax=3
+
+####################
+# Swamp
+####################
 
 [TreasureChest_swamp.10]
 PrefabName=TurnipSeeds
@@ -45,12 +175,6 @@ 
 ####################
 
-[TreasureChest_sunkencrypt]
-SetDropChance=100
-SetDropOnlyOnce=True
-SetDropMin=2
-SetDropMax=3
-
 [TreasureChest_sunkencrypt.0]
 PrefabName=WitheredBone
 Weight=0.5
@@ -63,7 +187,6 @@ Weight=1
 AmountMin=10
 AmountMax=15
-ConditionGlobalKeys=defeated_gdking
 
 [TreasureChest_sunkencrypt.2] #Disabled
 PrefabName=ArrowPoison
@@ -71,7 +194,6 @@ Weight=1
 AmountMin=10
 AmountMax=15
-ConditionGlobalKeys=defeated_gdking
 
 [TreasureChest_sunkencrypt.3]
 PrefabName=Coins
@@ -105,14 +227,12 @@ Weight=1
 AmountMin=1
 AmountMax=2
-ConditionGlobalKeys=defeated_gdking
 
 [TreasureChest_sunkencrypt.8]
 PrefabName=ElderBark
 Weight=1
 AmountMin=20
 AmountMax=30
-ConditionGlobalKeys=defeated_eikthyr
 DisableResourceModifierScaling=true
 
 [TreasureChest_sunkencrypt.9]
@@ -120,7 +240,6 @@ Weight=1
 AmountMin=10
 AmountMax=15
-ConditionGlobalKeys=defeated_gdking
 DisableResourceModifierScaling=true
 
 [TreasureChest_sunkencrypt.10]
@@ -141,12 +260,6 @@ # Mountains
 ####################
 
-[TreasureChest_mountains]
-SetDropChance=100
-SetDropOnlyOnce=True
-SetDropMin=2
-SetDropMax=4
-
 [TreasureChest_mountains.10]
 PrefabName=MushroomWizardbutter_TW
 SetTemplateWeight=1
@@ -155,12 +268,6 @@ 
 ####################
 
-[TreasureChest_mountaincave]
-SetDropChance=100
-SetDropOnlyOnce=True
-SetDropMin=2
-SetDropMax=5
-
 [TreasureChest_mountaincave.10]
 PrefabName=ShardModer_TW
 SetTemplateWeight=1
@@ -168,15 +275,35 @@ SetAmountMax=2
 DisableResourceModifierScaling=true
 
+[TreasureChest_mountaincave_hildir.0]
+PrefabName=Crystal
+Weight=1
+AmountMin=5
+AmountMax=10
+DisableResourceModifierScaling=true
+
+[TreasureChest_mountaincave_hildir.1]
+PrefabName=AmberPearl
+Weight=1
+AmountMin=1
+AmountMax=3
+
+[TreasureChest_mountaincave_hildir.2]
+PrefabName=Coins
+Weight=1
+AmountMin=20
+AmountMax=50
+
+[TreasureChest_mountaincave_hildir.10]
+PrefabName=ShardModer_TW
+SetTemplateWeight=1
+SetAmountMin=2
+SetAmountMax=2
+DisableResourceModifierScaling=true
+
 ####################
 # Plains
 ####################
-
-[TreasureChest_plains_stone]
-SetDropChance=100
-SetDropOnlyOnce=True
-SetDropMin=2
-SetDropMax=4
 
 [TreasureChest_plains_stone.10]
 PrefabName=ShardYagluth_TW
@@ -187,12 +314,6 @@ 
 ####################
 
-[TreasureChest_heath]
-SetDropChance=100
-SetDropOnlyOnce=True
-SetDropMin=2
-SetDropMax=4
-
 [TreasureChest_heath.10]
 PrefabName=ShardYagluth_TW
 SetTemplateWeight=1
@@ -201,12 +322,6 @@ DisableResourceModifierScaling=true
 
 ####################
-
-[TreasureChest_heath_hildir]
-SetDropChance=100
-SetDropOnlyOnce=True
-SetDropMin=5
-SetDropMax=6
 
 [TreasureChest_heath_hildir.0]
 PrefabName=AmberPearl
@@ -237,7 +352,6 @@ Weight=0.1
 AmountMin=1
 AmountMax=2
-ConditionGlobalKeys=defeated_dragon
 DisableResourceModifierScaling=true
 
 [TreasureChest_heath_hildir.10]
@@ -245,4 +359,293 @@ SetTemplateWeight=1
 SetAmountMin=2
 SetAmountMax=2
-DisableResourceModifierScaling=true+DisableResourceModifierScaling=true
+
+[TreasureChest_plainsfortress_hildir.0]
+PrefabName=BlackMetalScrap
+Weight=1
+AmountMin=2
+AmountMax=5
+DisableResourceModifierScaling=true
+
+[TreasureChest_plainsfortress_hildir.1]
+PrefabName=Chain
+Weight=0.5
+AmountMin=1
+AmountMax=3
+
+[TreasureChest_plainsfortress_hildir.2]
+PrefabName=Coins
+Weight=1
+AmountMin=50
+AmountMax=100
+
+[TreasureChest_plainsfortress_hildir.10]
+PrefabName=ShardYagluth_TW
+SetTemplateWeight=1
+SetAmountMin=2
+SetAmountMax=2
+DisableResourceModifierScaling=true
+
+####################
+# Treasure Maps
+####################
+
+[TreasureMapChest_Meadows]
+SetDropChance=100
+SetDropOnlyOnce=True
+SetDropMin=2
+SetDropMax=4
+
+[TreasureMapChest_BlackForest]
+SetDropChance=100
+SetDropOnlyOnce=True
+SetDropMin=3
+SetDropMax=5
+
+[TreasureMapChest_Swamp]
+SetDropChance=100
+SetDropOnlyOnce=True
+SetDropMin=3
+SetDropMax=5
+
+[TreasureMapChest_Mountain]
+SetDropChance=100
+SetDropOnlyOnce=True
+SetDropMin=4
+SetDropMax=6
+
+[TreasureMapChest_Plains]
+SetDropChance=100
+SetDropOnlyOnce=True
+SetDropMin=4
+SetDropMax=6
+
+[TreasureMapChest_Mistlands]
+SetDropChance=100
+SetDropOnlyOnce=True
+SetDropMin=4
+SetDropMax=6
+
+[TreasureMapChest_AshLands]
+SetDropChance=100
+SetDropOnlyOnce=True
+SetDropMin=4
+SetDropMax=6
+
+[TreasureMapChest_DeepNorth]
+SetDropChance=100
+SetDropOnlyOnce=True
+SetDropMin=4
+SetDropMax=6
+
+####################
+# Ashlands
+####################
+
+[TreasureChest_charredfortress.0]
+PrefabName=GemstoneBlue
+Weight=0.5
+AmountMin=1
+AmountMax=1
+DisableResourceModifierScaling=true
+
+[TreasureChest_charredfortress.1]
+PrefabName=GemstoneGreen
+Weight=0.5
+AmountMin=1
+AmountMax=1
+DisableResourceModifierScaling=true
+
+[TreasureChest_charredfortress.2]
+PrefabName=GemstoneRed
+Weight=0.5
+AmountMin=1
+AmountMax=1
+DisableResourceModifierScaling=true
+
+[TreasureChest_charredfortress.3]
+PrefabName=Coins
+Weight=1
+AmountMin=500
+AmountMax=1000
+DisableResourceModifierScaling=true
+
+[TreasureChest_charredfortress.4]
+PrefabName=CharredBone
+Weight=1
+AmountMin=5
+AmountMax=10
+DisableResourceModifierScaling=true
+
+[TreasureChest_charredfortress.5]
+PrefabName=Charredskull
+Weight=1
+AmountMin=1
+AmountMax=2
+DisableResourceModifierScaling=true
+
+[TreasureChest_charredfortress.6]
+PrefabName=ShieldCore
+Weight=0.1
+AmountMin=1
+AmountMax=1
+DisableResourceModifierScaling=true
+
+[TreasureChest_charredfortress.7]
+PrefabName=MoltenCore
+Weight=0.5
+AmountMin=1
+AmountMax=2
+DisableResourceModifierScaling=true
+
+[TreasureChest_charredfortress.8]
+PrefabName=FlametalOreNew
+Weight=1
+AmountMin=10
+AmountMax=20
+ConditionGlobalKeys=defeated_queen
+DisableResourceModifierScaling=true
+
+[TreasureChest_charredfortress.10]
+PrefabName=ShardQueen_TW
+SetTemplateWeight=1
+SetAmountMin=2
+SetAmountMax=2
+DisableResourceModifierScaling=true
+
+####################
+
+[TreasureChest_ashland_stone.0]
+PrefabName=FlametalOreNew
+Weight=1
+AmountMin=5
+AmountMax=10
+ConditionGlobalKeys=defeated_queen
+DisableResourceModifierScaling=true
+
+[TreasureChest_ashland_stone.1]
+PrefabName=MagmaCore
+Weight=0.5
+AmountMin=1
+AmountMax=2
+DisableResourceModifierScaling=true
+
+[TreasureChest_ashland_stone.10]
+PrefabName=ShardQueen_TW
+SetTemplateWeight=1
+SetAmountMin=2
+SetAmountMax=2
+
+# Mistlands
+####################
+
+
+[TreasureChest_dvergrtown.10]
+PrefabName=ShardQueen_TW
+SetTemplateWeight=1
+SetAmountMin=2
+SetAmountMax=3
+DisableResourceModifierScaling=true
+
+
+[TreasureChest_dvergrtower.10]
+PrefabName=ShardQueen_TW
+SetTemplateWeight=1
+SetAmountMin=2
+SetAmountMax=3
+DisableResourceModifierScaling=true
+
+
+[TreasureChest_dvergr_loose_stone.10]
+PrefabName=ShardQueen_TW
+SetTemplateWeight=1
+SetAmountMin=2
+SetAmountMax=3
+ConditionGlobalKeys=defeated_queen
+DisableResourceModifierScaling=true
+
+####################
+# Deep North & Muspelheim
+####################
+
+[TreasureChest_DeepNorth_TW.0]
+PrefabName=YmirRemains
+Weight=1
+AmountMin=2
+AmountMax=4
+DisableResourceModifierScaling=true
+
+[TreasureChest_DeepNorth_TW.1]
+PrefabName=Coins
+Weight=1
+AmountMin=50
+AmountMax=100
+
+[TreasureChest_DeepNorth_TW.10]
+PrefabName=ShardQueen_TW
+SetTemplateWeight=1
+SetAmountMin=2
+SetAmountMax=2
+DisableResourceModifierScaling=true
+
+[TreasureChest_CaveDeepNorth_TW.0]
+PrefabName=FreezeGland
+Weight=1
+AmountMin=2
+AmountMax=4
+DisableResourceModifierScaling=true
+
+[TreasureChest_CaveDeepNorth_TW.1]
+PrefabName=Coins
+Weight=1
+AmountMin=50
+AmountMax=100
+
+[TreasureChest_CaveDeepNorth_TW.10]
+PrefabName=ShardQueen_TW
+SetTemplateWeight=1
+SetAmountMin=2
+SetAmountMax=2
+DisableResourceModifierScaling=true
+
+[TreasureChest_JotunnDungeon.0]
+PrefabName=YmirRemains
+Weight=1
+AmountMin=2
+AmountMax=4
+DisableResourceModifierScaling=true
+
+[TreasureChest_JotunnDungeon.1]
+PrefabName=Coins
+Weight=1
+AmountMin=50
+AmountMax=100
+
+[TreasureChest_JotunnDungeon.10]
+PrefabName=ShardQueen_TW
+SetTemplateWeight=1
+SetAmountMin=2
+SetAmountMax=2
+DisableResourceModifierScaling=true
+
+[TreasureChest_Muspelheim.0]
+PrefabName=MagmaCore
+Weight=0.5
+AmountMin=1
+AmountMax=2
+DisableResourceModifierScaling=true
+
+[TreasureChest_Muspelheim.1]
+PrefabName=FlametalOreNew
+Weight=1
+AmountMin=5
+AmountMax=10
+DisableResourceModifierScaling=true
+
+[TreasureChest_Muspelheim.10]
+PrefabName=ShardQueen_TW
+SetTemplateWeight=1
+SetAmountMin=2
+SetAmountMax=2
+DisableResourceModifierScaling=true

```

---

#### _RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.EpicLootChest.cfg

**Status**: Modified

**Summary**: ~17 changes

**Key Changes**:

**Total changes**: 17 (showing top 8)

• **Enchanted_Chest.10.SetTemplateWeight**: `0.2` → `0.22` (+0.02)
• **Enchanted_Chest.11.SetTemplateWeight**: `0.6` → `0.66` (+0.06)
• **Enchanted_Chest.12.SetTemplateWeight**: `0.2` → `0.22` (+0.02)
• **Enchanted_Chest.13.SetTemplateWeight**: `0.4` → `0.44` (+0.04)
• **Enchanted_Chest.14.SetTemplateWeight**: `0.1` → `0.11` (+0.01)
• **Enchanted_Chest.15.SetTemplateWeight**: `0.1` → `0.11` (+0.01)
• **Enchanted_Chest.16.SetTemplateWeight**: `0.1` → `0.11` (+0.01)
• **Enchanted_Chest.17.SetTemplateWeight**: `0.1` → `0.11` (+0.01)
• ... and 9 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| Enchanted_Chest.10.SetTemplateWeight | 0.2 | 0.22 | +0.02 |
| Enchanted_Chest.11.SetTemplateWeight | 0.6 | 0.66 | +0.06 |
| Enchanted_Chest.12.SetTemplateWeight | 0.2 | 0.22 | +0.02 |
| Enchanted_Chest.13.SetTemplateWeight | 0.4 | 0.44 | +0.04 |
| Enchanted_Chest.14.SetTemplateWeight | 0.1 | 0.11 | +0.01 |
| Enchanted_Chest.15.SetTemplateWeight | 0.1 | 0.11 | +0.01 |
| Enchanted_Chest.16.SetTemplateWeight | 0.1 | 0.11 | +0.01 |
| Enchanted_Chest.17.SetTemplateWeight | 0.1 | 0.11 | +0.01 |
| Enchanted_Chest.18.SetTemplateWeight | 0.05 | 0.055 | +0.005 |
| Enchanted_Chest.2.SetTemplateWeight | 0.95 | 1.05 | +0.1 |
| Enchanted_Chest.3.SetTemplateWeight | 1 | 1.1 | +0.1 |
| Enchanted_Chest.4.SetTemplateWeight | 0.95 | 1.05 | +0.1 |
| Enchanted_Chest.5.SetTemplateWeight | 1 | 1.1 | +0.1 |
| Enchanted_Chest.6.SetTemplateWeight | 0.8 | 0.88 | +0.08 |
| Enchanted_Chest.7.SetTemplateWeight | 0.9 | 0.99 | +0.09 |
| Enchanted_Chest.8.SetTemplateWeight | 0.8 | 0.88 | +0.08 |
| Enchanted_Chest.9.SetTemplateWeight | 0.9 | 0.99 | +0.09 |

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.EpicLootChest.cfg+++ current/_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.EpicLootChest.cfg@@ -15,28 +15,28 @@ 
 [Enchanted_Chest.2]
 PrefabName=EssenceRare
-SetTemplateWeight=0.95
+SetTemplateWeight=1.05
 SetAmountMin=2
 SetAmountMax=2
 DisableResourceModifierScaling=True
 
 [Enchanted_Chest.3]
 PrefabName=RunestoneRare
-SetTemplateWeight=1
+SetTemplateWeight=1.1
 SetAmountMin=2
 SetAmountMax=2
 DisableResourceModifierScaling=True
 
 [Enchanted_Chest.4]
 PrefabName=ShardRare
-SetTemplateWeight=0.95
+SetTemplateWeight=1.05
 SetAmountMin=2
 SetAmountMax=2
 DisableResourceModifierScaling=True
 
 [Enchanted_Chest.5]
 PrefabName=DustRare
-SetTemplateWeight=1
+SetTemplateWeight=1.1
 SetAmountMin=2
 SetAmountMax=4
 DisableResourceModifierScaling=True
@@ -45,28 +45,28 @@ 
 [Enchanted_Chest.6]
 PrefabName=EssenceEpic
-SetTemplateWeight=0.8
+SetTemplateWeight=0.88
 SetAmountMin=1
 SetAmountMax=2
 DisableResourceModifierScaling=True
 
 [Enchanted_Chest.7]
 PrefabName=RunestoneEpic
-SetTemplateWeight=0.9
+SetTemplateWeight=0.99
 SetAmountMin=1
 SetAmountMax=2
 DisableResourceModifierScaling=True
 
 [Enchanted_Chest.8]
 PrefabName=ShardEpic
-SetTemplateWeight=0.8
+SetTemplateWeight=0.88
 SetAmountMin=1
 SetAmountMax=2
 DisableResourceModifierScaling=True
 
 [Enchanted_Chest.9]
 PrefabName=DustEpic
-SetTemplateWeight=0.9
+SetTemplateWeight=0.99
 SetAmountMin=2
 SetAmountMax=3
 DisableResourceModifierScaling=True
@@ -75,28 +75,28 @@ 
 [Enchanted_Chest.10]
 PrefabName=EssenceLegendary
-SetTemplateWeight=0.2
+SetTemplateWeight=0.22
 SetAmountMin=1
 SetAmountMax=2
 DisableResourceModifierScaling=True
 
 [Enchanted_Chest.11]
 PrefabName=RunestoneLegendary
-SetTemplateWeight=0.6
+SetTemplateWeight=0.66
 SetAmountMin=1
 SetAmountMax=2
 DisableResourceModifierScaling=True
 
 [Enchanted_Chest.12]
 PrefabName=ShardLegendary
-SetTemplateWeight=0.2
+SetTemplateWeight=0.22
 SetAmountMin=1
 SetAmountMax=2
 DisableResourceModifierScaling=True
 
 [Enchanted_Chest.13]
 PrefabName=DustLegendary
-SetTemplateWeight=0.4
+SetTemplateWeight=0.44
 SetAmountMin=1
 SetAmountMax=2
 DisableResourceModifierScaling=True
@@ -105,35 +105,35 @@ 
 [Enchanted_Chest.14]
 PrefabName=EssenceMythic
-SetTemplateWeight=0.1
+SetTemplateWeight=0.11
 SetAmountMin=1
 SetAmountMax=2
 DisableResourceModifierScaling=True
 
 [Enchanted_Chest.15]
 PrefabName=RunestoneMythic
-SetTemplateWeight=0.1
+SetTemplateWeight=0.11
 SetAmountMin=1
 SetAmountMax=2
 DisableResourceModifierScaling=True
 
 [Enchanted_Chest.16]
 PrefabName=ShardMythic
-SetTemplateWeight=0.1
+SetTemplateWeight=0.11
 SetAmountMin=1
 SetAmountMax=2
 DisableResourceModifierScaling=True
 
 [Enchanted_Chest.17]
 PrefabName=DustMythic
-SetTemplateWeight=0.1
+SetTemplateWeight=0.11
 SetAmountMin=1
 SetAmountMax=2
 DisableResourceModifierScaling=True
 
 [Enchanted_Chest.18]
 PrefabName=EnchantedKey
-SetTemplateWeight=0.05
+SetTemplateWeight=0.055
 SetAmountMin=1
 SetAmountMax=2
-DisableResourceModifierScaling=True+DisableResourceModifierScaling=True

```

---

#### _RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.zBase.cfg

**Status**: Modified

**Summary**: +1, -116, ~1 changes

**Key Changes**:

**Total changes**: 118 (showing top 8)

• **Dverger.1.AmountMax**: `2` *(removed)*
• **Dverger.1.AmountMin**: `1` *(removed)*
• **Dverger.1.ChanceToDrop**: `50` *(removed)*
• **Dverger.1.ScaleByLevel**: `false` *(removed)*
• **Dverger.2.AmountMax**: `3` *(removed)*
• **Dverger.2.AmountMin**: `1` *(removed)*
• **Dverger.2.ChanceToDrop**: `100` *(removed)*
• **Dverger.2.ScaleByLevel**: `true` *(removed)*
• ... and 110 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| Troll.2.AmountMin | 3 | 5 | +2 |

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.zBase.cfg+++ current/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.zBase.cfg@@ -190,16 +190,6 @@ 
 ####################
 
-[Troll.0]
-PrefabName=Ruby
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
 [Troll.1]
 PrefabName=TrophyFrostTroll
 EnableConfig=True
@@ -213,11 +203,12 @@ [Troll.2]
 PrefabName=TrollHide
 EnableConfig=True
-AmountMin=3
+AmountMin=5
 AmountMax=5
 ChanceToDrop=100
 DropOnePerPlayer=False
 ScaleByLevel=True
+AmountLimit=20
 DisableResourceModifierScaling=True
 
 ####################
@@ -607,17 +598,6 @@ 
 ####################
 
-[Goblin.0]
-PrefabName=AmberPearl
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=1
-ChanceToDrop=25
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
 [Goblin.1]
 PrefabName=BlackMetalScrap
 EnableConfig=True
@@ -654,17 +634,6 @@ 
 ####################
 
-[GoblinArcher.0]
-PrefabName=AmberPearl
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=1
-ChanceToDrop=25
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
 [GoblinArcher.1]
 PrefabName=BlackMetalScrap
 EnableConfig=True
@@ -700,17 +669,6 @@ DisableResourceModifierScaling=True
 
 ####################
-
-[GoblinBrute.0]
-PrefabName=AmberPearl
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=25
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
 
 [GoblinBrute.1]
 PrefabName=BlackMetalScrap
@@ -758,17 +716,6 @@ 
 ####################
 
-[GoblinShaman.0]
-PrefabName=Ruby
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=25
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
 [GoblinShaman.1]
 PrefabName=BlackMetalScrap
 EnableConfig=True
@@ -887,28 +834,6 @@ ScaleByLevel=true
 DisableResourceModifierScaling=True
 
-[Dverger.1]
-PrefabName=BlackMarble
-Enable=false
-EnableConfig=true
-AmountMin=1
-AmountMax=2
-ChanceToDrop=50
-DropOnePerPlayer=false
-ScaleByLevel=false
-DisableResourceModifierScaling=True
-
-[Dverger.2]
-PrefabName=Amber
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
 [Dverger.3]
 PrefabName=TrophyDvergr
 EnableConfig=True
@@ -951,17 +876,6 @@ ScaleByLevel=true
 DisableResourceModifierScaling=True
 
-[DvergerMage.2]
-PrefabName=Amber
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
 [DvergerMage.50]
 PrefabName=JuteBlue
 EnableConfig=True
@@ -983,43 +897,6 @@ DisableResourceModifierScaling=True
 
 ####################
-
-[DvergerMageFire.2]
-PrefabName=Amber
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-####################
-
-[DvergerMageIce.2]
-PrefabName=Amber
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
-
-####################
-
-[DvergerMageSupport.2]
-PrefabName=Amber
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True
 
 [DvergerMageSupport.50]
 PrefabName=DvergrKeyFragment
@@ -1107,8 +984,6 @@ ConditionKilledByEntityType=Player
 AmountLimit=1
 
-####################
-
 [Morgen.50]
 PrefabName=GemstoneRed
 EnableConfig=True
@@ -1144,28 +1019,4 @@ DropOnePerPlayer=False
 ScaleByLevel=True
 DisableResourceModifierScaling=True
-ConditionKilledByEntityType=Player
-
-####################
-
-[DvergerAshlands.1]
-PrefabName=BlackMarble
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=2
-ChanceToDrop=50
-DropOnePerPlayer=false
-ScaleByLevel=false
-DisableResourceModifierScaling=false
-
-[DvergerAshlands.2]
-PrefabName=Amber
-Enable=true
-EnableConfig=true
-AmountMin=1
-AmountMax=3
-ChanceToDrop=100
-DropOnePerPlayer=false
-ScaleByLevel=true
-DisableResourceModifierScaling=True+ConditionKilledByEntityType=Player
```

---

#### _RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Wizardry.cfg

**Status**: Modified

**Summary**: ~1 changes

**Key Changes**:

**Total changes**: 1 (showing top 1)

• **CorruptedDvergerMage_TW.0.ChanceToDrop**: `50` → `100` (+50)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| CorruptedDvergerMage_TW.0.ChanceToDrop | 50 | 100 | +50 |

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Wizardry.cfg+++ current/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Wizardry.cfg@@ -267,7 +267,7 @@ EnableConfig=true
 AmountMin=1
 AmountMax=3
-ChanceToDrop=50
+ChanceToDrop=100
 DropOnePerPlayer=false
 ScaleByLevel=true
 DisableResourceModifierScaling=true

```

---

#### _RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Bosses.cfg

**Status**: Modified

**Summary**: ~26 changes

**Key Changes**:

**Total changes**: 26 (showing top 8)

• **Bonemass.3.SetDropOnePerPlayer**: `False` → `True`
• **BossAsmodeus_TW.0.SetDropOnePerPlayer**: `False` → `True`
• **BossGorr_TW.1.SetDropOnePerPlayer**: `False` → `True`
• **BossGorr_TW.2.SetDropOnePerPlayer**: `False` → `True`
• **BossStormHerald_TW.3.SetDropOnePerPlayer**: `False` → `True`
• **BossStormHerald_TW.4.SetDropOnePerPlayer**: `False` → `True`
• **BossSvalt_TW.0.SetDropOnePerPlayer**: `False` → `True`
• **BossVrykolathas_TW.0.SetDropOnePerPlayer**: `False` → `True`
• ... and 18 more changes

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Bosses.cfg+++ current/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Bosses.cfg@@ -8,7 +8,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=10
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 DisableResourceModifierScaling=True
 SetAmountLimit=1
@@ -19,7 +19,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=10
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 DisableResourceModifierScaling=True
 SetAmountLimit=1
@@ -30,7 +30,7 @@ SetAmountMin=5
 SetAmountMax=5
 SetChanceToDrop=100
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 SetAmountLimit=5
 ConditionNotGlobalKeys=defeated_eikthyr
@@ -46,7 +46,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=10
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 DisableResourceModifierScaling=True
 SetAmountLimit=1
@@ -57,7 +57,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=10
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 DisableResourceModifierScaling=True
 SetAmountLimit=1
@@ -72,7 +72,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=10
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 DisableResourceModifierScaling=True
 SetAmountLimit=1
@@ -99,7 +99,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=10
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 DisableResourceModifierScaling=True
 SetAmountLimit=1
@@ -114,7 +114,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=10
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 DisableResourceModifierScaling=True
 SetAmountLimit=1
@@ -129,7 +129,7 @@ SetAmountMin=5
 SetAmountMax=5
 SetChanceToDrop=100
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 DisableResourceModifierScaling=True
 SetAmountLimit=5
@@ -140,7 +140,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=10
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 DisableResourceModifierScaling=True
 SetAmountLimit=1
@@ -155,7 +155,7 @@ SetAmountMin=5
 SetAmountMax=5
 SetChanceToDrop=100
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 DisableResourceModifierScaling=True
 SetAmountLimit=5
@@ -170,7 +170,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=10
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 DisableResourceModifierScaling=True
 SetAmountLimit=1
@@ -185,7 +185,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=10
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 DisableResourceModifierScaling=True
 SetAmountLimit=1
@@ -200,7 +200,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=10
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 DisableResourceModifierScaling=True
 SetAmountLimit=1
@@ -211,7 +211,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=10
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 DisableResourceModifierScaling=True
 SetAmountLimit=1
@@ -226,7 +226,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=10
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 DisableResourceModifierScaling=True
 SetAmountLimit=1
@@ -237,7 +237,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=10
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 DisableResourceModifierScaling=True
 SetAmountLimit=1
@@ -252,7 +252,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=10
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 DisableResourceModifierScaling=True
 SetAmountLimit=1
@@ -263,7 +263,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=10
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 DisableResourceModifierScaling=True
 SetAmountLimit=1
@@ -278,7 +278,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=100
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 SetAmountLimit=1
 DisableResourceModifierScaling=True
@@ -289,7 +289,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=100
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 SetAmountLimit=1
 DisableResourceModifierScaling=True
@@ -300,7 +300,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=100
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 SetAmountLimit=1
 DisableResourceModifierScaling=True
@@ -311,7 +311,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=100
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 SetAmountLimit=1
 DisableResourceModifierScaling=True
@@ -322,7 +322,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=100
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 SetAmountLimit=1
 DisableResourceModifierScaling=True
@@ -333,7 +333,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=100
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 SetAmountLimit=1
 DisableResourceModifierScaling=True
@@ -344,7 +344,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=100
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 SetAmountLimit=1
 DisableResourceModifierScaling=True
```

---

#### _RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.GoldTrophy.cfg

**Status**: Modified

**Summary**: ~9 changes

**Key Changes**:

**Total changes**: 9 (showing top 8)

• **Bonemass.59.SetDropOnePerPlayer**: `False` → `True`
• **BossAsmodeus_TW.59.SetDropOnePerPlayer**: `False` → `True`
• **BossSvalt_TW.59.SetDropOnePerPlayer**: `False` → `True`
• **BossVrykolathas_TW.59.SetDropOnePerPlayer**: `False` → `True`
• **Dragon.59.SetDropOnePerPlayer**: `False` → `True`
• **Eikthyr.59.SetDropOnePerPlayer**: `False` → `True`
• **GoblinKing.59.SetDropOnePerPlayer**: `False` → `True`
• **SeekerQueen.59.SetDropOnePerPlayer**: `False` → `True`
• ... and 1 more changes

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.GoldTrophy.cfg+++ current/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.GoldTrophy.cfg@@ -71,7 +71,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=2.5
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 SetAmountLimit=1
 DisableResourceModifierScaling=True
@@ -82,7 +82,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=2.5
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 SetAmountLimit=1
 DisableResourceModifierScaling=True
@@ -93,7 +93,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=5
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 SetAmountLimit=1
 DisableResourceModifierScaling=True
@@ -104,7 +104,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=5
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 SetAmountLimit=1
 DisableResourceModifierScaling=True
@@ -115,7 +115,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=5
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 SetAmountLimit=1
 DisableResourceModifierScaling=True
@@ -126,7 +126,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=5
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 SetAmountLimit=1
 DisableResourceModifierScaling=True
@@ -137,7 +137,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=5
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 SetAmountLimit=1
 DisableResourceModifierScaling=true
@@ -148,7 +148,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=5
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 SetAmountLimit=1
 DisableResourceModifierScaling=true
@@ -159,7 +159,7 @@ SetAmountMin=1
 SetAmountMax=1
 SetChanceToDrop=5
-SetDropOnePerPlayer=False
+SetDropOnePerPlayer=True
 SetScaleByLevel=False
 SetAmountLimit=1
 DisableResourceModifierScaling=true
```

---

#### _RelicHeimFiles/Drop,Spawn_That/RockPiles/spawn_that.world_spawners.PileOres.cfg

**Status**: Modified

**Summary**: ~11 changes

**Key Changes**:

**Total changes**: 11 (showing top 8)

• **WorldSpawner.33000.SpawnChance**: `10` → `15` (+5)
• **WorldSpawner.33001.SpawnChance**: `10` → `15` (+5)
• **WorldSpawner.33002.SpawnChance**: `15` → `20` (+5)
• **WorldSpawner.33003.SpawnChance**: `10` → `15` (+5)
• **WorldSpawner.33004.SpawnChance**: `10` → `20` (+10)
• **WorldSpawner.33005.SpawnChance**: `5` → `15` (+10)
• **WorldSpawner.33000.SpawnInterval**: `900` → `1200` (+300)
• **WorldSpawner.33001.SpawnInterval**: `900` → `1200` (+300)
• ... and 3 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| WorldSpawner.33000.SpawnChance | 10 | 15 | +5 |
| WorldSpawner.33000.SpawnInterval | 900 | 1200 | +300 |
| WorldSpawner.33001.SpawnChance | 10 | 15 | +5 |
| WorldSpawner.33001.SpawnInterval | 900 | 1200 | +300 |
| WorldSpawner.33002.SpawnChance | 15 | 20 | +5 |
| WorldSpawner.33002.SpawnInterval | 900 | 1200 | +300 |
| WorldSpawner.33003.SpawnChance | 10 | 15 | +5 |
| WorldSpawner.33003.SpawnInterval | 900 | 1200 | +300 |
| WorldSpawner.33004.SpawnChance | 10 | 20 | +10 |
| WorldSpawner.33005.SpawnChance | 5 | 15 | +10 |
| WorldSpawner.33005.SpawnInterval | 900 | 1200 | +300 |

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Drop,Spawn_That/RockPiles/spawn_that.world_spawners.PileOres.cfg+++ current/_RelicHeimFiles/Drop,Spawn_That/RockPiles/spawn_that.world_spawners.PileOres.cfg@@ -9,8 +9,8 @@ PrefabName=MineRock_Copper
 HuntPlayer=False
 MaxSpawned=2
-SpawnInterval=900
-SpawnChance=10
+SpawnInterval=1200
+SpawnChance=15
 SpawnDistance=120
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -33,8 +33,8 @@ PrefabName=MineRock_Iron
 HuntPlayer=False
 MaxSpawned=2
-SpawnInterval=900
-SpawnChance=10
+SpawnInterval=1200
+SpawnChance=15
 SpawnDistance=120
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -55,8 +55,8 @@ PrefabName=MineRock_Tin
 HuntPlayer=False
 MaxSpawned=2
-SpawnInterval=900
-SpawnChance=15
+SpawnInterval=1200
+SpawnChance=20
 SpawnDistance=70
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -77,8 +77,8 @@ PrefabName=giant_brain
 HuntPlayer=False
 MaxSpawned=1
-SpawnInterval=900
-SpawnChance=10
+SpawnInterval=1200
+SpawnChance=15
 SpawnDistance=120
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -100,7 +100,7 @@ HuntPlayer=False
 MaxSpawned=1
 SpawnInterval=1200
-SpawnChance=10
+SpawnChance=20
 SpawnDistance=120
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -122,8 +122,8 @@ PrefabName=MineRock_Meteorite
 HuntPlayer=False
 MaxSpawned=2
-SpawnInterval=900
-SpawnChance=5
+SpawnInterval=1200
+SpawnChance=15
 SpawnDistance=120
 SpawnRadiusMin=0
 SpawnRadiusMax=0

```

---

#### _RelicHeimFiles/Drop,Spawn_That/RockPiles/drop_that.drop_table.PileOres.cfg

**Status**: Modified

**Summary**: -2 changes

**Key Changes**:

**Total changes**: 2 (showing top 2)

• **TreasureChest_charredfortress.8.ConditionGlobalKeys**: `defeated_queen` *(removed)*
• **TreasureChest_charredfortress.8.PrefabName**: `FlametalOreNew` *(removed)*

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Drop,Spawn_That/RockPiles/drop_that.drop_table.PileOres.cfg+++ current/_RelicHeimFiles/Drop,Spawn_That/RockPiles/drop_that.drop_table.PileOres.cfg@@ -359,12 +359,10 @@ DisableResourceModifierScaling=True
 
 [TreasureChest_charredfortress.8]
-PrefabName=FlametalOreNew
 Weight=1
 AmountMin=10
 AmountMax=20
 DisableResourceModifierScaling=True
-ConditionGlobalKeys=defeated_queen
 
 ###################
 # Small Rocks

```

---

#### _RelicHeimFiles/Raids/custom_raids.supplemental.WizardryRaids.cfg

**Status**: Modified

**Summary**: ~11 changes

**Key Changes**:

**Total changes**: 11 (showing top 8)

• **CorruptedMage_JH.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **CorruptedMage_JH.1.SpawnChancePerInterval**: `100` → `95` (-5)
• **FenringMage_JH.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **FenringMage_JH.1.SpawnChancePerInterval**: `100` → `95` (-5)
• **GoblinMage_JH.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **GoblinMage_JH.1.SpawnChancePerInterval**: `100` → `95` (-5)
• **GreydwarfMage_JH.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **GreydwarfMage_JH.1.SpawnChancePerInterval**: `100` → `95` (-5)
• ... and 3 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| CorruptedMage_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| CorruptedMage_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |
| FenringMage_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| FenringMage_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |
| GoblinMage_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| GoblinMage_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |
| GreydwarfMage_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| GreydwarfMage_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |
| Sheepy_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| SkeletonMage_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| SkeletonMage_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Raids/custom_raids.supplemental.WizardryRaids.cfg+++ current/_RelicHeimFiles/Raids/custom_raids.supplemental.WizardryRaids.cfg@@ -26,7 +26,7 @@ PrefabName=Sheep_TW
 MaxSpawned=3
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=2
 GroupSizeMax=3
@@ -66,7 +66,7 @@ PrefabName=GreydwarfMage_TW
 MaxSpawned=2
 SpawnInterval=45
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=2
 SpawnAtNight=True
@@ -82,7 +82,7 @@ PrefabName=Greydwarf_Shaman
 MaxSpawned=1
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=1
 GroupSizeMax=1
 SpawnAtNight=True
@@ -121,7 +121,7 @@ PrefabName=SkeletonMage_TW
 MaxSpawned=2
 SpawnInterval=45
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=2
 SpawnAtNight=True
@@ -137,7 +137,7 @@ PrefabName=Skeleton_Poison
 MaxSpawned=1
 SpawnInterval=100
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=1
 GroupSizeMax=1
 SpawnAtNight=True
@@ -176,7 +176,7 @@ PrefabName=FenringMage_TW
 MaxSpawned=2
 SpawnInterval=45
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=2
 SpawnAtNight=True
@@ -192,7 +192,7 @@ PrefabName=Fenring_Cultist
 MaxSpawned=1
 SpawnInterval=100
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=1
 GroupSizeMax=1
 SpawnAtNight=True
@@ -231,7 +231,7 @@ PrefabName=GoblinMage_TW
 MaxSpawned=2
 SpawnInterval=45
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=2
 SpawnAtNight=True
@@ -247,7 +247,7 @@ PrefabName=GoblinShaman
 MaxSpawned=1
 SpawnInterval=100
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=1
 GroupSizeMax=1
 SpawnAtNight=True
@@ -286,7 +286,7 @@ PrefabName=CorruptedDvergerMage_TW
 MaxSpawned=2
 SpawnInterval=45
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=2
 SpawnAtNight=True
@@ -302,12 +302,12 @@ PrefabName=DvergerMageSupport
 MaxSpawned=1
 SpawnInterval=100
-SpawnChancePerInterval=100
-GroupSizeMin=2
-GroupSizeMax=2
-SpawnAtNight=True
-SpawnAtDay=True
-HuntPlayer=True
-GroundOffset=0
-AltitudeMin = 0
-AltitudeMax = 1000
+SpawnChancePerInterval=95
+GroupSizeMin=2
+GroupSizeMax=2
+SpawnAtNight=True
+SpawnAtDay=True
+HuntPlayer=True
+GroundOffset=0
+AltitudeMin = 0
+AltitudeMax = 1000

```

---

#### _RelicHeimFiles/Raids/custom_raids.supplemental.MoreRaids.cfg

**Status**: Modified

**Summary**: ~33 changes

**Key Changes**:

**Total changes**: 33 (showing top 8)

• **BoarParty_JH.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **Cultist_Hunt_JH.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **Cultist_Hunt_JH.1.SpawnChancePerInterval**: `100` → `95` (-5)
• **Draugr_Daddy_JH.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **Draugr_Daddy_JH.1.SpawnChancePerInterval**: `100` → `95` (-5)
• **Draugr_Daddy_JH.2.SpawnChancePerInterval**: `100` → `95` (-5)
• **Dvergrs_JH.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **Dvergrs_JH.1.SpawnChancePerInterval**: `100` → `95` (-5)
• ... and 25 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| BoarParty_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Cultist_Hunt_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Cultist_Hunt_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |
| Draugr_Daddy_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Draugr_Daddy_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |
| Draugr_Daddy_JH.2.SpawnChancePerInterval | 100 | 95 | -5 |
| Dvergrs_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Dvergrs_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |
| Dvergrs_JH.2.SpawnChancePerInterval | 100 | 95 | -5 |
| Dvergrs_JH.3.SpawnChancePerInterval | 100 | 95 | -5 |
| Eikthyr_Resistance_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Eikthyr_Resistance_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |
| Eikthyr_Resistance_JH.2.SpawnChancePerInterval | 100 | 95 | -5 |
| Elders_Wrath_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Elders_Wrath_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |
| Floating_Death_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Forest_Healers_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Forest_Healers_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |
| FurryMadness_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Ghost_Town_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| MegaBugs_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| MegaBugs_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |
| Mosquitos_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| MutatedNecks_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Rage_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Revulting_Remains_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| RootedAlive_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Serpent_Rush_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Stony_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Surtling_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| TarParty_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Troll_Scare_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Valkyrie_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Raids/custom_raids.supplemental.MoreRaids.cfg+++ current/_RelicHeimFiles/Raids/custom_raids.supplemental.MoreRaids.cfg@@ -25,7 +25,7 @@ PrefabName=Neck
 MaxSpawned=3
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=0
 GroupSizeMin=2
 GroupSizeMax=3
@@ -42,7 +42,7 @@ PrefabName=Boar
 MaxSpawned=3
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=0
 GroupSizeMin=2
 GroupSizeMax=3
@@ -59,7 +59,7 @@ PrefabName=Greyling
 MaxSpawned=3
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=0
 GroupSizeMin=2
 GroupSizeMax=3
@@ -97,7 +97,7 @@ PrefabName=Boar
 MaxSpawned=3
 SpawnInterval=15
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=2
 GroupSizeMax=3
@@ -134,7 +134,7 @@ PrefabName=Troll
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -173,7 +173,7 @@ PrefabName=Greydwarf_Shaman
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=1
 GroupSizeMax=2
@@ -190,7 +190,7 @@ PrefabName=Greydwarf
 MaxSpawned=3
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=2
 GroupSizeMax=4
@@ -227,7 +227,7 @@ PrefabName=Greydwarf_Elite
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=1
 GroupSizeMax=2
@@ -244,7 +244,7 @@ PrefabName=Greydwarf
 MaxSpawned=3
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=2
 GroupSizeMax=4
@@ -283,7 +283,7 @@ PrefabName=Ghost
 MaxSpawned=3
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=5
 GroupSizeMin=2
 GroupSizeMax=3
@@ -319,7 +319,7 @@ PrefabName=Skeleton_Poison
 MaxSpawned=2
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=2
 GroupSizeMax=2
@@ -354,7 +354,7 @@ PrefabName=Draugr_Elite
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=1
 GroupSizeMax=2
@@ -368,7 +368,7 @@ PrefabName=Draugr_Ranged
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=1
 GroupSizeMax=2
@@ -382,7 +382,7 @@ PrefabName=Draugr
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=1
 GroupSizeMax=2
@@ -416,7 +416,7 @@ PrefabName=Wraith
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=5
 GroupSizeMin=2
 GroupSizeMax=2
@@ -450,7 +450,7 @@ PrefabName=Fenring_Cultist
 MaxSpawned=1
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=1
 GroupSizeMax=1
@@ -464,7 +464,7 @@ PrefabName=Ulv
 MaxSpawned=3
 SpawnInterval=15
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=5
 GroupSizeMin=2
 GroupSizeMax=3
@@ -497,7 +497,7 @@ PrefabName=BlobTar
 MaxSpawned=3
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=2
 GroupSizeMax=3
@@ -531,7 +531,7 @@ PrefabName=Serpent
 MaxSpawned=2
 SpawnInterval=60
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=15
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -568,7 +568,7 @@ PrefabName=Deathsquito
 MaxSpawned=4
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=30
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -603,7 +603,7 @@ PrefabName=Abomination
 MaxSpawned=1
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=1
 GroupSizeMax=1
@@ -637,7 +637,7 @@ PrefabName=StoneGolem
 MaxSpawned=2
 SpawnInterval=45
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=1
 GroupSizeMax=2
@@ -672,7 +672,7 @@ PrefabName=Lox
 MaxSpawned=2
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=1
 GroupSizeMax=2
@@ -708,7 +708,7 @@ PrefabName=GoblinBrute
 MaxSpawned=2
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=1
 GroupSizeMax=2
@@ -744,7 +744,7 @@ PrefabName=Asksvin
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=2
 GroupSizeMax=2
@@ -780,7 +780,7 @@ PrefabName=FallenValkyrie
 MaxSpawned=1
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=1
 GroupSizeMax=2
@@ -816,7 +816,7 @@ HuntPlayer=True
 MaxSpawned=4
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 SpawnRadiusMin=0
 SpawnRadiusMax=0
@@ -864,7 +864,7 @@ PrefabName=SeekerBrute
 MaxSpawned=2
 SpawnInterval=60
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=1
 GroupSizeMax=2
@@ -879,7 +879,7 @@ PrefabName=Seeker
 MaxSpawned=3
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=1
 GroupSizeMax=2
@@ -915,7 +915,7 @@ PrefabName=Dverger
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=1
 GroupSizeMax=2
@@ -930,7 +930,7 @@ PrefabName=DvergerMageFire
 MaxSpawned=1
 SpawnInterval=40
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=1
 GroupSizeMax=2
@@ -945,7 +945,7 @@ PrefabName=DvergerMageIce
 MaxSpawned=1
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=1
 GroupSizeMax=2
@@ -960,7 +960,7 @@ PrefabName=DvergerMageSupport
 MaxSpawned=1
 SpawnInterval=60
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=1
 GroupSizeMax=2

```

---

#### _RelicHeimFiles/Raids/custom_raids.supplemental.VanillaRaids.cfg

**Status**: Modified

**Summary**: ~44 changes

**Key Changes**:

**Total changes**: 44 (showing top 8)

• **army_bonemass.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **army_bonemass.1.SpawnChancePerInterval**: `100` → `95` (-5)
• **army_charred.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **army_charred.1.SpawnChancePerInterval**: `100` → `95` (-5)
• **army_charred.2.SpawnChancePerInterval**: `100` → `95` (-5)
• **army_charredspawners.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **army_charredspawners.1.SpawnChancePerInterval**: `100` → `95` (-5)
• **army_eikthyr.0.SpawnChancePerInterval**: `100` → `95` (-5)
• ... and 36 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| army_bonemass.0.SpawnChancePerInterval | 100 | 95 | -5 |
| army_bonemass.1.SpawnChancePerInterval | 100 | 95 | -5 |
| army_charred.0.SpawnChancePerInterval | 100 | 95 | -5 |
| army_charred.1.SpawnChancePerInterval | 100 | 95 | -5 |
| army_charred.2.SpawnChancePerInterval | 100 | 95 | -5 |
| army_charredspawners.0.SpawnChancePerInterval | 100 | 95 | -5 |
| army_charredspawners.1.SpawnChancePerInterval | 100 | 95 | -5 |
| army_eikthyr.0.SpawnChancePerInterval | 100 | 95 | -5 |
| army_eikthyr.1.SpawnChancePerInterval | 100 | 95 | -5 |
| army_gjall.0.SpawnChancePerInterval | 100 | 95 | -5 |
| army_gjall.0.SpawnInterval | 40 | 50 | +10 |
| army_gjall.1.SpawnChancePerInterval | 100 | 95 | -5 |
| army_gjall.1.SpawnInterval | 20 | 25 | +5 |
| army_goblin.0.SpawnChancePerInterval | 58.2 | 55.29 | -2.91 |
| army_goblin.1.SpawnChancePerInterval | 47 | 44.65 | -2.35 |
| army_goblin.2.SpawnChancePerInterval | 47 | 44.65 | -2.35 |
| army_moder.0.SpawnChancePerInterval | 100 | 95 | -5 |
| army_seekers.0.SpawnChancePerInterval | 100 | 95 | -5 |
| army_seekers.1.SpawnChancePerInterval | 100 | 95 | -5 |
| army_seekers.1.SpawnInterval | 20 | 25 | +5 |
| army_seekers.2.SpawnChancePerInterval | 100 | 95 | -5 |
| army_theelder.0.SpawnChancePerInterval | 100 | 95 | -5 |
| army_theelder.1.SpawnChancePerInterval | 100 | 95 | -5 |
| army_theelder.2.SpawnChancePerInterval | 100 | 95 | -5 |
| army_theelder.3.SpawnChancePerInterval | 100 | 95 | -5 |
| bats.0.SpawnChancePerInterval | 100 | 95 | -5 |
| blobs.0.SpawnChancePerInterval | 100 | 95 | -5 |
| blobs.1.SpawnChancePerInterval | 100 | 95 | -5 |
| foresttrolls.0.SpawnChancePerInterval | 100 | 95 | -5 |
| ghosts.0.SpawnChancePerInterval | 100 | 95 | -5 |
| ghosts.1.SpawnChancePerInterval | 100 | 95 | -5 |
| hildirboss1.0.SpawnChancePerInterval | 100 | 95 | -5 |
| hildirboss1.1.SpawnChancePerInterval | 100 | 95 | -5 |
| hildirboss1.2.SpawnChancePerInterval | 100 | 95 | -5 |
| hildirboss2.0.SpawnChancePerInterval | 100 | 95 | -5 |
| hildirboss2.1.SpawnChancePerInterval | 100 | 95 | -5 |
| hildirboss2.2.SpawnChancePerInterval | 100 | 95 | -5 |
| hildirboss3.0.SpawnChancePerInterval | 100 | 95 | -5 |
| hildirboss3.1.SpawnChancePerInterval | 100 | 95 | -5 |
| hildirboss3.2.SpawnChancePerInterval | 100 | 95 | -5 |
| skeletons.0.SpawnChancePerInterval | 100 | 95 | -5 |
| skeletons.1.SpawnChancePerInterval | 54 | 51.3 | -2.7 |
| surtlings.0.SpawnChancePerInterval | 100 | 95 | -5 |
| wolves.0.SpawnChancePerInterval | 100 | 95 | -5 |

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Raids/custom_raids.supplemental.VanillaRaids.cfg+++ current/_RelicHeimFiles/Raids/custom_raids.supplemental.VanillaRaids.cfg@@ -26,7 +26,7 @@ HuntPlayer=True
 MaxSpawned=2
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -56,7 +56,7 @@ HuntPlayer=True
 MaxSpawned=2
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -107,7 +107,7 @@ HuntPlayer=True
 MaxSpawned=8
 SpawnInterval=10
-SpawnChancePerInterval=58.2
+SpawnChancePerInterval=55.29
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -137,7 +137,7 @@ HuntPlayer=True
 MaxSpawned=2
 SpawnInterval=20
-SpawnChancePerInterval=47
+SpawnChancePerInterval=44.65
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -167,7 +167,7 @@ HuntPlayer=True
 MaxSpawned=1
 SpawnInterval=20
-SpawnChancePerInterval=47
+SpawnChancePerInterval=44.65
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -219,7 +219,7 @@ HuntPlayer=True
 MaxSpawned=6
 SpawnInterval=5
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=0
@@ -249,7 +249,7 @@ HuntPlayer=True
 MaxSpawned=4
 SpawnInterval=5
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=0
@@ -279,7 +279,7 @@ HuntPlayer=True
 MaxSpawned=1
 SpawnInterval=5
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -309,7 +309,7 @@ HuntPlayer=True
 MaxSpawned=1
 SpawnInterval=5
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -360,7 +360,7 @@ HuntPlayer=True
 MaxSpawned=6
 SpawnInterval=2
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -411,7 +411,7 @@ HuntPlayer=True
 MaxSpawned=20
 SpawnInterval=10
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -441,7 +441,7 @@ HuntPlayer=True
 MaxSpawned=1
 SpawnInterval=15
-SpawnChancePerInterval=54
+SpawnChancePerInterval=51.3
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -492,7 +492,7 @@ HuntPlayer=True
 MaxSpawned=3
 SpawnInterval=5
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -522,7 +522,7 @@ HuntPlayer=True
 MaxSpawned=6
 SpawnInterval=5
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -573,7 +573,7 @@ HuntPlayer=True
 MaxSpawned=3
 SpawnInterval=10
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -624,7 +624,7 @@ HuntPlayer=True
 MaxSpawned=5
 SpawnInterval=2
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -654,7 +654,7 @@ HuntPlayer=True
 MaxSpawned=2
 SpawnInterval=10
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -705,7 +705,7 @@ HuntPlayer=True
 MaxSpawned=2
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -756,7 +756,7 @@ HuntPlayer=True
 MaxSpawned=4
 SpawnInterval=2
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -807,7 +807,7 @@ HuntPlayer=True
 MaxSpawned=6
 SpawnInterval=5
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=0
@@ -837,7 +837,7 @@ HuntPlayer=True
 MaxSpawned=4
 SpawnInterval=5
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=0
@@ -867,7 +867,7 @@ HuntPlayer=True
 MaxSpawned=1
 SpawnInterval=5
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -897,7 +897,7 @@ HuntPlayer=True
 MaxSpawned=1
 SpawnInterval=5
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -948,7 +948,7 @@ HuntPlayer=True
 MaxSpawned=10
 SpawnInterval=10
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -998,8 +998,8 @@ PrefabName=Gjall
 HuntPlayer=True
 MaxSpawned=1
-SpawnInterval=40
-SpawnChancePerInterval=100
+SpawnInterval=50
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -1028,8 +1028,8 @@ PrefabName=Tick
 HuntPlayer=True
 MaxSpawned=4
-SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnInterval=25
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=3
 SpawnDistance=10
@@ -1080,7 +1080,7 @@ HuntPlayer=True
 MaxSpawned=5
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -1109,8 +1109,8 @@ PrefabName=SeekerBrood
 HuntPlayer=True
 MaxSpawned=2
-SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnInterval=25
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -1140,7 +1140,7 @@ HuntPlayer=True
 MaxSpawned=1
 SpawnInterval=100
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -1191,7 +1191,7 @@ HuntPlayer=True
 MaxSpawned=1
 SpawnInterval=100
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -1221,7 +1221,7 @@ HuntPlayer=True
 MaxSpawned=4
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=2
 MaxLevel=3
 SpawnDistance=10
@@ -1251,7 +1251,7 @@ HuntPlayer=True
 MaxSpawned=1
 SpawnInterval=100
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=2
 MaxLevel=3
 SpawnDistance=10
@@ -1302,7 +1302,7 @@ HuntPlayer=True
 MaxSpawned=1
 SpawnInterval=100
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -1332,7 +1332,7 @@ HuntPlayer=True
 MaxSpawned=3
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=2
 MaxLevel=3
 SpawnDistance=10
@@ -1362,7 +1362,7 @@ HuntPlayer=True
 MaxSpawned=1
 SpawnInterval=100
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=2
 MaxLevel=3
 SpawnDistance=10
@@ -1413,7 +1413,7 @@ HuntPlayer=True
 MaxSpawned=1
 SpawnInterval=100
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -1443,7 +1443,7 @@ HuntPlayer=True
 MaxSpawned=4
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=2
 MaxLevel=3
 SpawnDistance=10
@@ -1473,7 +1473,7 @@ HuntPlayer=True
 MaxSpawned=1
 SpawnInterval=100
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=2
 MaxLevel=3
 SpawnDistance=10
@@ -1524,7 +1524,7 @@ HuntPlayer=True
 MaxSpawned=2
 SpawnInterval=50
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -1554,7 +1554,7 @@ HuntPlayer=True
 MaxSpawned=3
 SpawnInterval=40
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -1584,7 +1584,7 @@ HuntPlayer=True
 MaxSpawned=3
 SpawnInterval=50
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -1635,7 +1635,7 @@ HuntPlayer=True
 MaxSpawned=2
 SpawnInterval=60
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=50
@@ -1665,7 +1665,7 @@ HuntPlayer=True
 MaxSpawned=3
 SpawnInterval=40
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -1718,7 +1718,7 @@ HuntPlayer=True
 MaxSpawned=3
 SpawnInterval=10
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10
@@ -1748,7 +1748,7 @@ HuntPlayer=True
 MaxSpawned=2
 SpawnInterval=10
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 MinLevel=1
 MaxLevel=1
 SpawnDistance=10

```

---

#### _RelicHeimFiles/Raids/custom_raids.supplemental.MonstrumDNRaids.cfg

**Status**: Modified

**Summary**: ~21 changes

**Key Changes**:

**Total changes**: 21 (showing top 8)

• **Daggerfang_Army_JH.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **Daggerfang_Army_JH.1.SpawnChancePerInterval**: `100` → `95` (-5)
• **DireWolf_Army_JH.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **DireWolf_Army_JH.1.SpawnChancePerInterval**: `100` → `95` (-5)
• **Doomcaller_Army_JH.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **Doomcaller_Army_JH.1.SpawnChancePerInterval**: `100` → `95` (-5)
• **Helhounds_Army_JH.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **Helhounds_Army_JH.1.SpawnChancePerInterval**: `100` → `95` (-5)
• ... and 13 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| Daggerfang_Army_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Daggerfang_Army_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |
| DireWolf_Army_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| DireWolf_Army_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |
| Doomcaller_Army_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Doomcaller_Army_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |
| Helhounds_Army_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Helhounds_Army_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |
| IceStalker_Army_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Jotunn_Army1_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Jotunn_Army1_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |
| Jotunn_Army_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Jotunn_Army_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |
| Legionnaire_Army_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Legionnaire_Army_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |
| Pridetusk_Army_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Storm_Army_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Storm_Army_JH.1.SpawnChancePerInterval | 50 | 47.5 | -2.5 |
| Ursa_Army_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| WarBringer_Army_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| WarBringer_Army_JH.1.SpawnChancePerInterval | 100 | 95 | -5 |

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Raids/custom_raids.supplemental.MonstrumDNRaids.cfg+++ current/_RelicHeimFiles/Raids/custom_raids.supplemental.MonstrumDNRaids.cfg@@ -24,7 +24,7 @@ PrefabName=ArcticWolf_TW
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=3
 SpawnAtNight=True
@@ -40,7 +40,7 @@ PrefabName=JotunnWolf_TW
 MaxSpawned=1
 SpawnInterval=15
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=1
 GroupSizeMax=1
 SpawnAtNight=True
@@ -76,7 +76,7 @@ PrefabName=ArcticBear_TW
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=3
 SpawnAtNight=True
@@ -112,7 +112,7 @@ PrefabName=StormFenring_TW
 MaxSpawned=1
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=3
 SpawnAtNight=True
@@ -128,7 +128,7 @@ PrefabName=StormCultist_TW
 MaxSpawned=1
 SpawnInterval=20
-SpawnChancePerInterval=50
+SpawnChancePerInterval=47.5
 GroupSizeMin=2
 GroupSizeMax=3
 SpawnAtNight=True
@@ -165,7 +165,7 @@ PrefabName=JotunnBladefist_TW
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=3
 SpawnAtNight=True
@@ -181,7 +181,7 @@ PrefabName=JotunnShaman_TW
 MaxSpawned=1
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=1
 GroupSizeMax=1
 SpawnAtNight=True
@@ -217,7 +217,7 @@ PrefabName=JotunnBrute_TW
 MaxSpawned=1
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=1
 GroupSizeMax=1
 SpawnAtNight=True
@@ -233,7 +233,7 @@ PrefabName=JotunnJuggernaut_TW
 MaxSpawned=1
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=1
 GroupSizeMax=1
 SpawnAtNight=True
@@ -269,7 +269,7 @@ PrefabName=ArcticMammoth_TW
 MaxSpawned=1
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=3
 SpawnAtNight=True
@@ -305,7 +305,7 @@ PrefabName=ArcticSerpent_TW
 MaxSpawned=2
 SpawnInterval=60
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnRadiusMin=0
 SpawnRadiusMax=0
 GroupSizeMin=2
@@ -343,7 +343,7 @@ PrefabName=SurtrHound_TW
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=3
 SpawnAtNight=True
@@ -359,7 +359,7 @@ PrefabName=SurtrBones_TW
 MaxSpawned=1
 SpawnInterval=15
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=2
 SpawnAtNight=True
@@ -395,7 +395,7 @@ PrefabName=SurtrWarbringer_TW
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=3
 SpawnAtNight=True
@@ -411,7 +411,7 @@ PrefabName=SurtrBones_TW
 MaxSpawned=1
 SpawnInterval=15
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=2
 SpawnAtNight=True
@@ -447,7 +447,7 @@ PrefabName=SurtrSeer_TW
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=3
 SpawnAtNight=True
@@ -463,7 +463,7 @@ PrefabName=SurtrBones_TW
 MaxSpawned=1
 SpawnInterval=15
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=2
 SpawnAtNight=True
@@ -499,7 +499,7 @@ PrefabName=SurtrLegionnaire_TW
 MaxSpawned=1
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=2
 SpawnAtNight=True
@@ -515,7 +515,7 @@ PrefabName=SurtrBones_TW
 MaxSpawned=1
 SpawnInterval=15
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=2
 SpawnAtNight=True
@@ -551,7 +551,7 @@ PrefabName=DaggerFang_TW
 MaxSpawned=1
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 GroupSizeMin=2
 GroupSizeMax=2
 SpawnAtNight=True
@@ -567,12 +567,12 @@ PrefabName=SurtrBones_TW
 MaxSpawned=1
 SpawnInterval=15
-SpawnChancePerInterval=100
-GroupSizeMin=2
-GroupSizeMax=2
-SpawnAtNight=True
-SpawnAtDay=True
-HuntPlayer=True
-GroundOffset=5
-AltitudeMin = 1
-AltitudeMax = 1000
+SpawnChancePerInterval=95
+GroupSizeMin=2
+GroupSizeMax=2
+SpawnAtNight=True
+SpawnAtDay=True
+HuntPlayer=True
+GroundOffset=5
+AltitudeMin = 1
+AltitudeMax = 1000

```

---

#### _RelicHeimFiles/Raids/custom_raids.supplemental.MonstrumRaids.cfg

**Status**: Modified

**Summary**: ~13 changes

**Key Changes**:

**Total changes**: 13 (showing top 8)

• **AncientOnes_JH.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **Bear_AttackBF_JH.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **Bear_AttackMN_JH.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **DeadlyKiss_JH.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **Elks_JH.0.GroupSizeMax**: `3` → `2` (-1)
• **Elks_JH.0.SpawnChancePerInterval**: `100` → `25` (-75)
• **FoxAttack_JH.0.SpawnChancePerInterval**: `100` → `95` (-5)
• **NastyCrawlers_JH.0.GroupSizeMax**: `3` → `2` (-1)
• ... and 5 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| AncientOnes_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Bear_AttackBF_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Bear_AttackMN_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| DeadlyKiss_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Elks_JH.0.GroupSizeMax | 3 | 2 | -1 |
| Elks_JH.0.SpawnChancePerInterval | 100 | 25 | -75 |
| Elks_JH.0.SpawnInterval | 20 | 15 | -5 |
| FoxAttack_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| NastyCrawlers_JH.0.GroupSizeMax | 3 | 2 | -1 |
| NastyCrawlers_JH.0.SpawnChancePerInterval | 100 | 25 | -75 |
| ProwlerHunt_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| Razorback_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |
| SharkAttack_JH.0.SpawnChancePerInterval | 100 | 95 | -5 |

**Full Diff**:

```diff
--- backup/_RelicHeimFiles/Raids/custom_raids.supplemental.MonstrumRaids.cfg+++ current/_RelicHeimFiles/Raids/custom_raids.supplemental.MonstrumRaids.cfg@@ -24,7 +24,7 @@ PrefabName=Fox_TW
 MaxSpawned=3
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=2
 GroupSizeMax=3
@@ -61,7 +61,7 @@ PrefabName=Razorback_TW
 MaxSpawned=3
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=2
 GroupSizeMax=3
@@ -99,7 +99,7 @@ PrefabName=BlackBear_TW
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=2
 GroupSizeMax=2
@@ -135,7 +135,7 @@ PrefabName=GrizzlyBear_TW
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=2
 GroupSizeMax=2
@@ -171,10 +171,10 @@ PrefabName=Crawler_TW
 MaxSpawned=3
 SpawnInterval=15
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=2
-GroupSizeMax=3
+SpawnChancePerInterval=25
+SpawnDistance=10
+GroupSizeMin=2
+GroupSizeMax=2
 HuntPlayer=True
 GroundOffset=5
 AltitudeMin = 1
@@ -205,11 +205,11 @@ Enabled=true
 PrefabName=RottingElk_TW
 MaxSpawned=3
-SpawnInterval=20
-SpawnChancePerInterval=100
-SpawnDistance=10
-GroupSizeMin=2
-GroupSizeMax=3
+SpawnInterval=15
+SpawnChancePerInterval=25
+SpawnDistance=10
+GroupSizeMin=2
+GroupSizeMax=2
 SpawnAtNight=True
 SpawnAtDay=True
 HuntPlayer=True
@@ -243,7 +243,7 @@ PrefabName=Prowler_TW
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=1
 GroupSizeMax=2
@@ -278,7 +278,7 @@ PrefabName=GDAncientShaman_TW
 MaxSpawned=2
 SpawnInterval=20
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=2
 GroupSizeMax=2
@@ -313,7 +313,7 @@ PrefabName=HelWraith_TW
 MaxSpawned=2
 SpawnInterval=30
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=10
 GroupSizeMin=2
 GroupSizeMax=2
@@ -349,7 +349,7 @@ PrefabName=Shark_TW
 MaxSpawned=2
 SpawnInterval=60
-SpawnChancePerInterval=100
+SpawnChancePerInterval=95
 SpawnDistance=15
 SpawnRadiusMin=0
 SpawnRadiusMax=0

```

---

#### wackysDatabase/Items\_RelicHeimWDB2.0\Food\Item_SerpentMeatCooked.yml

**Status**: Modified

**Summary**: ~2 changes

**Note**: No backup file mapping found for diff generation.

---

#### wackysDatabase/Items\_RelicHeimWDB2.0\Food\Item_SerpentStew.yml

**Status**: Modified

**Summary**: ~2 changes

**Note**: No backup file mapping found for diff generation.

---

#### wackysDatabase/Items\_RelicHeimWDB2.0\Food\Feasts\Item_FeastAshlands.yml

**Status**: Modified

**Summary**: ~2 changes

**Note**: No backup file mapping found for diff generation.

---

#### wackysDatabase/Items\_RelicHeimWDB2.0\Food\Feasts\Item_FeastMistlands.yml

**Status**: Modified

**Summary**: ~2 changes

**Note**: No backup file mapping found for diff generation.

---

#### EpicLoot/patches\RelicHeimPatches\AdventureData_Bounties_RelicHeim.json

**Status**: Modified

**Summary**: +20, -2 changes

**Note**: No backup file mapping found for diff generation.

---

#### EpicLoot/patches\RelicHeimPatches\MagicEffects_RelicHeim.json

**Status**: Modified

**Summary**: +1, -13 changes

**Note**: No backup file mapping found for diff generation.

---

#### EpicLoot/patches\RelicHeimPatches\zLootables_CreatureDrops_RelicHeim.json

**Status**: Modified

**Summary**: +2, -1, ~3 changes

**Note**: No backup file mapping found for diff generation.

---

#### EpicLoot/patches\RelicHeimPatches\zLootables_TreasureLoot_RelicHeim.json

**Status**: Modified

**Summary**: +1, ~3 changes

**Note**: No backup file mapping found for diff generation.

---


### Plant Everything

*Files in this category with changes from RelicHeim backup:*

#### advize.PlantEverything.cfg

**Status**: Modified

**Summary**: ~12 changes

**Key Changes**:

**Total changes**: 12 (showing top 8)

• **Berries.BlueberryRespawnTime**: `120` → `220` (+100)
• **Berries.CloudberryRespawnTime**: `120` → `300` (+180)
• **Berries.RaspberryRespawnTime**: `120` → `160` (+40)
• **Debris.PickableBranchRespawnTime**: `120` → `240` (+120)
• **Debris.PickableFlintRespawnTime**: `120` → `240` (+120)
• **Debris.PickableStoneRespawnTime**: `120` → `240` (+120)
• **Flowers.DandelionRespawnTime**: `120` → `100` (-20)
• **Flowers.ThistleRespawnTime**: `120` → `110` (-10)
• ... and 4 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| Berries.BlueberryRespawnTime | 120 | 220 | +100 |
| Berries.CloudberryRespawnTime | 120 | 300 | +180 |
| Berries.RaspberryRespawnTime | 120 | 160 | +40 |
| Debris.PickableBranchRespawnTime | 120 | 240 | +120 |
| Debris.PickableFlintRespawnTime | 120 | 240 | +120 |
| Debris.PickableStoneRespawnTime | 120 | 240 | +120 |
| Flowers.DandelionRespawnTime | 120 | 100 | -20 |
| Flowers.ThistleRespawnTime | 120 | 110 | -10 |
| Mushrooms.BlueMushroomRespawnTime | 120 | 110 | -10 |
| Mushrooms.MushroomRespawnTime | 120 | 110 | -10 |
| Mushrooms.SmokepuffRespawnTime | 120 | 100 | -20 |
| Mushrooms.YellowMushroomRespawnTime | 120 | 110 | -10 |

**Full Diff**:

```diff
--- backup/advize.PlantEverything.cfg+++ current/advize.PlantEverything.cfg@@ -1,4 +1,4 @@-## Settings file was created by plugin PlantEverything v1.18.2
+## Settings file was created by plugin PlantEverything v1.19.1
 ## Plugin GUID: advize.PlantEverything
 
 [Berries]
@@ -21,17 +21,17 @@ ## Number of minutes it takes for a raspberry bush to respawn berries.
 # Setting type: Int32
 # Default value: 300
-RaspberryRespawnTime = 120
+RaspberryRespawnTime = 160
 
 ## Number of minutes it takes for a blueberry bush to respawn berries.
 # Setting type: Int32
 # Default value: 300
-BlueberryRespawnTime = 120
+BlueberryRespawnTime = 220
 
 ## Number of minutes it takes for a cloudberry bush to respawn berries.
 # Setting type: Int32
 # Default value: 300
-CloudberryRespawnTime = 120
+CloudberryRespawnTime = 300
 
 ## Number of berries a raspberry bush will spawn.
 # Setting type: Int32
@@ -220,7 +220,7 @@ ## Number of minutes it takes for a pickable branch to respawn.
 # Setting type: Int32
 # Default value: 240
-PickableBranchRespawnTime = 120
+PickableBranchRespawnTime = 240
 
 ## Amount of stone required to place stone debris. Set to 0 to disable the ability to plant this resource.
 # Setting type: Int32
@@ -235,7 +235,7 @@ ## Number of minutes it takes for a pickable Stone to respawn.
 # Setting type: Int32
 # Default value: 0
-PickableStoneRespawnTime = 120
+PickableStoneRespawnTime = 240
 
 ## Amount of flint required to place flint debris. Set to 0 to disable the ability to plant this resource.
 # Setting type: Int32
@@ -250,7 +250,7 @@ ## Number of minutes it takes for pickable flint to respawn.
 # Setting type: Int32
 # Default value: 240
-PickableFlintRespawnTime = 120
+PickableFlintRespawnTime = 240
 
 [Difficulty]
 
@@ -319,12 +319,12 @@ ## Number of minutes it takes for thistle to respawn.
 # Setting type: Int32
 # Default value: 240
-ThistleRespawnTime = 120
+ThistleRespawnTime = 110
 
 ## Number of minutes it takes for dandelion to respawn.
 # Setting type: Int32
 # Default value: 240
-DandelionRespawnTime = 120
+DandelionRespawnTime = 100
 
 ## Number of minutes it takes for fiddlehead to respawn.
 # Setting type: Int32
@@ -428,22 +428,22 @@ ## Number of minutes it takes for mushrooms to respawn.
 # Setting type: Int32
 # Default value: 240
-MushroomRespawnTime = 120
+MushroomRespawnTime = 110
 
 ## Number of minutes it takes for yellow mushrooms to respawn.
 # Setting type: Int32
 # Default value: 240
-YellowMushroomRespawnTime = 120
+YellowMushroomRespawnTime = 110
 
 ## Number of minutes it takes for blue mushrooms to respawn.
 # Setting type: Int32
 # Default value: 240
-BlueMushroomRespawnTime = 120
+BlueMushroomRespawnTime = 110
 
 ## Number of minutes it takes for smoke puffs to respawn.
 # Setting type: Int32
 # Default value: 240
-SmokepuffRespawnTime = 120
+SmokepuffRespawnTime = 100
 
 ## Number of mushrooms a pickable mushroom spawner will spawn.
 # Setting type: Int32

```

---


### Smart Containers

*Files in this category with changes from RelicHeim backup:*

#### flueno.SmartContainers.cfg

**Status**: Modified

**Summary**: +45, -31 changes

**Key Changes**:

**Total changes**: 76 (showing top 8)

• **Explorers Backpack.Crafting Station Level**: `2` *(removed)*
• **Explorers Backpack.Maximum Crafting Station Level**: `6` *(removed)*
• **Explorers Backpack.Quality Multiplier**: `1` *(removed)*
• **2 - Backpack.Use External YAML**: `On` *(removed)*
• **General.audioFeedbackEnabled**: `true` *(new setting)*
• **General.effectFeedbackEnabled**: `true` *(new setting)*
• **General.enabled**: `true` *(new setting)*
• **General.hudMessageEnabled**: `true` *(new setting)*
• ... and 68 more changes

**Full Diff**:

```diff
--- backup/flueno.SmartContainers.cfg+++ current/flueno.SmartContainers.cfg@@ -1,187 +1,239 @@-## Settings file was created by plugin Backpacks v1.3.6
-## Plugin GUID: org.bepinex.plugins.backpacks
-
-[1 - General]
-
-## If on, the configuration is locked and can be changed by server admins only.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Lock Configuration = On
-
-[2 - Backpack]
-
-## If set to on, the YAML file from your config folder will be used, to implement custom Backpacks inside of that file.
-# Setting type: Toggle
-# Default value: Off
-# Acceptable values: Off, On
-Use External YAML = On
-
-## Just ignore this.
+## Settings file was created by plugin Smart Containers Mod v1.7.0
+## Plugin GUID: flueno.SmartContainers
+
+[General]
+
+## Nexus mod ID
 # Setting type: Int32
-# Default value: 0
-YAML Editor Anchor = 0
-
-## If on, pressing the interact key will not close the inventory.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Prevent Closing = On
-
-## Rows in a Backpack. One number for each upgrade level. Adding more numbers adds more upgrades. Changing this value does not affect existing Backpacks.
-# Setting type: String
-# Default value: 3, 3, 4, 4, 4
-Backpack Slot Rows = 3, 3, 4, 4, 4
-
-## Columns in a Backpack. One number for each upgrade level. Adding more numbers adds more upgrades. Changing this value does not affect existing Backpacks.
-# Setting type: String
-# Default value: 5, 6, 5, 6, 7
-Backpack Slot Columns = 5, 6, 5, 6, 7
-
-## Weight of items inside a Backpack.
+# Default value: 332
+NexusID = 332
+
+## Enables this mod
+# Setting type: Boolean
+# Default value: true
+enabled = true
+
+## Rearranges only stackable items
+# Setting type: Boolean
+# Default value: true
+onlyStackableItems = true
+
+## Enables hud message indicating that item was routed & placed to some other chest
+# Setting type: Boolean
+# Default value: true
+hudMessageEnabled = true
+
+## HUD message consists of Icon, item-name plus this text.
+# Setting type: String
+# Default value: Routed to another Chest
+hudMessageText = Routed to another Chest
+
+## Range within which containers will participate in resources arrangement.
 # Setting type: Int32
-# Default value: 100
-# Acceptable value range: From 0 to 100
-Backpack Weight = 100
-
-## If off, portals do not check the content of a backpack upon teleportation.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Backpack Teleportation Check = On
-
-## Allowed: Can put all backpacks into any other backpack.
-## Not Allowed: Cannot put any backpacks into another backpack.
-## Not Allowed Backpacks: Cannot put backpacks added by Backpacks into each other.
-## Not Allowed Same Backpack: Cannot put the same backpack type into each other.
-# Setting type: BackpackCeption
-# Default value: NotAllowed
-# Acceptable values: Allowed, NotAllowed, NotAllowedBackpacks, NotAllowedSameBackpack
-Backpacks in Backpacks = NotAllowed
-
-## If on, you can put backpacks that aren't empty into chests, to make the chests bigger on the inside.
-# Setting type: Toggle
-# Default value: Off
-# Acceptable values: Off, On
-Backpacks in Chests = Off
-
-## Can be used to restrict the number of backpacks a player can have in their inventory.
-## Global: Only one backpack.
-## Restricted: No other backpacks without item restrictions allowed.
-## Type: Only one backpack of each type.
-## Bypass: As many backpacks as you want.
-## None: Same as bypass, but doesn't overrule every other flag.
-# Setting type: Unique
-# Default value: Global
-# Acceptable values: None, Global, Restricted, Type, Bypass
-Unique Backpack = Global
-
-## If on, the backpack visual is hidden.
-# Setting type: Toggle
-# Default value: Off
-# Acceptable values: Off, On
-Hide Backpack = Off
-
-## If on, the backpack in your backpack slot is opened automatically, if the inventory is opened.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Auto Open Backpack = On
-
-## Name of a status effect that should be applied to the player, if the backpack is equipped.
+# Default value: 14
+# Acceptable value range: From 5 to 99
+range = 14
+
+## Change only if you wish to have even longer than ctrl+click combination (holding ctrl is mandatory since it's a 'move-stack' ingame key)
+# Setting type: KeyboardShortcut
+# Default value: LeftControl
+hkeyModifier = LeftControl
+
+## first part of gamepads transfer-item key-combo
+# Setting type: String
+# Default value: JoyLTrigger
+gamepadKey1 = JoyLTrigger
+
+## second part of gamepads transfer-item key-combo
+# Setting type: KeyboardShortcut
+# Default value: JoystickButton2
+gamepadKey2 = JoystickButton2
+
+## Enables playing of sound on successful items transfer
+# Setting type: Boolean
+# Default value: true
+audioFeedbackEnabled = true
+
+## Enables highlighting of end-target chests where items have been transferred.
+# Setting type: Boolean
+# Default value: true
+effectFeedbackEnabled = true
+
+## There are rare possibility of items loss if two players simultaneously (within a ~second) modify same containers inventory. Options are: ignore possible issue; ignore 'opened' chests; block mod if any other nearby player opened a chest
+# Setting type: ConcurrentChestModificationWorkaround
+# Default value: ExcludeContainersOpenedByOthers
+# Acceptable values: None, ExcludeContainersOpenedByOthers, BlockIfOtherContainersAreOpened
+concurrentChestModificationWorkaround = ExcludeContainersOpenedByOthers
+
+[Grouping]
+
+## Enables distributing items to containers with 'same-kinded' items (used if no nearby containers contain 'same item')
+# Setting type: Boolean
+# Default value: true
+enabled = true
+
+## Enable grouping by item-types (Trophie, Tool, Ammo, Armor, Weapon).
+# Setting type: Boolean
+# Default value: true
+itemTypeGroupsEnabled = true
+
+## Enable grouping by more broad criteria.
+# Setting type: Boolean
+# Default value: false
+fuzzyGroupingEnabled = false
+
+##  Change to 'LeftControl + LeftShift' if you want to trigger grouping with a separate hotkey (ctrl+shift+click)(holding ctrl is mandatory since it's a 'move-stack' ingame key)
+# Setting type: KeyboardShortcut
+# Default value: LeftControl
+groupingKeyModifier = LeftControl
+
+## Adds to the chest UI button [☼] which creates items-group based on the current items set in the chest.
+# Setting type: Boolean
+# Default value: true
+createGroupBtnEnabled = true
+
+## In case when createGroupBtn clicked and chest already contains some members of one ore more groups - dialog showed with option to merge items & groups into a single group.
+# Setting type: Boolean
+# Default value: true
+mergePromptEnabled = true
+
+## Adjusts btn position on inventory ui. →x:1.5..-10 ↓y:0.4..10.7  bottom-left: (1.5f, 10.7f) top-right:(-10f, 0.4f) bottom-right:(-10f, 10.7f)
+# Setting type: Vector2
+# Default value: {"x":1.5,"y":10.699999809265137}
+createGroupBtnPos = {"x":1.5,"y":10.699999809265137}
+
+[ItemGroup]
+
+## Items-group based on item-names list
+# Setting type: String
+# Default value: ruby,coins,amber,amberpearl
+valuables = ruby,coins,amber,amberpearl
+
+## Items-group based on item-names list
+# Setting type: String
+# Default value: copperore,flametalore,ironore,silverore,tinore,ironscrap,blackmetalscrap
+ore = copperore,flametalore,ironore,silverore,tinore,ironscrap,blackmetalscrap
+
+## Items-group based on item-names list
+# Setting type: String
+# Default value: stone,flint,obsidian
+rock = stone,flint,obsidian
+
+## Items-group based on item-names list
+# Setting type: String
+# Default value: copper,bronze,flametal,iron,silver,tin,blackmetal
+ingots = copper,bronze,flametal,iron,silver,tin,blackmetal
+
+## Items-group based on item-names list
+# Setting type: String
+# Default value: wood,finewood,corewood,elderbark,roundlog
+wood = wood,finewood,corewood,elderbark,roundlog
+
+## Items-group based on item-names list
+# Setting type: String
+# Default value: Mushroom,MushroomBlue,MushroomYellow,mushroomcommon
+mushrooms = Mushroom,MushroomBlue,MushroomYellow,mushroomcommon
+
+## Items-group based on item-names list
+# Setting type: String
+# Default value: Blueberries,raspberries,cloudberries,honey
+berries = Blueberries,raspberries,cloudberries,honey
+
+## Items-group based on item-names list
+# Setting type: String
+# Default value: Carrot,Turnip
+vegetables = Carrot,Turnip
+
+## Items-group based on item-names list
+# Setting type: String
+# Default value: CookedLoxMeat,NeckTailGrilled,MeatCooked,FishCooked,SerpentMeatCooked
+cookedMeat = CookedLoxMeat,NeckTailGrilled,MeatCooked,FishCooked,SerpentMeatCooked
+
+## Items-group based on item-names list
+# Setting type: String
+# Default value: CarrotSoup,Sausages,QueensJam,SerpentStew,TurnipStew,BloodPudding
+food = CarrotSoup,Sausages,QueensJam,SerpentStew,TurnipStew,BloodPudding
+
+[PostfixedItemGroups]
+
+## If both item names end with same 'postfix' - they are considered to have same group. I.e. carrotSeeds & turnipSeeds
+# Setting type: String
+# Default value: cone,seeds,pelt,hide,berries
+posfixes = cone,seeds,pelt,hide,berries
+
+[PrefixedItemGroups]
+
+## If both item names start with same 'prefix' - they are considered to have same group. I.e. arrowFire & arrowFlint
+# Setting type: String
+# Default value: trophy,mead,arrow,armor,cape,helmet,atgeir,bow,battleaxe,knife,mace,shield,sledge,spear,sword,tankard,club,mushroom,arrow
+prefixes = trophy,mead,arrow,armor,cape,helmet,atgeir,bow,battleaxe,knife,mace,shield,sledge,spear,sword,tankard,club,mushroom,arrow
+
+[Unload]
+
+## Enables Unload-all option & UI button [\||/]. Allows to batch-unload all eligible items from players inventory to their corresponding stacks & groups in nearby chests.
+# Setting type: Boolean
+# Default value: false
+enabled = false
+
+## Use existing 'place-stacks' UI button for unloading. If disabled - new UI button [\||/] will be created.
+# Setting type: Boolean
+# Default value: false
+nativeButton = false
+
+# Setting type: Vector2
+# Default value: {"x":1.5,"y":8.149999618530274}
+btnPos = {"x":1.5,"y":8.149999618530274}
+
+## If pressed - overrides createGroupBtn behaviour by passing item-names to unload 'itemsList' instead of creating new items group
+# Setting type: KeyboardShortcut
+# Default value: LeftShift
+addToItemsFilterKeyModifier = LeftShift
+
+## If enabled - check for groupingKeyModifier pressed is ignored for 'unload' button
+# Setting type: Boolean
+# Default value: true
+alwaysGrouping = true
+
+## If pressed - overrides createGroupBtn behaviour by passing item-names to unload 'itemsSkipList' instead of creating new items group
+# Setting type: KeyboardShortcut
+# Default value: LeftControl
+addToSkipItemsFilterKeyModifier = LeftControl
+
+## List of item-names allowed to be 'unloaded'
 # Setting type: String
 # Default value: 
-Equip Status Effect = 
-
-## If on, items you pick up are added to your backpack. Conditions apply.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Auto Fill Backpack = On
-
-## If on, there is a dedicated slot for your backpack. Requires AzuExtendedPlayerInventory.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Backpack Slot = On
-
-[Explorers Backpack]
-
-## Crafting station where Explorers Backpack is available.
-# Setting type: CraftingTable
-# Default value: Workbench
-# Acceptable values: Disabled, Inventory, Workbench, Cauldron, Forge, ArtisanTable, StoneCutter, MageTable, BlackForge, FoodPreparationTable, MeadKetill, Custom
-Crafting Station = Disabled
-
+itemsList = 
+
+## List of item-names to exclude from being 'unloaded'
 # Setting type: String
 # Default value: 
-Custom Crafting Station = 
-
-## Required crafting station level to craft Explorers Backpack.
-# Setting type: Int32
-# Default value: 2
-Crafting Station Level = 2
-
-## Maximum crafting station level to upgrade and repair Explorers Backpack.
-# Setting type: Int32
-# Default value: 6
-Maximum Crafting Station Level = 6
-
-## Whether only one of the ingredients is needed to craft Explorers Backpack
-# Setting type: Toggle
-# Default value: Off
-# Acceptable values: Off, On
-Require only one resource = Off
-
-## Multiplies the crafted amount based on the quality of the resources when crafting Explorers Backpack. Only works, if Require Only One Resource is true.
-# Setting type: Single
-# Default value: 1
-Quality Multiplier = 1
-
-## Item costs to craft Explorers Backpack
-# Setting type: String
-# Default value: BronzeNails:5,DeerHide:10,LeatherScraps:10
-Crafting Costs = BronzeNails:5,DeerHide:10,LeatherScraps:10
-
-## Item costs per level to upgrade Explorers Backpack
-# Setting type: String
-# Default value: Iron:5:2,ElderBark:10:2,Guck:2:2,Silver:5:3,WolfPelt:3:3,JuteRed:2:3,BlackMetal:5:4,LinenThread:10:4,LoxPelt:2:4,JuteBlue:5:5,ScaleHide:5:5,Carapace:5:5
-Upgrading Costs = Iron:5:2,ElderBark:10:2,Guck:2:2,Silver:5:3,WolfPelt:3:3,JuteRed:2:3,BlackMetal:5:4,LinenThread:10:4,LoxPelt:2:4,JuteBlue:5:5,ScaleHide:5:5,Carapace:5:5
-
-## Explorers Backpack drops from this creature.
-# Setting type: String
-# Default value: 
-Drops from = 
-
-## Weight of Explorers Backpack.
-# Setting type: Single
-# Default value: 4
-Weight = 4
-
-## Trader value of Explorers Backpack.
-# Setting type: Int32
-# Default value: 0
-Trader Value = 0
-
-## Which traders sell Explorers Backpack.
-# Setting type: Trader
-# Default value: None
-# Acceptable values: None, Haldor, Hildir
-# Multiple values can be set at the same time by separating them with , (e.g. Debug, Warning)
-Trader Selling = None
-
-## Price of Explorers Backpack at the trader.
-# Setting type: UInt32
-# Default value: 0
-Trader Price = 0
-
-## Stack size of Explorers Backpack in the trader. Also known as the number of items sold by a trader in one transaction.
-# Setting type: UInt32
-# Default value: 1
-Trader Stack = 1
-
-## Required global key to unlock Explorers Backpack at the trader.
-# Setting type: String
-# Default value: 
-Trader Required Global Key = 
-
+itemsSkipList = 
+
+## List of items group-ids from [ItemGroup] config section allowed to be 'unloaded'
+# Setting type: String
+# Default value: valuables,ore,wood,mushrooms
+groupsList = valuables,ore,wood,mushrooms
+
+# Setting type: String
+# Default value: trophy
+prefixItemGroups = trophy
+
+# Setting type: String
+# Default value: seeds
+postfixItemGroups = seeds
+
+## allow all Materials to be 'unloaded'
+# Setting type: Boolean
+# Default value: true
+materialsFiltering = true
+
+## allow all Trophies to be 'unloaded'
+# Setting type: Boolean
+# Default value: true
+trophiesFiltering = true
+
+## allow all Consumables to be 'unloaded'
+# Setting type: Boolean
+# Default value: false
+consumableFiltering = false
+

```

---


### Smoothbrain

*Files in this category with changes from RelicHeim backup:*

#### org.bepinex.plugins.tenacity.cfg

**Status**: Modified

**Summary**: ~2 changes

**Key Changes**:

**Total changes**: 2 (showing top 2)

• **skill_1612888259.Skill gain factor**: `0.4` → `0.65` (+0.25)
• **skill_1612888259.Skill loss**: `10` → `6` (-4)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| skill_1612888259.Skill gain factor | 0.4 | 0.65 | +0.25 |
| skill_1612888259.Skill loss | 10 | 6 | -4 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.tenacity.cfg+++ current/org.bepinex.plugins.tenacity.cfg@@ -7,7 +7,7 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill gain factor = 0.4
+Skill gain factor = 0.65
 
 ## The power of the skill, based on the default power.
 # Setting type: Single
@@ -19,5 +19,5 @@ # Setting type: Int32
 # Default value: 5
 # Acceptable value range: From 0 to 100
-Skill loss = 10
+Skill loss = 6
 

```

---

#### org.bepinex.plugins.sailing.cfg

**Status**: Modified

**Summary**: +56, ~11 changes

**Key Changes**:

**Total changes**: 67 (showing top 8)

• **2 - Ship Speed.Big Cargo Ship Full Requirement**: `0` *(new setting)*
• **2 - Ship Speed.Big Cargo Ship Half Requirement**: `0` *(new setting)*
• **2 - Ship Speed.Big Cargo Ship Paddle Requirement**: `0` *(new setting)*
• **2 - Ship Speed.Big Cargo Ship Speed Factor**: `1.5` *(new setting)*
• **2 - Ship Speed.Cargo Caravel Full Requirement**: `0` *(new setting)*
• **2 - Ship Speed.Cargo Caravel Half Requirement**: `0` *(new setting)*
• **2 - Ship Speed.Cargo Caravel Paddle Requirement**: `0` *(new setting)*
• **2 - Ship Speed.Cargo Caravel Speed Factor**: `1.5` *(new setting)*
• ... and 59 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| 2 - Ship Speed.Drakkar Full Requirement | 0 | 50 | +50 |
| 2 - Ship Speed.Drakkar Half Requirement | 0 | 50 | +50 |
| 2 - Ship Speed.Drakkar Paddle Requirement | 0 | 50 | +50 |
| 2 - Ship Speed.Karve Full Requirement | 0 | 10 | +10 |
| 2 - Ship Speed.Karve Half Requirement | 0 | 10 | +10 |
| 2 - Ship Speed.Karve Paddle Requirement | 0 | 10 | +10 |
| 2 - Ship Speed.Longship Full Requirement | 0 | 30 | +30 |
| 2 - Ship Speed.Longship Half Requirement | 0 | 30 | +30 |
| 2 - Ship Speed.Longship Paddle Requirement | 0 | 30 | +30 |
| 3 - Other.Skill Experience Gain Factor | 0.5 | 0.4 | -0.1 |
| 3 - Other.Skill Experience Loss | 1 | 0 | -1 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.sailing.cfg+++ current/org.bepinex.plugins.sailing.cfg@@ -50,19 +50,19 @@ # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Karve Paddle Requirement = 0
+Karve Paddle Requirement = 10
 
 ## Required sailing skill level to be able to sail a Karve with reduced sail.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Karve Half Requirement = 0
+Karve Half Requirement = 10
 
 ## Required sailing skill level to be able to sail a Karve with full sail.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Karve Full Requirement = 0
+Karve Full Requirement = 10
 
 ## Speed factor for Longship at skill level 100.
 # Setting type: Single
@@ -74,19 +74,19 @@ # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Longship Paddle Requirement = 0
+Longship Paddle Requirement = 30
 
 ## Required sailing skill level to be able to sail a Longship with reduced sail.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Longship Half Requirement = 0
+Longship Half Requirement = 30
 
 ## Required sailing skill level to be able to sail a Longship with full sail.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Longship Full Requirement = 0
+Longship Full Requirement = 30
 
 ## Speed factor for Drakkar at skill level 100.
 # Setting type: Single
@@ -98,19 +98,355 @@ # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Drakkar Paddle Requirement = 0
+Drakkar Paddle Requirement = 50
 
 ## Required sailing skill level to be able to sail a Drakkar with reduced sail.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Drakkar Half Requirement = 0
+Drakkar Half Requirement = 50
 
 ## Required sailing skill level to be able to sail a Drakkar with full sail.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Drakkar Full Requirement = 0
+Drakkar Full Requirement = 50
+
+## Speed factor for Merchant's boat at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Merchants boat Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Merchant's boat.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Merchants boat Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Merchant's boat with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Merchants boat Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Merchant's boat with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Merchants boat Full Requirement = 0
+
+## Speed factor for Cargo Ship at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Cargo Ship Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Cargo Ship.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Cargo Ship Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Cargo Ship with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Cargo Ship Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Cargo Ship with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Cargo Ship Full Requirement = 0
+
+## Speed factor for Big Cargo Ship at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Big Cargo Ship Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Big Cargo Ship.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Big Cargo Ship Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Big Cargo Ship with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Big Cargo Ship Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Big Cargo Ship with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Big Cargo Ship Full Requirement = 0
+
+## Speed factor for Cargo Caravel at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Cargo Caravel Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Cargo Caravel.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Cargo Caravel Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Cargo Caravel with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Cargo Caravel Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Cargo Caravel with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Cargo Caravel Full Requirement = 0
+
+## Speed factor for Huge Cargo Ship at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Huge Cargo Ship Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Huge Cargo Ship.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Huge Cargo Ship Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Huge Cargo Ship with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Huge Cargo Ship Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Huge Cargo Ship with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Huge Cargo Ship Full Requirement = 0
+
+## Speed factor for Rowing canoe at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Rowing canoe Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Rowing canoe.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Rowing canoe Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Rowing canoe with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Rowing canoe Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Rowing canoe with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Rowing canoe Full Requirement = 0
+
+## Speed factor for Double rowing canoe at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Double rowing canoe Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Double rowing canoe.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Double rowing canoe Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Double rowing canoe with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Double rowing canoe Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Double rowing canoe with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Double rowing canoe Full Requirement = 0
+
+## Speed factor for Little Boat at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Little Boat Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Little Boat.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Little Boat Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Little Boat with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Little Boat Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Little Boat with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Little Boat Full Requirement = 0
+
+## Speed factor for War Ship at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+War Ship Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a War Ship.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+War Ship Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a War Ship with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+War Ship Half Requirement = 0
+
+## Required sailing skill level to be able to sail a War Ship with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+War Ship Full Requirement = 0
+
+## Speed factor for War Ship Skuldelev at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+War Ship Skuldelev Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a War Ship Skuldelev.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+War Ship Skuldelev Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a War Ship Skuldelev with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+War Ship Skuldelev Half Requirement = 0
+
+## Required sailing skill level to be able to sail a War Ship Skuldelev with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+War Ship Skuldelev Full Requirement = 0
+
+## Speed factor for Taurus War Ship at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Taurus War Ship Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Taurus War Ship.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Taurus War Ship Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Taurus War Ship with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Taurus War Ship Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Taurus War Ship with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Taurus War Ship Full Requirement = 0
+
+## Speed factor for Fast Ship Skuldelev at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Fast Ship Skuldelev Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Fast Ship Skuldelev.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Fast Ship Skuldelev Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Fast Ship Skuldelev with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Fast Ship Skuldelev Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Fast Ship Skuldelev with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Fast Ship Skuldelev Full Requirement = 0
+
+## Speed factor for Goblin Boat at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Goblin Boat Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Goblin Boat.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Goblin Boat Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Goblin Boat with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Goblin Boat Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Goblin Boat with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Goblin Boat Full Requirement = 0
+
+## Speed factor for Hercule Fishing boat at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Hercule Fishing boat Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Hercule Fishing boat.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Hercule Fishing boat Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Hercule Fishing boat with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Hercule Fishing boat Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Hercule Fishing boat with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Hercule Fishing boat Full Requirement = 0
 
 [3 - Other]
 
@@ -130,13 +466,13 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill Experience Gain Factor = 0.5
+Skill Experience Gain Factor = 0.4
 
 ## How much experience to lose in the sailing skill on death.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Skill Experience Loss = 1
+Skill Experience Loss = 0
 
 ## If on, players can press a hotkey, to give their ship a nudge, if it is stuck.
 # Setting type: Toggle

```

---

#### org.bepinex.plugins.packhorse.cfg

**Status**: Modified

**Summary**: ~2 changes

**Key Changes**:

**Total changes**: 2 (showing top 2)

• **skill_1443093080.Skill gain factor**: `0.5` → `0.7` (+0.2)
• **skill_1443093080.Skill loss**: `5` → `3` (-2)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| skill_1443093080.Skill gain factor | 0.5 | 0.7 | +0.2 |
| skill_1443093080.Skill loss | 5 | 3 | -2 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.packhorse.cfg+++ current/org.bepinex.plugins.packhorse.cfg@@ -7,7 +7,7 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill gain factor = 0.5
+Skill gain factor = 0.7
 
 ## The power of the skill, based on the default power.
 # Setting type: Single
@@ -19,5 +19,5 @@ # Setting type: Int32
 # Default value: 5
 # Acceptable value range: From 0 to 100
-Skill loss = 5
+Skill loss = 3
 

```

---

#### org.bepinex.plugins.mining.cfg

**Status**: Modified

**Summary**: ~2 changes

**Key Changes**:

**Total changes**: 2 (showing top 2)

• **3 - Other.Skill Experience Gain Factor**: `0.5` → `0.72` (+0.22)
• **3 - Other.Skill Experience Loss**: `1` → `0` (-1)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| 3 - Other.Skill Experience Gain Factor | 0.5 | 0.72 | +0.22 |
| 3 - Other.Skill Experience Loss | 1 | 0 | -1 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.mining.cfg+++ current/org.bepinex.plugins.mining.cfg@@ -46,11 +46,11 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill Experience Gain Factor = 0.5
+Skill Experience Gain Factor = 0.72
 
 ## How much experience to lose in the mining skill on death.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Skill Experience Loss = 1
+Skill Experience Loss = 0
 

```

---

#### org.bepinex.plugins.lumberjacking.cfg

**Status**: Modified

**Summary**: ~2 changes

**Key Changes**:

**Total changes**: 2 (showing top 2)

• **2 - Other.Skill Experience Gain Factor**: `0.5` → `0.6` (+0.1)
• **2 - Other.Skill Experience Loss**: `1` → `0` (-1)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| 2 - Other.Skill Experience Gain Factor | 0.5 | 0.6 | +0.1 |
| 2 - Other.Skill Experience Loss | 1 | 0 | -1 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.lumberjacking.cfg+++ current/org.bepinex.plugins.lumberjacking.cfg@@ -39,11 +39,11 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill Experience Gain Factor = 0.5
+Skill Experience Gain Factor = 0.6
 
 ## How much experience to lose in the lumberjacking skill on death.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Skill Experience Loss = 1
+Skill Experience Loss = 0
 

```

---

#### org.bepinex.plugins.foraging.cfg

**Status**: Modified

**Summary**: ~5 changes

**Key Changes**:

**Total changes**: 5 (showing top 5)

• **2 - Foraging.Minimum Level Respawn Display**: `10` → `30` (+20)
• **2 - Foraging.Multiplier for Respawn Speed**: `2` → `1.5` (-0.5)
• **2 - Foraging.Maximum Mass Picking Range**: `10` → `8` (-2)
• **3 - Other.Skill Experience Gain Factor**: `0.5` → `0.60` (+0.1)
• **3 - Other.Skill Experience Loss**: `1` → `0` (-1)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| 2 - Foraging.Maximum Mass Picking Range | 10 | 8 | -2 |
| 2 - Foraging.Minimum Level Respawn Display | 10 | 30 | +20 |
| 2 - Foraging.Multiplier for Respawn Speed | 2 | 1.5 | -0.5 |
| 3 - Other.Skill Experience Gain Factor | 0.5 | 0.60 | +0.1 |
| 3 - Other.Skill Experience Loss | 1 | 0 | -1 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.foraging.cfg+++ current/org.bepinex.plugins.foraging.cfg@@ -29,19 +29,19 @@ # Setting type: Int32
 # Default value: 30
 # Acceptable value range: From 0 to 100
-Minimum Level Respawn Display = 10
+Minimum Level Respawn Display = 30
 
 ## Mass picking radius at skill level 100 in meters.
 # Setting type: Int32
 # Default value: 10
 # Acceptable value range: From 0 to 20
-Maximum Mass Picking Range = 10
+Maximum Mass Picking Range = 8
 
 ## Multiplier for the respawn speed at skill level 100.
 # Setting type: Single
 # Default value: 2
 # Acceptable value range: From 1 to 10
-Multiplier for Respawn Speed = 2
+Multiplier for Respawn Speed = 1.5
 
 [3 - Other]
 
@@ -49,11 +49,11 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill Experience Gain Factor = 0.5
+Skill Experience Gain Factor = 0.60
 
 ## How much experience to lose in the foraging skill on death.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Skill Experience Loss = 1
+Skill Experience Loss = 0
 

```

---

#### org.bepinex.plugins.farming.cfg

**Status**: Modified

**Summary**: ~7 changes

**Key Changes**:

**Total changes**: 7 (showing top 7)

• **2 - Crops.Grow Speed Factor**: `3` → `1.6` (-1.4)
• **2 - Crops.Show Progress Level**: `10` → `25` (+15)
• **2 - Crops.Harvest Increase Interval**: `10` → `15` (+5)
• **2 - Crops.Plant Increase Interval**: `10` → `15` (+5)
• **2 - Crops.Random Rotation**: `Off` → `On`
• **3 - Other.Skill Experience Gain Factor**: `1.25` → `0.57` (-0.68)
• **3 - Other.Skill Experience Loss**: `2` → `1` (-1)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| 2 - Crops.Grow Speed Factor | 3 | 1.6 | -1.4 |
| 2 - Crops.Harvest Increase Interval | 10 | 15 | +5 |
| 2 - Crops.Plant Increase Interval | 10 | 15 | +5 |
| 2 - Crops.Show Progress Level | 10 | 25 | +15 |
| 3 - Other.Skill Experience Gain Factor | 1.25 | 0.57 | -0.68 |
| 3 - Other.Skill Experience Loss | 2 | 1 | -1 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.farming.cfg+++ current/org.bepinex.plugins.farming.cfg@@ -1,3 +1,5 @@+##Changes made by Dogeheim: Changed growth speed factor to 1.6, Ignore Biome Level to 80, Skill Experience Gain Factor to 0.57
+
 ## Settings file was created by plugin Farming v2.2.1
 ## Plugin GUID: org.bepinex.plugins.farming
 
@@ -15,7 +17,7 @@ # Setting type: Single
 # Default value: 3
 # Acceptable value range: From 1 to 10
-Grow Speed Factor = 3
+Grow Speed Factor = 1.6
 
 ## Item yield factor for crops at skill level 100.
 # Setting type: Single
@@ -27,7 +29,7 @@ # Setting type: Int32
 # Default value: 30
 # Acceptable value range: From 0 to 100
-Show Progress Level = 10
+Show Progress Level = 25
 
 ## Required skill level to ignore the required biome of planted crops. 0 is disabled.
 # Setting type: Int32
@@ -39,13 +41,13 @@ # Setting type: Int32
 # Default value: 20
 # Acceptable value range: From 0 to 100
-Plant Increase Interval = 10
+Plant Increase Interval = 15
 
 ## Level interval to increase the radius harvested at the same time. 0 is disabled.
 # Setting type: Int32
 # Default value: 20
 # Acceptable value range: From 0 to 100
-Harvest Increase Interval = 10
+Harvest Increase Interval = 15
 
 ## Reduces the stamina usage while planting and harvesting your crops. Percentage stamina reduction per level. 0 is disabled.
 # Setting type: Int32
@@ -57,7 +59,7 @@ # Setting type: Toggle
 # Default value: Off
 # Acceptable values: Off, On
-Random Rotation = Off
+Random Rotation = On
 
 [3 - Other]
 
@@ -65,13 +67,13 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill Experience Gain Factor = 1.25
+Skill Experience Gain Factor = 0.57
 
 ## How much experience to lose in the farming skill on death.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Skill Experience Loss = 2
+Skill Experience Loss = 1
 
 ## Shortcut to press to toggle between the single plant mode and the mass plant mode. Please note that you have to stand still, to toggle this.
 # Setting type: KeyboardShortcut

```

---

#### org.bepinex.plugins.creaturelevelcontrol.cfg

**Status**: Modified

**Summary**: ~12 changes

**Key Changes**:

**Total changes**: 12 (showing top 8)

• **2 - Creatures.Base damage for creatures (percentage)**: `120` → `110` (-10)
• **2 - Creatures.Base health for creatures (percentage)**: `120` → `400` (+280)
• **2 - Creatures.Creature size increase per star (percentage)**: `10` → `14` (+4)
• **5 - Age of world.World level 1 start (days)**: `10` → `9999` (+9989)
• **5 - Age of world.World level 2 start (days)**: `25` → `9999` (+9974)
• **5 - Age of world.World level 3 start (days)**: `50` → `9999` (+9949)
• **5 - Age of world.World level 4 start (days)**: `100` → `9999` (+9899)
• **5 - Age of world.World level 5 start (days)**: `250` → `9999` (+9749)
• ... and 4 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| 2 - Creatures.Base damage for creatures (percentage) | 120 | 110 | -10 |
| 2 - Creatures.Base health for creatures (percentage) | 120 | 400 | +280 |
| 2 - Creatures.Creature size increase per star (percentage) | 10 | 14 | +4 |
| 5 - Age of world.World level 1 start (days) | 10 | 9999 | +9989 |
| 5 - Age of world.World level 2 start (days) | 25 | 9999 | +9974 |
| 5 - Age of world.World level 3 start (days) | 50 | 9999 | +9949 |
| 5 - Age of world.World level 4 start (days) | 100 | 9999 | +9899 |
| 5 - Age of world.World level 5 start (days) | 250 | 9999 | +9749 |
| 5 - Age of world.World level 6 start (days) | 500 | 9999 | +9499 |
| 5 - Age of world.World level 7 start (days) | 600 | 9999 | +9399 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.creaturelevelcontrol.cfg+++ current/org.bepinex.plugins.creaturelevelcontrol.cfg@@ -98,7 +98,7 @@ # Setting type: DifficultySecondFactor
 # Default value: BossesKilled
 # Acceptable values: None, Age_of_world, Distance, BossesKilled
-Second factor = Distance
+Second factor = BossesKilled
 
 ## Display circles on the map for distance from spawn option.
 # Setting type: Toggle
@@ -162,7 +162,7 @@ # Setting type: Int32
 # Default value: 10
 # Acceptable value range: From 0 to 40
-Creature size increase per star (percentage) = 10
+Creature size increase per star (percentage) = 14
 
 ## If creature size will be increased in dungeons as well, where they might get stuck if they get too big.
 # Setting type: Toggle
@@ -174,7 +174,7 @@ # Setting type: Single
 # Default value: 100
 # Acceptable value range: From 1 to 500
-Base health for creatures (percentage) = 120
+Base health for creatures (percentage) = 400
 
 ## Health gained per star for creatures in percentage.
 # Setting type: Single
@@ -186,7 +186,7 @@ # Setting type: Single
 # Default value: 100
 # Acceptable value range: From 1 to 500
-Base damage for creatures (percentage) = 120
+Base damage for creatures (percentage) = 110
 
 ## Damage gained per star for creatures in percentage.
 # Setting type: Single
@@ -280,7 +280,7 @@ # Setting type: Toggle
 # Default value: Off
 # Acceptable values: Off, On
-Creatures can drop multiple trophies = Off
+Creatures can drop multiple trophies = On
 
 ## If bosses can drop multiple trophies.
 # Setting type: Toggle
@@ -341,37 +341,37 @@ ## Days needed to pass before your world gets to world level 1.
 # Setting type: Int32
 # Default value: 10
-World level 1 start (days) = 10
+World level 1 start (days) = 9999
 
 ## Days needed to pass before your world gets to world level 2.
 # Setting type: Int32
 # Default value: 25
-World level 2 start (days) = 25
+World level 2 start (days) = 9999
 
 ## Days needed to pass before your world gets to world level 3.
 # Setting type: Int32
 # Default value: 50
-World level 3 start (days) = 50
+World level 3 start (days) = 9999
 
 ## Days needed to pass before your world gets to world level 4.
 # Setting type: Int32
 # Default value: 100
-World level 4 start (days) = 100
+World level 4 start (days) = 9999
 
 ## Days needed to pass before your world gets to world level 5.
 # Setting type: Int32
 # Default value: 250
-World level 5 start (days) = 250
+World level 5 start (days) = 9999
 
 ## Days needed to pass before your world gets to world level 6.
 # Setting type: Int32
 # Default value: 400
-World level 6 start (days) = 500
+World level 6 start (days) = 9999
 
 ## Days needed to pass before your world gets to world level 7.
 # Setting type: Int32
 # Default value: 600
-World level 7 start (days) = 600
+World level 7 start (days) = 9999
 
 [5 - Custom level chances]
 

```

---

#### org.bepinex.plugins.conversionsizespeed.cfg

**Status**: Modified

**Summary**: +18 changes

**Key Changes**:

**Total changes**: 18 (showing top 8)

• **Advanced cooking station.Conversion time**: `5` *(new setting)*
• **Bird House.Conversion time**: `20` *(new setting)*
• **Fish Trap.Conversion time**: `30` *(new setting)*
• **Fishing Dock.Conversion time**: `120` *(new setting)*
• **Primitive Compost.Conversion time**: `30` *(new setting)*
• **Bird House.Storage space**: `50` *(new setting)*
• **Bird House.Storage space increase per boss**: `0` *(new setting)*
• **Advanced cooking station.Fuel per product**: `1` *(new setting)*
• ... and 10 more changes

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.conversionsizespeed.cfg+++ current/org.bepinex.plugins.conversionsizespeed.cfg@@ -14,6 +14,44 @@ # Default value: LeftShift
 Fill up modifier key = LeftShift
 
+[Advanced cooking station]
+
+## Sets the maximum number of items that a Advanced cooking station can hold.
+# Setting type: Int32
+# Default value: 100
+# Acceptable value range: From 1 to 1000
+Storage space = 100
+
+## Increases the maximum number of items that a Advanced cooking station can hold for each boss killed.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Storage space increase per boss = 0
+
+## Sets the maximum number of fuel that a Advanced cooking station can hold.
+# Setting type: Int32
+# Default value: 100
+# Acceptable value range: From 1 to 1000
+Fuel space = 100
+
+## Increases the maximum number of fuel that a Advanced cooking station can hold for each boss killed.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Fuel space increase per boss = 0
+
+## Sets how much fuel a Advanced cooking station needs per produced product.
+# Setting type: Int32
+# Default value: 1
+# Acceptable value range: From 1 to 20
+Fuel per product = 1
+
+## Time in seconds that a Advanced cooking station needs for one conversion.
+# Setting type: Int32
+# Default value: 5
+# Acceptable value range: From 1 to 1000
+Conversion time = 5
+
 [Armory]
 
 ## Sets the maximum number of items that a Armory can hold.
@@ -72,6 +110,26 @@ # Acceptable value range: From 1 to 1000
 Conversion time = 20
 
+[Bird House]
+
+## Sets the maximum number of items that a Bird House can hold.
+# Setting type: Int32
+# Default value: 50
+# Acceptable value range: From 1 to 1000
+Storage space = 50
+
+## Increases the maximum number of items that a Bird House can hold for each boss killed.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Storage space increase per boss = 0
+
+## Time in seconds that a Bird House needs for one conversion.
+# Setting type: Int32
+# Default value: 20
+# Acceptable value range: From 1 to 1000
+Conversion time = 20
+
 [Blast Furnace]
 
 ## Sets the maximum number of items that a Blast Furnace can hold.
@@ -205,6 +263,46 @@ # Default value: 40
 # Acceptable value range: From 1 to 1000
 Conversion time = 20
+
+[Fish Trap]
+
+## Sets the maximum number of items that a Fish Trap can hold.
+# Setting type: Int32
+# Default value: 50
+# Acceptable value range: From 1 to 1000
+Storage space = 50
+
+## Increases the maximum number of items that a Fish Trap can hold for each boss killed.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Storage space increase per boss = 0
+
+## Time in seconds that a Fish Trap needs for one conversion.
+# Setting type: Int32
+# Default value: 30
+# Acceptable value range: From 1 to 1000
+Conversion time = 30
+
+[Fishing Dock]
+
+## Sets the maximum number of items that a Fishing Dock can hold.
+# Setting type: Int32
+# Default value: 100
+# Acceptable value range: From 1 to 1000
+Storage space = 100
+
+## Increases the maximum number of items that a Fishing Dock can hold for each boss killed.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Storage space increase per boss = 0
+
+## Time in seconds that a Fishing Dock needs for one conversion.
+# Setting type: Int32
+# Default value: 120
+# Acceptable value range: From 1 to 1000
+Conversion time = 120
 
 [Hot Tub]
 
@@ -225,6 +323,26 @@ # Default value: 5000
 # Acceptable value range: From 1 to 10000
 Conversion time = 5000
+
+[Primitive Compost]
+
+## Sets the maximum number of items that a Primitive Compost can hold.
+# Setting type: Int32
+# Default value: 50
+# Acceptable value range: From 1 to 1000
+Storage space = 50
+
+## Increases the maximum number of items that a Primitive Compost can hold for each boss killed.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Storage space increase per boss = 0
+
+## Time in seconds that a Primitive Compost needs for one conversion.
+# Setting type: Int32
+# Default value: 30
+# Acceptable value range: From 1 to 1000
+Conversion time = 30
 
 [Smelter]
 

```

---

#### org.bepinex.plugins.building.cfg

**Status**: Modified

**Summary**: ~6 changes

**Key Changes**:

**Total changes**: 6 (showing top 6)

• **2 - Building.Durability Increase Level Requirement**: `30` → `25` (-5)
• **2 - Building.Free Build Level Requirement**: `50` → `100` (+50)
• **2 - Building.Maximum Support Factor**: `1.5` → `1.8` (+0.3)
• **2 - Building.Support Loss Factor**: `0.75` → `0.85` (+0.1)
• **3 - Other.Skill Experience Gain Factor**: `0.5` → `0.8` (+0.3)
• **3 - Other.Skill Experience Loss**: `1` → `0` (-1)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| 2 - Building.Durability Increase Level Requirement | 30 | 25 | -5 |
| 2 - Building.Free Build Level Requirement | 50 | 100 | +50 |
| 2 - Building.Maximum Support Factor | 1.5 | 1.8 | +0.3 |
| 2 - Building.Support Loss Factor | 0.75 | 0.85 | +0.1 |
| 3 - Other.Skill Experience Gain Factor | 0.5 | 0.8 | +0.3 |
| 3 - Other.Skill Experience Loss | 1 | 0 | -1 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.building.cfg+++ current/org.bepinex.plugins.building.cfg@@ -15,13 +15,13 @@ # Setting type: Single
 # Default value: 1.5
 # Acceptable value range: From 1 to 5
-Maximum Support Factor = 1.5
+Maximum Support Factor = 1.8
 
 ## Support loss factor for vertical and horizontal building at skill level 100.
 # Setting type: Single
 # Default value: 0.75
 # Acceptable value range: From 0.01 to 1
-Support Loss Factor = 0.75
+Support Loss Factor = 0.85
 
 ## Health factor for building pieces at skill level 100.
 # Setting type: Single
@@ -33,13 +33,13 @@ # Setting type: Int32
 # Default value: 50
 # Acceptable value range: From 0 to 100
-Free Build Level Requirement = 50
+Free Build Level Requirement = 100
 
 ## Minimum required skill level to reduce the durability usage of hammers by 30%. 0 is disabled.
 # Setting type: Int32
 # Default value: 30
 # Acceptable value range: From 0 to 100
-Durability Increase Level Requirement = 30
+Durability Increase Level Requirement = 25
 
 ## Reduces the stamina usage while building. Percentage stamina reduction per level. 0 is disabled.
 # Setting type: Int32
@@ -53,11 +53,11 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill Experience Gain Factor = 0.5
+Skill Experience Gain Factor = 0.8
 
 ## How much experience to lose in the building skill on death.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Skill Experience Loss = 1
+Skill Experience Loss = 0
 

```

---

#### org.bepinex.plugins.blacksmithing.cfg

**Status**: Modified

**Summary**: ~9 changes

**Key Changes**:

**Total changes**: 9 (showing top 8)

• **2 - Crafting.Skill Level for Extra Upgrade Level**: `80` → `70` (-10)
• **2 - Crafting.Skill Level for Inventory Repair**: `70` → `50` (-20)
• **2 - Crafting.Base Durability Factor**: `1` → `2` (+1)
• **2 - Crafting.Durability Factor**: `2` → `4` (+2)
• **2 - Crafting.Experience Reduction Factor**: `0.5` → `0.25` (-0.25)
• **2 - Crafting.Experience Reduction Threshold**: `5` → `10` (+5)
• **2 - Crafting.First Craft Bonus**: `75` → `100` (+25)
• **3 - Other.Skill Experience Gain Factor**: `0.5` → `0.7` (+0.2)
• ... and 1 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| 2 - Crafting.Base Durability Factor | 1 | 2 | +1 |
| 2 - Crafting.Durability Factor | 2 | 4 | +2 |
| 2 - Crafting.Experience Reduction Factor | 0.5 | 0.25 | -0.25 |
| 2 - Crafting.Experience Reduction Threshold | 5 | 10 | +5 |
| 2 - Crafting.First Craft Bonus | 75 | 100 | +25 |
| 2 - Crafting.Skill Level for Extra Upgrade Level | 80 | 70 | -10 |
| 2 - Crafting.Skill Level for Inventory Repair | 70 | 50 | -20 |
| 3 - Other.Skill Experience Gain Factor | 0.5 | 0.7 | +0.2 |
| 3 - Other.Skill Experience Loss | 1 | 0 | -1 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.blacksmithing.cfg+++ current/org.bepinex.plugins.blacksmithing.cfg@@ -63,25 +63,25 @@ # Setting type: Int32
 # Default value: 70
 # Acceptable value range: From 0 to 100
-Skill Level for Inventory Repair = 70
+Skill Level for Inventory Repair = 50
 
 ## Minimum skill level for an additional upgrade level for armor and weapons. 0 means disabled.
 # Setting type: Int32
 # Default value: 80
 # Acceptable value range: From 0 to 100
-Skill Level for Extra Upgrade Level = 80
+Skill Level for Extra Upgrade Level = 70
 
 ## Factor for durability of armor and weapons at skill level 0.
 # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Base Durability Factor = 1
+Base Durability Factor = 2
 
 ## Factor for durability of armor and weapons at skill level 100.
 # Setting type: Single
 # Default value: 2
 # Acceptable value range: From 1 to 5
-Durability Factor = 2
+Durability Factor = 4
 
 ## Factor for the price of the additional upgrade.
 # Setting type: Single
@@ -93,19 +93,19 @@ # Setting type: Int32
 # Default value: 75
 # Acceptable value range: From 0 to 200
-First Craft Bonus = 75
+First Craft Bonus = 100
 
 ## After crafting an item this amount of times, crafting it will give reduced blacksmithing experience. Use 0 to disable this.
 # Setting type: Int32
 # Default value: 5
 # Acceptable value range: From 0 to 50
-Experience Reduction Threshold = 5
+Experience Reduction Threshold = 10
 
 ## Factor at which the blacksmithing experience gain is reduced, once too many of the same item have been crafted. Additive, not multiplicative. E.g. reducing the experience gained by 50% every 5 crafts means that you won't get any experience anymore after the 10th craft.
 # Setting type: Single
 # Default value: 0.5
 # Acceptable value range: From 0 to 1
-Experience Reduction Factor = 0.5
+Experience Reduction Factor = 0.25
 
 [3 - Other]
 
@@ -113,11 +113,11 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill Experience Gain Factor = 0.5
+Skill Experience Gain Factor = 0.7
 
 ## How much experience to lose in the blacksmithing skill on death.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Skill Experience Loss = 1
+Skill Experience Loss = 0
 

```

---

#### org.bepinex.plugins.ranching.cfg

**Status**: Modified

**Summary**: +7, -30 changes

**Key Changes**:

**Total changes**: 37 (showing top 8)

• **2 - Ranching.Calming Level Requirement**: `20` *(new setting)*
• **2 - Ranching.Food Level Requirement**: `10` *(new setting)*
• **2 - Ranching.Pregnancy Level Requirement**: `40` *(new setting)*
• **Explorers Backpack.Crafting Station Level**: `2` *(removed)*
• **Explorers Backpack.Maximum Crafting Station Level**: `6` *(removed)*
• **Explorers Backpack.Quality Multiplier**: `1` *(removed)*
• **2 - Backpack.Use External YAML**: `On` *(removed)*
• **2 - Backpack.Auto Fill Backpack**: `On` *(removed)*
• ... and 29 more changes

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.ranching.cfg+++ current/org.bepinex.plugins.ranching.cfg@@ -1,5 +1,5 @@-## Settings file was created by plugin Backpacks v1.3.6
-## Plugin GUID: org.bepinex.plugins.backpacks
+## Settings file was created by plugin Ranching v1.1.3
+## Plugin GUID: org.bepinex.plugins.ranching
 
 [1 - General]
 
@@ -9,179 +9,49 @@ # Acceptable values: Off, On
 Lock Configuration = On
 
-[2 - Backpack]
+[2 - Ranching]
 
-## If set to on, the YAML file from your config folder will be used, to implement custom Backpacks inside of that file.
-# Setting type: Toggle
-# Default value: Off
-# Acceptable values: Off, On
-Use External YAML = On
+## Item drop factor for tamed creatures at skill level 100.
+# Setting type: Single
+# Default value: 2
+# Acceptable value range: From 1 to 10
+Item Drop Factor = 2
 
-## Just ignore this.
+## Speed at which creatures get tame at skill level 100.
+# Setting type: Single
+# Default value: 2
+# Acceptable value range: From 1 to 10
+Taming Factor = 2
+
+## Minimum required skill level to see when tamed creatures will become hungry again. 0 is disabled.
+# Setting type: Int32
+# Default value: 10
+# Acceptable value range: From 0 to 100
+Food Level Requirement = 10
+
+## Minimum required skill level to calm nearby taming creatures. 0 is disabled.
+# Setting type: Int32
+# Default value: 20
+# Acceptable value range: From 0 to 100
+Calming Level Requirement = 20
+
+## Minimum required skill level to get pregnancy related information of tame creatures. 0 is disabled.
+# Setting type: Int32
+# Default value: 40
+# Acceptable value range: From 0 to 100
+Pregnancy Level Requirement = 40
+
+[3 - Other]
+
+## Factor for experience gained for the ranching skill.
+# Setting type: Single
+# Default value: 1
+# Acceptable value range: From 0.01 to 5
+Skill Experience Gain Factor = 0.6
+
+## How much experience to lose in the ranching skill on death.
 # Setting type: Int32
 # Default value: 0
-YAML Editor Anchor = 0
+# Acceptable value range: From 0 to 100
+Skill Experience Loss = 0
 
-## If on, pressing the interact key will not close the inventory.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Prevent Closing = On
-
-## Rows in a Backpack. One number for each upgrade level. Adding more numbers adds more upgrades. Changing this value does not affect existing Backpacks.
-# Setting type: String
-# Default value: 3, 3, 4, 4, 4
-Backpack Slot Rows = 3, 3, 4, 4, 4
-
-## Columns in a Backpack. One number for each upgrade level. Adding more numbers adds more upgrades. Changing this value does not affect existing Backpacks.
-# Setting type: String
-# Default value: 5, 6, 5, 6, 7
-Backpack Slot Columns = 5, 6, 5, 6, 7
-
-## Weight of items inside a Backpack.
-# Setting type: Int32
-# Default value: 100
-# Acceptable value range: From 0 to 100
-Backpack Weight = 100
-
-## If off, portals do not check the content of a backpack upon teleportation.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Backpack Teleportation Check = On
-
-## Allowed: Can put all backpacks into any other backpack.
-## Not Allowed: Cannot put any backpacks into another backpack.
-## Not Allowed Backpacks: Cannot put backpacks added by Backpacks into each other.
-## Not Allowed Same Backpack: Cannot put the same backpack type into each other.
-# Setting type: BackpackCeption
-# Default value: NotAllowed
-# Acceptable values: Allowed, NotAllowed, NotAllowedBackpacks, NotAllowedSameBackpack
-Backpacks in Backpacks = NotAllowed
-
-## If on, you can put backpacks that aren't empty into chests, to make the chests bigger on the inside.
-# Setting type: Toggle
-# Default value: Off
-# Acceptable values: Off, On
-Backpacks in Chests = Off
-
-## Can be used to restrict the number of backpacks a player can have in their inventory.
-## Global: Only one backpack.
-## Restricted: No other backpacks without item restrictions allowed.
-## Type: Only one backpack of each type.
-## Bypass: As many backpacks as you want.
-## None: Same as bypass, but doesn't overrule every other flag.
-# Setting type: Unique
-# Default value: Global
-# Acceptable values: None, Global, Restricted, Type, Bypass
-Unique Backpack = Global
-
-## If on, the backpack visual is hidden.
-# Setting type: Toggle
-# Default value: Off
-# Acceptable values: Off, On
-Hide Backpack = Off
-
-## If on, the backpack in your backpack slot is opened automatically, if the inventory is opened.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Auto Open Backpack = On
-
-## Name of a status effect that should be applied to the player, if the backpack is equipped.
-# Setting type: String
-# Default value: 
-Equip Status Effect = 
-
-## If on, items you pick up are added to your backpack. Conditions apply.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Auto Fill Backpack = On
-
-## If on, there is a dedicated slot for your backpack. Requires AzuExtendedPlayerInventory.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Backpack Slot = On
-
-[Explorers Backpack]
-
-## Crafting station where Explorers Backpack is available.
-# Setting type: CraftingTable
-# Default value: Workbench
-# Acceptable values: Disabled, Inventory, Workbench, Cauldron, Forge, ArtisanTable, StoneCutter, MageTable, BlackForge, FoodPreparationTable, MeadKetill, Custom
-Crafting Station = Disabled
-
-# Setting type: String
-# Default value: 
-Custom Crafting Station = 
-
-## Required crafting station level to craft Explorers Backpack.
-# Setting type: Int32
-# Default value: 2
-Crafting Station Level = 2
-
-## Maximum crafting station level to upgrade and repair Explorers Backpack.
-# Setting type: Int32
-# Default value: 6
-Maximum Crafting Station Level = 6
-
-## Whether only one of the ingredients is needed to craft Explorers Backpack
-# Setting type: Toggle
-# Default value: Off
-# Acceptable values: Off, On
-Require only one resource = Off
-
-## Multiplies the crafted amount based on the quality of the resources when crafting Explorers Backpack. Only works, if Require Only One Resource is true.
-# Setting type: Single
-# Default value: 1
-Quality Multiplier = 1
-
-## Item costs to craft Explorers Backpack
-# Setting type: String
-# Default value: BronzeNails:5,DeerHide:10,LeatherScraps:10
-Crafting Costs = BronzeNails:5,DeerHide:10,LeatherScraps:10
-
-## Item costs per level to upgrade Explorers Backpack
-# Setting type: String
-# Default value: Iron:5:2,ElderBark:10:2,Guck:2:2,Silver:5:3,WolfPelt:3:3,JuteRed:2:3,BlackMetal:5:4,LinenThread:10:4,LoxPelt:2:4,JuteBlue:5:5,ScaleHide:5:5,Carapace:5:5
-Upgrading Costs = Iron:5:2,ElderBark:10:2,Guck:2:2,Silver:5:3,WolfPelt:3:3,JuteRed:2:3,BlackMetal:5:4,LinenThread:10:4,LoxPelt:2:4,JuteBlue:5:5,ScaleHide:5:5,Carapace:5:5
-
-## Explorers Backpack drops from this creature.
-# Setting type: String
-# Default value: 
-Drops from = 
-
-## Weight of Explorers Backpack.
-# Setting type: Single
-# Default value: 4
-Weight = 4
-
-## Trader value of Explorers Backpack.
-# Setting type: Int32
-# Default value: 0
-Trader Value = 0
-
-## Which traders sell Explorers Backpack.
-# Setting type: Trader
-# Default value: None
-# Acceptable values: None, Haldor, Hildir
-# Multiple values can be set at the same time by separating them with , (e.g. Debug, Warning)
-Trader Selling = None
-
-## Price of Explorers Backpack at the trader.
-# Setting type: UInt32
-# Default value: 0
-Trader Price = 0
-
-## Stack size of Explorers Backpack in the trader. Also known as the number of items sold by a trader in one transaction.
-# Setting type: UInt32
-# Default value: 1
-Trader Stack = 1
-
-## Required global key to unlock Explorers Backpack at the trader.
-# Setting type: String
-# Default value: 
-Trader Required Global Key = 
-

```

---

#### org.bepinex.plugins.groups.cfg

**Status**: Modified

**Summary**: +12, -30 changes

**Key Changes**:

**Total changes**: 42 (showing top 8)

• **1 - General.Maximum size for groups**: `5` *(new setting)*
• **Explorers Backpack.Crafting Station Level**: `2` *(removed)*
• **Explorers Backpack.Maximum Crafting Station Level**: `6` *(removed)*
• **Explorers Backpack.Quality Multiplier**: `1` *(removed)*
• **2 - Backpack.Use External YAML**: `On` *(removed)*
• **2 - Display.Color of the group chat**: `00FF00FF` *(new setting)*
• **2 - Display.Group leader color**: `999933FF` *(new setting)*
• **2 - Display.Group leader display**: `Icon` *(new setting)*
• ... and 34 more changes

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.groups.cfg+++ current/org.bepinex.plugins.groups.cfg@@ -1,187 +1,80 @@-## Settings file was created by plugin Backpacks v1.3.6
-## Plugin GUID: org.bepinex.plugins.backpacks
+## Settings file was created by plugin Groups v1.2.9
+## Plugin GUID: org.bepinex.plugins.groups
 
 [1 - General]
 
-## If on, the configuration is locked and can be changed by server admins only.
+## If on, only server admins can change the configuration.
 # Setting type: Toggle
 # Default value: On
 # Acceptable values: Off, On
 Lock Configuration = On
 
-[2 - Backpack]
+## Maximum size for groups.
+# Setting type: Int32
+# Default value: 5
+# Acceptable value range: From 2 to 10
+Maximum size for groups = 5
 
-## If set to on, the YAML file from your config folder will be used, to implement custom Backpacks inside of that file.
+## If members of the same group can damage each other in PvP.
 # Setting type: Toggle
 # Default value: Off
 # Acceptable values: Off, On
-Use External YAML = On
+Friendly fire in groups = Off
 
-## Just ignore this.
-# Setting type: Int32
-# Default value: 0
-YAML Editor Anchor = 0
+[2 - Display]
 
-## If on, pressing the interact key will not close the inventory.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Prevent Closing = On
+## The color for messages in your group.
+# Setting type: Color
+# Default value: 00FF00FF
+Color of the group chat = 00FF00FF
 
-## Rows in a Backpack. One number for each upgrade level. Adding more numbers adds more upgrades. Changing this value does not affect existing Backpacks.
-# Setting type: String
-# Default value: 3, 3, 4, 4, 4
-Backpack Slot Rows = 3, 3, 4, 4, 4
+## The color for names of members of the own group, if you see them in the world.
+# Setting type: Color
+# Default value: 00FF00FF
+Name color for group members = 00FF00FF
 
-## Columns in a Backpack. One number for each upgrade level. Adding more numbers adds more upgrades. Changing this value does not affect existing Backpacks.
-# Setting type: String
-# Default value: 5, 6, 5, 6, 7
-Backpack Slot Columns = 5, 6, 5, 6, 7
+## Sets the anchor position of the group interface.
+# Setting type: Vector2
+# Default value: {"x":-875.0,"y":310.0}
+Position of the group interface = {"x":-875.0,"y":310.0}
 
-## Weight of items inside a Backpack.
-# Setting type: Int32
-# Default value: 100
-# Acceptable value range: From 0 to 100
-Backpack Weight = 100
-
-## If off, portals do not check the content of a backpack upon teleportation.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Backpack Teleportation Check = On
-
-## Allowed: Can put all backpacks into any other backpack.
-## Not Allowed: Cannot put any backpacks into another backpack.
-## Not Allowed Backpacks: Cannot put backpacks added by Backpacks into each other.
-## Not Allowed Same Backpack: Cannot put the same backpack type into each other.
-# Setting type: BackpackCeption
-# Default value: NotAllowed
-# Acceptable values: Allowed, NotAllowed, NotAllowedBackpacks, NotAllowedSameBackpack
-Backpacks in Backpacks = NotAllowed
-
-## If on, you can put backpacks that aren't empty into chests, to make the chests bigger on the inside.
+## Aligns the group interface horizontally, instead of vertically.
 # Setting type: Toggle
 # Default value: Off
 # Acceptable values: Off, On
-Backpacks in Chests = Off
+Horizontal group interface = Off
 
-## Can be used to restrict the number of backpacks a player can have in their inventory.
-## Global: Only one backpack.
-## Restricted: No other backpacks without item restrictions allowed.
-## Type: Only one backpack of each type.
-## Bypass: As many backpacks as you want.
-## None: Same as bypass, but doesn't overrule every other flag.
-# Setting type: Unique
-# Default value: Global
-# Acceptable values: None, Global, Restricted, Type, Bypass
-Unique Backpack = Global
+## How the leader of the group is displayed.
+# Setting type: GroupLeaderDisplayOption
+# Default value: Icon
+# Acceptable values: Disabled, Icon, Color
+Group leader display = Icon
 
-## If on, the backpack visual is hidden.
-# Setting type: Toggle
-# Default value: Off
-# Acceptable values: Off, On
-Hide Backpack = Off
+## Color of the group leader, if using the group leader color display option.
+# Setting type: Color
+# Default value: 999933FF
+Group leader color = 999933FF
 
-## If on, the backpack in your backpack slot is opened automatically, if the inventory is opened.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Auto Open Backpack = On
+## The space between group members in the group display.
+# Setting type: Single
+# Default value: 75
+Space between group members = 75
 
-## Name of a status effect that should be applied to the player, if the backpack is equipped.
+[3 - Other]
+
+## Modifier key that has to be pressed while pinging the map, to make the map ping visible to group members only.
+# Setting type: KeyboardShortcut
+# Default value: LeftAlt
+Group ping modifier key = LeftAlt
+
+## Ignore group invitations from people on this list. Comma separated.
 # Setting type: String
 # Default value: 
-Equip Status Effect = 
+Names of people who cannot invite you = 
 
-## If on, items you pick up are added to your backpack. Conditions apply.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Auto Fill Backpack = On
+## Can be used to block all invitations. Optionally, only block invitations while PvP is enabled.
+# Setting type: BlockInvitation
+# Default value: Never
+# Acceptable values: Never, Always, PvP, Enemy
+Block all invitations = Never
 
-## If on, there is a dedicated slot for your backpack. Requires AzuExtendedPlayerInventory.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Backpack Slot = On
-
-[Explorers Backpack]
-
-## Crafting station where Explorers Backpack is available.
-# Setting type: CraftingTable
-# Default value: Workbench
-# Acceptable values: Disabled, Inventory, Workbench, Cauldron, Forge, ArtisanTable, StoneCutter, MageTable, BlackForge, FoodPreparationTable, MeadKetill, Custom
-Crafting Station = Disabled
-
-# Setting type: String
-# Default value: 
-Custom Crafting Station = 
-
-## Required crafting station level to craft Explorers Backpack.
-# Setting type: Int32
-# Default value: 2
-Crafting Station Level = 2
-
-## Maximum crafting station level to upgrade and repair Explorers Backpack.
-# Setting type: Int32
-# Default value: 6
-Maximum Crafting Station Level = 6
-
-## Whether only one of the ingredients is needed to craft Explorers Backpack
-# Setting type: Toggle
-# Default value: Off
-# Acceptable values: Off, On
-Require only one resource = Off
-
-## Multiplies the crafted amount based on the quality of the resources when crafting Explorers Backpack. Only works, if Require Only One Resource is true.
-# Setting type: Single
-# Default value: 1
-Quality Multiplier = 1
-
-## Item costs to craft Explorers Backpack
-# Setting type: String
-# Default value: BronzeNails:5,DeerHide:10,LeatherScraps:10
-Crafting Costs = BronzeNails:5,DeerHide:10,LeatherScraps:10
-
-## Item costs per level to upgrade Explorers Backpack
-# Setting type: String
-# Default value: Iron:5:2,ElderBark:10:2,Guck:2:2,Silver:5:3,WolfPelt:3:3,JuteRed:2:3,BlackMetal:5:4,LinenThread:10:4,LoxPelt:2:4,JuteBlue:5:5,ScaleHide:5:5,Carapace:5:5
-Upgrading Costs = Iron:5:2,ElderBark:10:2,Guck:2:2,Silver:5:3,WolfPelt:3:3,JuteRed:2:3,BlackMetal:5:4,LinenThread:10:4,LoxPelt:2:4,JuteBlue:5:5,ScaleHide:5:5,Carapace:5:5
-
-## Explorers Backpack drops from this creature.
-# Setting type: String
-# Default value: 
-Drops from = 
-
-## Weight of Explorers Backpack.
-# Setting type: Single
-# Default value: 4
-Weight = 4
-
-## Trader value of Explorers Backpack.
-# Setting type: Int32
-# Default value: 0
-Trader Value = 0
-
-## Which traders sell Explorers Backpack.
-# Setting type: Trader
-# Default value: None
-# Acceptable values: None, Haldor, Hildir
-# Multiple values can be set at the same time by separating them with , (e.g. Debug, Warning)
-Trader Selling = None
-
-## Price of Explorers Backpack at the trader.
-# Setting type: UInt32
-# Default value: 0
-Trader Price = 0
-
-## Stack size of Explorers Backpack in the trader. Also known as the number of items sold by a trader in one transaction.
-# Setting type: UInt32
-# Default value: 1
-Trader Stack = 1
-
-## Required global key to unlock Explorers Backpack at the trader.
-# Setting type: String
-# Default value: 
-Trader Required Global Key = 
-

```

---

#### org.bepinex.plugins.exploration.cfg

**Status**: Modified

**Summary**: +9, -30 changes

**Key Changes**:

**Total changes**: 39 (showing top 8)

• **2 - Exploration.Cartography Read Level**: `40` *(new setting)*
• **2 - Exploration.Cartography Write Level**: `20` *(new setting)*
• **2 - Exploration.Exploration Radius Increase**: `250` *(new setting)*
• **2 - Exploration.Movement Speed Increase**: `15` *(new setting)*
• **2 - Exploration.Treasure Multiplication Chance**: `25` *(new setting)*
• **2 - Exploration.Treasure Multiplication Level**: `50` *(new setting)*
• **2 - Exploration.Wishbone Radius Increase**: `50` *(new setting)*
• **Explorers Backpack.Crafting Station Level**: `2` *(removed)*
• ... and 31 more changes

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.exploration.cfg+++ current/org.bepinex.plugins.exploration.cfg@@ -1,5 +1,5 @@-## Settings file was created by plugin Backpacks v1.3.6
-## Plugin GUID: org.bepinex.plugins.backpacks
+## Settings file was created by plugin Exploration v1.0.3
+## Plugin GUID: org.bepinex.plugins.exploration
 
 [1 - General]
 
@@ -9,179 +9,61 @@ # Acceptable values: Off, On
 Lock Configuration = On
 
-[2 - Backpack]
+[2 - Exploration]
 
-## If set to on, the YAML file from your config folder will be used, to implement custom Backpacks inside of that file.
-# Setting type: Toggle
-# Default value: Off
-# Acceptable values: Off, On
-Use External YAML = On
+## Exploration radius increase at skill level 100.
+# Setting type: Int32
+# Default value: 250
+# Acceptable value range: From 0 to 1000
+Exploration Radius Increase = 250
 
-## Just ignore this.
+## Movement speed increase at skill level 100.
+# Setting type: Int32
+# Default value: 15
+# Acceptable value range: From 0 to 30
+Movement Speed Increase = 15
+
+## Wishbone radius increase at skill level 100.
+# Setting type: Int32
+# Default value: 50
+# Acceptable value range: From 0 to 100
+Wishbone Radius Increase = 50
+
+## Exploration skill level required to write your map to the cartography table. Set to 0 to disable the requirement.
+# Setting type: Int32
+# Default value: 20
+# Acceptable value range: From 0 to 100
+Cartography Write Level = 20
+
+## Exploration skill level required to read the map from the cartography table. Set to 0 to disable the requirement.
+# Setting type: Int32
+# Default value: 40
+# Acceptable value range: From 0 to 100
+Cartography Read Level = 40
+
+## Exploration skill level required to have a chance to multiply the content of treasure chests. Set to 0 to disable this.
+# Setting type: Int32
+# Default value: 50
+# Acceptable value range: From 0 to 100
+Treasure Multiplication Level = 50
+
+## Chance to multiply the content of treasure chests, if the required skill level is reached.
+# Setting type: Int32
+# Default value: 25
+# Acceptable value range: From 0 to 100
+Treasure Multiplication Chance = 25
+
+[3 - Other]
+
+## Factor for experience gained for the exploration skill.
+# Setting type: Single
+# Default value: 1
+# Acceptable value range: From 0.01 to 5
+Skill Experience Gain Factor = 0.48
+
+## How much experience to lose in the exploration skill on death.
 # Setting type: Int32
 # Default value: 0
-YAML Editor Anchor = 0
+# Acceptable value range: From 0 to 100
+Skill Experience Loss = 0
 
-## If on, pressing the interact key will not close the inventory.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Prevent Closing = On
-
-## Rows in a Backpack. One number for each upgrade level. Adding more numbers adds more upgrades. Changing this value does not affect existing Backpacks.
-# Setting type: String
-# Default value: 3, 3, 4, 4, 4
-Backpack Slot Rows = 3, 3, 4, 4, 4
-
-## Columns in a Backpack. One number for each upgrade level. Adding more numbers adds more upgrades. Changing this value does not affect existing Backpacks.
-# Setting type: String
-# Default value: 5, 6, 5, 6, 7
-Backpack Slot Columns = 5, 6, 5, 6, 7
-
-## Weight of items inside a Backpack.
-# Setting type: Int32
-# Default value: 100
-# Acceptable value range: From 0 to 100
-Backpack Weight = 100
-
-## If off, portals do not check the content of a backpack upon teleportation.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Backpack Teleportation Check = On
-
-## Allowed: Can put all backpacks into any other backpack.
-## Not Allowed: Cannot put any backpacks into another backpack.
-## Not Allowed Backpacks: Cannot put backpacks added by Backpacks into each other.
-## Not Allowed Same Backpack: Cannot put the same backpack type into each other.
-# Setting type: BackpackCeption
-# Default value: NotAllowed
-# Acceptable values: Allowed, NotAllowed, NotAllowedBackpacks, NotAllowedSameBackpack
-Backpacks in Backpacks = NotAllowed
-
-## If on, you can put backpacks that aren't empty into chests, to make the chests bigger on the inside.
-# Setting type: Toggle
-# Default value: Off
-# Acceptable values: Off, On
-Backpacks in Chests = Off
-
-## Can be used to restrict the number of backpacks a player can have in their inventory.
-## Global: Only one backpack.
-## Restricted: No other backpacks without item restrictions allowed.
-## Type: Only one backpack of each type.
-## Bypass: As many backpacks as you want.
-## None: Same as bypass, but doesn't overrule every other flag.
-# Setting type: Unique
-# Default value: Global
-# Acceptable values: None, Global, Restricted, Type, Bypass
-Unique Backpack = Global
-
-## If on, the backpack visual is hidden.
-# Setting type: Toggle
-# Default value: Off
-# Acceptable values: Off, On
-Hide Backpack = Off
-
-## If on, the backpack in your backpack slot is opened automatically, if the inventory is opened.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Auto Open Backpack = On
-
-## Name of a status effect that should be applied to the player, if the backpack is equipped.
-# Setting type: String
-# Default value: 
-Equip Status Effect = 
-
-## If on, items you pick up are added to your backpack. Conditions apply.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Auto Fill Backpack = On
-
-## If on, there is a dedicated slot for your backpack. Requires AzuExtendedPlayerInventory.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Backpack Slot = On
-
-[Explorers Backpack]
-
-## Crafting station where Explorers Backpack is available.
-# Setting type: CraftingTable
-# Default value: Workbench
-# Acceptable values: Disabled, Inventory, Workbench, Cauldron, Forge, ArtisanTable, StoneCutter, MageTable, BlackForge, FoodPreparationTable, MeadKetill, Custom
-Crafting Station = Disabled
-
-# Setting type: String
-# Default value: 
-Custom Crafting Station = 
-
-## Required crafting station level to craft Explorers Backpack.
-# Setting type: Int32
-# Default value: 2
-Crafting Station Level = 2
-
-## Maximum crafting station level to upgrade and repair Explorers Backpack.
-# Setting type: Int32
-# Default value: 6
-Maximum Crafting Station Level = 6
-
-## Whether only one of the ingredients is needed to craft Explorers Backpack
-# Setting type: Toggle
-# Default value: Off
-# Acceptable values: Off, On
-Require only one resource = Off
-
-## Multiplies the crafted amount based on the quality of the resources when crafting Explorers Backpack. Only works, if Require Only One Resource is true.
-# Setting type: Single
-# Default value: 1
-Quality Multiplier = 1
-
-## Item costs to craft Explorers Backpack
-# Setting type: String
-# Default value: BronzeNails:5,DeerHide:10,LeatherScraps:10
-Crafting Costs = BronzeNails:5,DeerHide:10,LeatherScraps:10
-
-## Item costs per level to upgrade Explorers Backpack
-# Setting type: String
-# Default value: Iron:5:2,ElderBark:10:2,Guck:2:2,Silver:5:3,WolfPelt:3:3,JuteRed:2:3,BlackMetal:5:4,LinenThread:10:4,LoxPelt:2:4,JuteBlue:5:5,ScaleHide:5:5,Carapace:5:5
-Upgrading Costs = Iron:5:2,ElderBark:10:2,Guck:2:2,Silver:5:3,WolfPelt:3:3,JuteRed:2:3,BlackMetal:5:4,LinenThread:10:4,LoxPelt:2:4,JuteBlue:5:5,ScaleHide:5:5,Carapace:5:5
-
-## Explorers Backpack drops from this creature.
-# Setting type: String
-# Default value: 
-Drops from = 
-
-## Weight of Explorers Backpack.
-# Setting type: Single
-# Default value: 4
-Weight = 4
-
-## Trader value of Explorers Backpack.
-# Setting type: Int32
-# Default value: 0
-Trader Value = 0
-
-## Which traders sell Explorers Backpack.
-# Setting type: Trader
-# Default value: None
-# Acceptable values: None, Haldor, Hildir
-# Multiple values can be set at the same time by separating them with , (e.g. Debug, Warning)
-Trader Selling = None
-
-## Price of Explorers Backpack at the trader.
-# Setting type: UInt32
-# Default value: 0
-Trader Price = 0
-
-## Stack size of Explorers Backpack in the trader. Also known as the number of items sold by a trader in one transaction.
-# Setting type: UInt32
-# Default value: 1
-Trader Stack = 1
-
-## Required global key to unlock Explorers Backpack at the trader.
-# Setting type: String
-# Default value: 
-Trader Required Global Key = 
-

```

---

#### org.bepinex.plugins.cooking.cfg

**Status**: Modified

**Summary**: +13, -30 changes

**Key Changes**:

**Total changes**: 43 (showing top 8)

• **2 - Cooking.Bonus Crafting Amount**: `1` *(new setting)*
• **2 - Cooking.Bonus Crafting Chance**: `0` *(new setting)*
• **2 - Cooking.Crafting Time Reduction**: `30` *(new setting)*
• **2 - Cooking.Health Increase Factor**: `1.3` *(new setting)*
• **3 - Happy.Happy Required Level**: `50` *(new setting)*
• **Explorers Backpack.Crafting Station Level**: `2` *(removed)*
• **Explorers Backpack.Maximum Crafting Station Level**: `6` *(removed)*
• **Explorers Backpack.Quality Multiplier**: `1` *(removed)*
• ... and 35 more changes

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.cooking.cfg+++ current/org.bepinex.plugins.cooking.cfg@@ -1,5 +1,5 @@-## Settings file was created by plugin Backpacks v1.3.6
-## Plugin GUID: org.bepinex.plugins.backpacks
+## Settings file was created by plugin Cooking v1.2.1
+## Plugin GUID: org.bepinex.plugins.cooking
 
 [1 - General]
 
@@ -9,179 +9,87 @@ # Acceptable values: Off, On
 Lock Configuration = On
 
-[2 - Backpack]
+[2 - Cooking]
 
-## If set to on, the YAML file from your config folder will be used, to implement custom Backpacks inside of that file.
-# Setting type: Toggle
-# Default value: Off
-# Acceptable values: Off, On
-Use External YAML = On
+## Factor for the health on food items at skill level 100.
+# Setting type: Single
+# Default value: 1.3
+# Acceptable value range: From 1 to 5
+Health Increase Factor = 1.3
 
-## Just ignore this.
+## Factor for the stamina on food items at skill level 100.
+# Setting type: Single
+# Default value: 1.3
+# Acceptable value range: From 1 to 5
+Stamina Increase Factor = 1.3
+
+## Factor for the health regeneration on food items at skill level 100.
+# Setting type: Single
+# Default value: 1.3
+# Acceptable value range: From 1 to 5
+Regen Increase Factor = 1.3
+
+## Factor for the eitr on food items at skill level 100.
+# Setting type: Single
+# Default value: 1.3
+# Acceptable value range: From 1 to 5
+Eitr Increase Factor = 1.3
+
+## Chance to craft additional food items at skill level 100. Vanilla uses 25%.
 # Setting type: Int32
 # Default value: 0
-YAML Editor Anchor = 0
+# Acceptable value range: From 0 to 100
+Bonus Crafting Chance = 0
 
-## If on, pressing the interact key will not close the inventory.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Prevent Closing = On
+## Additional items to be crafted when the bonus crafting chance triggers.
+# Setting type: Int32
+# Default value: 1
+# Acceptable value range: From 1 to 10
+Bonus Crafting Amount = 1
 
-## Rows in a Backpack. One number for each upgrade level. Adding more numbers adds more upgrades. Changing this value does not affect existing Backpacks.
-# Setting type: String
-# Default value: 3, 3, 4, 4, 4
-Backpack Slot Rows = 3, 3, 4, 4, 4
+## Time reduction to craft food items at skill level 100. Vanilla uses 60%.
+# Setting type: Int32
+# Default value: 30
+# Acceptable value range: From 0 to 100
+Crafting Time Reduction = 30
 
-## Columns in a Backpack. One number for each upgrade level. Adding more numbers adds more upgrades. Changing this value does not affect existing Backpacks.
-# Setting type: String
-# Default value: 5, 6, 5, 6, 7
-Backpack Slot Columns = 5, 6, 5, 6, 7
+## Cooking skill level difference needed before food stops stacking with each other.
+# Setting type: Int32
+# Default value: 5
+# Acceptable value range: From 1 to 50
+Cooking Skill Interval = 5
 
-## Weight of items inside a Backpack.
+[3 - Happy]
+
+## Minimum required cooking skill level for a chance to cook perfect food. 0 is disabled
 # Setting type: Int32
-# Default value: 100
+# Default value: 50
 # Acceptable value range: From 0 to 100
-Backpack Weight = 100
+Happy Required Level = 50
 
-## If off, portals do not check the content of a backpack upon teleportation.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Backpack Teleportation Check = On
+## Duration for the happy buff from eating perfectly cooked food in minutes.
+# Setting type: Int32
+# Default value: 3
+# Acceptable value range: From 1 to 60
+Happy Buff Duration = 3
 
-## Allowed: Can put all backpacks into any other backpack.
-## Not Allowed: Cannot put any backpacks into another backpack.
-## Not Allowed Backpacks: Cannot put backpacks added by Backpacks into each other.
-## Not Allowed Same Backpack: Cannot put the same backpack type into each other.
-# Setting type: BackpackCeption
-# Default value: NotAllowed
-# Acceptable values: Allowed, NotAllowed, NotAllowedBackpacks, NotAllowedSameBackpack
-Backpacks in Backpacks = NotAllowed
+## Factor for the movement speed with the happy buff active.
+# Setting type: Single
+# Default value: 1.1
+# Acceptable value range: From 1 to 3
+Happy Buff Strength = 1.1
 
-## If on, you can put backpacks that aren't empty into chests, to make the chests bigger on the inside.
-# Setting type: Toggle
-# Default value: Off
-# Acceptable values: Off, On
-Backpacks in Chests = Off
+[4 - Other]
 
-## Can be used to restrict the number of backpacks a player can have in their inventory.
-## Global: Only one backpack.
-## Restricted: No other backpacks without item restrictions allowed.
-## Type: Only one backpack of each type.
-## Bypass: As many backpacks as you want.
-## None: Same as bypass, but doesn't overrule every other flag.
-# Setting type: Unique
-# Default value: Global
-# Acceptable values: None, Global, Restricted, Type, Bypass
-Unique Backpack = Global
-
-## If on, the backpack visual is hidden.
-# Setting type: Toggle
-# Default value: Off
-# Acceptable values: Off, On
-Hide Backpack = Off
-
-## If on, the backpack in your backpack slot is opened automatically, if the inventory is opened.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Auto Open Backpack = On
-
-## Name of a status effect that should be applied to the player, if the backpack is equipped.
-# Setting type: String
-# Default value: 
-Equip Status Effect = 
-
-## If on, items you pick up are added to your backpack. Conditions apply.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Auto Fill Backpack = On
-
-## If on, there is a dedicated slot for your backpack. Requires AzuExtendedPlayerInventory.
-# Setting type: Toggle
-# Default value: On
-# Acceptable values: Off, On
-Backpack Slot = On
-
-[Explorers Backpack]
-
-## Crafting station where Explorers Backpack is available.
-# Setting type: CraftingTable
-# Default value: Workbench
-# Acceptable values: Disabled, Inventory, Workbench, Cauldron, Forge, ArtisanTable, StoneCutter, MageTable, BlackForge, FoodPreparationTable, MeadKetill, Custom
-Crafting Station = Disabled
-
-# Setting type: String
-# Default value: 
-Custom Crafting Station = 
-
-## Required crafting station level to craft Explorers Backpack.
-# Setting type: Int32
-# Default value: 2
-Crafting Station Level = 2
-
-## Maximum crafting station level to upgrade and repair Explorers Backpack.
-# Setting type: Int32
-# Default value: 6
-Maximum Crafting Station Level = 6
-
-## Whether only one of the ingredients is needed to craft Explorers Backpack
-# Setting type: Toggle
-# Default value: Off
-# Acceptable values: Off, On
-Require only one resource = Off
-
-## Multiplies the crafted amount based on the quality of the resources when crafting Explorers Backpack. Only works, if Require Only One Resource is true.
+## Factor for experience gained for the cooking skill.
 # Setting type: Single
 # Default value: 1
-Quality Multiplier = 1
+# Acceptable value range: From 0.01 to 5
+Skill Experience Gain Factor = 0.6
 
-## Item costs to craft Explorers Backpack
-# Setting type: String
-# Default value: BronzeNails:5,DeerHide:10,LeatherScraps:10
-Crafting Costs = BronzeNails:5,DeerHide:10,LeatherScraps:10
-
-## Item costs per level to upgrade Explorers Backpack
-# Setting type: String
-# Default value: Iron:5:2,ElderBark:10:2,Guck:2:2,Silver:5:3,WolfPelt:3:3,JuteRed:2:3,BlackMetal:5:4,LinenThread:10:4,LoxPelt:2:4,JuteBlue:5:5,ScaleHide:5:5,Carapace:5:5
-Upgrading Costs = Iron:5:2,ElderBark:10:2,Guck:2:2,Silver:5:3,WolfPelt:3:3,JuteRed:2:3,BlackMetal:5:4,LinenThread:10:4,LoxPelt:2:4,JuteBlue:5:5,ScaleHide:5:5,Carapace:5:5
-
-## Explorers Backpack drops from this creature.
-# Setting type: String
-# Default value: 
-Drops from = 
-
-## Weight of Explorers Backpack.
-# Setting type: Single
-# Default value: 4
-Weight = 4
-
-## Trader value of Explorers Backpack.
+## How much experience to lose in the cooking skill on death.
 # Setting type: Int32
 # Default value: 0
-Trader Value = 0
+# Acceptable value range: From 0 to 100
+Skill Experience Loss = 0
 
-## Which traders sell Explorers Backpack.
-# Setting type: Trader
-# Default value: None
-# Acceptable values: None, Haldor, Hildir
-# Multiple values can be set at the same time by separating them with , (e.g. Debug, Warning)
-Trader Selling = None
-
-## Price of Explorers Backpack at the trader.
-# Setting type: UInt32
-# Default value: 0
-Trader Price = 0
-
-## Stack size of Explorers Backpack in the trader. Also known as the number of items sold by a trader in one transaction.
-# Setting type: UInt32
-# Default value: 1
-Trader Stack = 1
-
-## Required global key to unlock Explorers Backpack at the trader.
-# Setting type: String
-# Default value: 
-Trader Required Global Key = 
-

```

---


### Spawn That

*Files in this category with changes from RelicHeim backup:*

#### spawn_that.cfg

**Status**: Modified

**Summary**: +19, -292 changes

**Key Changes**:

**Total changes**: 311 (showing top 8)

• **WorldSpawner.32000.GroupRadius**: `5` *(removed)*
• **WorldSpawner.32000.GroupSizeMax**: `1` *(removed)*
• **WorldSpawner.32000.GroupSizeMin**: `1` *(removed)*
• **WorldSpawner.32000.LevelUpMinCenterDistance**: `0` *(removed)*
• **WorldSpawner.32000.SpawnChance**: `10` *(removed)*
• **WorldSpawner.32000.SpawnDistance**: `64` *(removed)*
• **WorldSpawner.32000.SpawnRadiusMax**: `0` *(removed)*
• **WorldSpawner.32000.SpawnRadiusMin**: `0` *(removed)*
• ... and 303 more changes

**Full Diff**:

```diff
--- backup/spawn_that.cfg+++ current/spawn_that.cfg@@ -1,321 +1,109 @@-###################
-# Index: 32000+ Extra_Spawns
-###################
+[Datamining]
 
-[WorldSpawner.32000]
-Name=RancidRemains
-Enabled=True
-Biomes=BlackForest
-PrefabName=Skeleton_Poison
-HuntPlayer=False
-MaxSpawned=2
-SpawnInterval=600
-SpawnChance=10
-LevelUpMinCenterDistance=0
-SpawnDistance=64
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=1
-GroupRadius=5
-GroundOffset=0.5
-SpawnDuringDay=False
-SpawnDuringNight=True
-ConditionAltitudeMin=0.1
-ConditionAltitudeMax=1000
-ConditionLocation=Crypt2, Crypt3, Crypt4
-SetTryDespawnOnConditionsInvalid=true
-SetFaction=Boss
+## Writes all locations loaded to a file, sectioned by the biome in which they can appear.
+# Setting type: Boolean
+# Default value: false
+WriteLocationsToFile = false
 
-[WorldSpawner.32001]
-Name=
-Enabled=True
-Biomes=BlackForest
-PrefabName=Troll
-HuntPlayer=False
-MaxSpawned=1
-SpawnInterval=300
-SpawnChance=15
-SpawnDistance=64
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=1
-GroupRadius=3
-GroundOffset=0.5
-SpawnDuringDay=False
-SpawnDuringNight=True
-ConditionAltitudeMin=0
-ConditionAltitudeMax=1000
-ConditionTiltMin=0
-ConditionTiltMax=35
-SpawnInForest=True
-SpawnOutsideForest=True
-ConditionDistanceToCenterMin=1000
-SetTryDespawnOnConditionsInvalid=true
-SetFaction=Boss
+[Debug]
 
-[WorldSpawner.32002]
-Name=
-Enabled=True
-Biomes=Ocean
-PrefabName=HelWraith_TW
-HuntPlayer=False
-MaxSpawned=1
-SpawnInterval=200
-SpawnChance=5
-SpawnDistance=100
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey= defeated_bonemass
-RequiredEnvironments= Misty
-GroupSizeMin=1
-GroupSizeMax=1
-GroupRadius=10
-GroundOffset=35
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin= -30
-ConditionAltitudeMax= 1000
-ConditionDistanceToCenterMin=2000
-SetTryDespawnOnConditionsInvalid=true
-SetFaction=Boss
+## Enable debug logging.
+# Setting type: Boolean
+# Default value: false
+DebugLoggingOn = false
 
-[WorldSpawner.32003]
-Name=
-Enabled=True
-Biomes=Ocean
-PrefabName=Hatchling
-HuntPlayer=False
-MaxSpawned=1
-SpawnInterval=200
-SpawnChance=5
-SpawnDistance=100
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey= defeated_dragon
-RequiredEnvironments= Rain
-GroupSizeMin=1
-GroupSizeMax=1
-GroupRadius=10
-GroundOffset=35
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin= -30
-ConditionAltitudeMax= 1000
-ConditionDistanceToCenterMin=2000
-SetTryDespawnOnConditionsInvalid=true
-SetFaction=Boss
+## Enables in-depth logging. Note, this might generate a LOT of log entries.
+# Setting type: Boolean
+# Default value: false
+TraceLoggingOn = false
 
-[WorldSpawner.32004]
-Name=
-Enabled=True
-Biomes=Ocean
-PrefabName=Deathsquito
-HuntPlayer=False
-MaxSpawned=2
-SpawnInterval=200
-SpawnChance=5
-SpawnDistance=100
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey= defeated_goblinking
-RequiredEnvironments= Clear
-GroupSizeMin=2
-GroupSizeMax=2
-GroupRadius=10
-GroundOffset=30
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin= -30
-ConditionAltitudeMax= 1000
-ConditionDistanceToCenterMin=2000
-SetTryDespawnOnConditionsInvalid=true
-SetFaction=Boss
+## Prints a set of pngs showing the area id's assigned by Spawn That to each biome 'area'. Each pixel's hex value corresponds to an area id, when converted into a decimal.
+# Setting type: Boolean
+# Default value: false
+PrintAreaMap = false
 
-[WorldSpawner.32005]
-Name=
-Enabled=True
-Biomes=Plains,
-PrefabName=GoblinBrute
-HuntPlayer=False
-MaxSpawned=2
-SpawnInterval=300
-SpawnChance=10
-LevelUpMinCenterDistance=0
-SpawnDistance=30
-SpawnRadiusMin=10
-SpawnRadiusMax=20
-RequiredGlobalKey=
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=2
-GroupRadius=3
-GroundOffset=0.5
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin=0
-ConditionAltitudeMax=1000
-ConditionTiltMin=0
-ConditionTiltMax=35
-SpawnInForest=True
-SpawnOutsideForest=True
-ConditionLocation=StoneTower1
-DistanceToTriggerPlayerConditions=5
-SetFaction=Boss
+## Prints a map of the biome of each zone.
+# Setting type: Boolean
+# Default value: false
+PrintBiomeMap = false
 
-[WorldSpawner.32006]
-Name=
-Enabled=True
-Biomes=Meadows,
-PrefabName=Fox_TW
-HuntPlayer=False
-MaxSpawned=4
-SpawnInterval=300
-SpawnChance=10
-LevelUpMinCenterDistance=0
-SpawnDistance=64
-SpawnRadiusMin=10
-SpawnRadiusMax=20
-RequiredGlobalKey=
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=2
-GroupRadius=3
-GroundOffset=0.5
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin=0
-ConditionAltitudeMax=1000
-ConditionTiltMin=0
-ConditionTiltMax=35
-SpawnInForest=True
-SpawnOutsideForest=True
-ConditionLocation=Runestone_Meadows, StoneCircle
-DistanceToTriggerPlayerConditions=5
-SetFaction=ForestMonsters
+## Prints maps marking where each configured world spawn template can spawn. This will be done for every config entry.
+# Setting type: Boolean
+# Default value: false
+PrintFantasticBeastsAndWhereToKillThem = false
 
-[WorldSpawner.32007]
-Name=Shark
-Enabled=True
-Biomes=Ocean
-PrefabName=Shark_TW
-HuntPlayer=False
-MaxSpawned=1
-SpawnInterval=500
-SpawnChance=10
-SpawnDistance=50
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=1
-GroupRadius=3
-GroundOffset=0.5
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin=-1000
-ConditionAltitudeMax=-5
-ConditionTiltMin=0
-ConditionTiltMax=35
-SpawnInForest=True
-SpawnOutsideForest=True
-OceanDepthMin=0
-OceanDepthMax=0
-BiomeArea=Median
-ConditionDistanceToCenterMin=3000
-SetFaction=Boss
+## Folder path to write to. Root folder is BepInEx.
+# Setting type: String
+# Default value: Debug
+DebugFileFolder = Debug
 
-[WorldSpawner.32008]
-Name=Morgen [Sleeping]
-Enabled=True
-Biomes=AshLands
-PrefabName=Morgen
-HuntPlayer=False
-MaxSpawned=2
-SpawnInterval=2000
-SpawnChance=5
-LevelUpChance=-1
-LevelUpMinCenterDistance=0
-SpawnDistance=60
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=1
-GroupRadius=3
-GroundOffset=0
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin=0
-ConditionAltitudeMax=1000
-ConditionTiltMin=0
-ConditionTiltMax=35
-SpawnInForest=True
-SpawnOutsideForest=True
-OceanDepthMin=0
-OceanDepthMax=0
-BiomeArea=Everything
-ConditionPositionMustNotBeNearPrefabs=Morgen_NonSleeping
+[LocalSpawner]
 
-###################
-# Index: 32100+ Pickables
-###################
+## Writes local spawners to a file before applying configuration changes.
+# Setting type: Boolean
+# Default value: false
+WriteSpawnTablesToFileBeforeChanges = false
 
-[WorldSpawner.32100]
-Name=Pickable_SeedOnion
-Enabled=True
-Biomes=Mountain
-PrefabName=Pickable_SeedOnion
-HuntPlayer=False
-MaxSpawned=1
-SpawnInterval=600
-SpawnChance=10
-SpawnDistance=64
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=defeated_bonemass
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=2
-GroupRadius=2
-GroundOffset=0.1
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin=120
-ConditionAltitudeMax=1000
-SpawnInForest=True
-SpawnOutsideForest=True
-ConditionPositionMustNotBeNearPrefabs=Pickable_SeedOnion
+## If true, locations with multiple spawners with duplicate creatures will be listed individually, instead of being only one of each creature.
+# Setting type: Boolean
+# Default value: false
+DontCollapseFile = false
 
-[WorldSpawner.32101]
-Name=TurnipSeeds
-Enabled=True
-Biomes=Swamp
-PrefabName=Pickable_SeedTurnip
-HuntPlayer=False
-MaxSpawned=1
-SpawnInterval=600
-SpawnChance=10
-SpawnDistance=120
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=defeated_gdking
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=2
-GroupRadius=2
-GroundOffset=0.1
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin=0
-ConditionAltitudeMax=1000
-SpawnInForest=True
-SpawnOutsideForest=True
-ConditionPositionMustNotBeNearPrefabs=Pickable_SeedTurnip+## Toggles if Spawn That changes to local spawners will be run or not.
+# Setting type: Boolean
+# Default value: true
+Enable = true
+
+[Simple]
+
+## If true, fills in simple cfg with a list of creatures when file is created.
+# Setting type: Boolean
+# Default value: true
+InitializeWithCreatures = true
+
+[SpawnAreaSpawner]
+
+## Writes SpawnArea spawners to a file before applying configuration changes.
+# Setting type: Boolean
+# Default value: false
+WriteSpawnTablesToFileBeforeChanges = false
+
+## Writes SpawnArea spawner configs loaded in Spawn That to file, before applying to spawners in game.
+## These are the configs loaded from files and set by other mods, after being merged and prepared internally in Spawn That.
+# Setting type: Boolean
+# Default value: false
+WriteConfigsToFile = false
+
+[WorldSpawner]
+
+## If true, removes all existing world spawner templates.
+# Setting type: Boolean
+# Default value: false
+ClearAllExisting = false
+
+## If true, will never override existing spawners, but add all custom configurations to the list.
+# Setting type: Boolean
+# Default value: false
+AlwaysAppend = false
+
+## Global spawn rate multiplier.
+# Setting type: Single
+# Default value: 0.7
+WorldSpawnRate = 0.7
+
+## Writes world spawner templates to a file, before applying custom changes.
+# Setting type: Boolean
+# Default value: false
+WriteSpawnTablesToFileBeforeChanges = false
+
+## Writes world spawner templates to a file after applying configuration changes.
+# Setting type: Boolean
+# Default value: false
+WriteSpawnTablesToFileAfterChanges = false
+
+## Writes world spawner configs loaded in Spawn That to file, before applying to spawners in game.
+## These are the configs loaded from files and set by other mods, after being merged and prepared internally in Spawn That.
+# Setting type: Boolean
+# Default value: false
+WriteConfigsToFile = false
+

```

---

#### spawn_that.world_spawners_advanced.cfg

**Status**: Modified

**Summary**: +350, -268, ~9 changes

**Key Changes**:

**Total changes**: 627 (showing top 8)

• **WorldSpawner.16.GroupRadius**: `10` *(new setting)*
• **WorldSpawner.16.GroupSizeMax**: `2` *(new setting)*
• **WorldSpawner.16.GroupSizeMin**: `1` *(new setting)*
• **WorldSpawner.16.SpawnChance**: `4.20` *(new setting)*
• **WorldSpawner.16.SpawnDistance**: `70` *(new setting)*
• **WorldSpawner.30.GroupRadius**: `3` *(new setting)*
• **WorldSpawner.30.GroupSizeMax**: `1` *(new setting)*
• **WorldSpawner.30.GroupSizeMin**: `1` *(new setting)*
• ... and 619 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| WorldSpawner.32001.SpawnChance | 15 | 7.50 | -7.5 |
| WorldSpawner.32001.SpawnInterval | 300 | 1200 | +900 |

**Full Diff**:

```diff
--- backup/spawn_that.world_spawners_advanced.cfg+++ current/spawn_that.world_spawners_advanced.cfg@@ -1,226 +1,501 @@-###################
-# Index: 32000+ Extra_Spawns
-###################
-
-[WorldSpawner.32000]
-Name=RancidRemains
+# Auto-generated file for adding World Spawner configurations.
+# This file is empty by default. It is intended to contains changes only, to avoid unintentional modifications as well as to reduce unnecessary performance cost.
+# Full documentation can be found at https://asharppen.github.io/Valheim.SpawnThat.
+# To get started:
+#     1. Generate default configs in BepInEx/Debug folder, by enabling WriteSpawnTablesToFileBeforeChanges in 'spawn_that.cfg'.
+#     2. Start game and enter a world, and wait a short moment (ca. 10 seconds) for files to generate.
+#     3. Go to generated file, and copy the creatures you want to modify into this file
+#     4. Make your changes.
+# To find modded configs and change those, enable WriteSpawnTablesToFileAfterChanges in 'spawn_that.cfg', and do as described above.
+
+
+# Target POI density: ~0.14 targets/km²
+
+[WorldSpawner.16]
+Name = greydwarf DAY
+PrefabName = Greydwarf
+Biomes = BlackForest
+Enabled = true
+MaxSpawned = 3
+SpawnInterval = 750
+# was 300 → slower spawn checks
+SpawnChance = 4.20
+# was 12 → lower global density (further reduced)
+SpawnDistance = 70
+GroupSizeMin = 1
+GroupSizeMax = 2
+# was 3 → smaller packs
+GroupRadius = 10
+GroundOffset = 0.5
+SpawnDuringDay = true
+SpawnDuringNight = false
+SpawnInForest = true
+SpawnOutsideForest = true
+ConditionTiltMax = 35
+BiomeArea = 7
+SetFaction = ForestMonsters
+SetTryDespawnOnConditionsInvalid = true
+
+[WorldSpawner.30]
+Name = Troll Day
+Biomes = BlackForest
+PrefabName = Troll
+Enabled = true
+HuntPlayer = false
+MaxSpawned = 1
+SpawnInterval = 1200
+SpawnChance = 10.00
+SpawnDistance = 64
+GroupSizeMin = 1
+GroupSizeMax = 1
+GroupRadius = 3
+GroundOffset = 0.5
+SpawnDuringDay = true
+SpawnDuringNight = false
+SpawnInForest = true
+SpawnOutsideForest = true
+ConditionTiltMax = 35
+BiomeArea = -1
+SetTryDespawnOnConditionsInvalid = true
+
+[WorldSpawner.32001]
+Name = BlackForest Troll Spawn
+Biomes = BlackForest
+PrefabName = Troll
+Enabled = true
+HuntPlayer = false
+MaxSpawned = 1
+SpawnInterval = 1200
+SpawnChance = 7.50
+SpawnDistance = 64
+GroupSizeMin = 1
+GroupSizeMax = 1
+GroupRadius = 3
+GroundOffset = 0.5
+SpawnDuringDay = false
+SpawnDuringNight = true
+SpawnInForest = true
+SpawnOutsideForest = true
+ConditionAltitudeMin = 0
+ConditionAltitudeMax = 1000
+ConditionTiltMin = 0
+ConditionTiltMax = 35
+ConditionDistanceToCenterMin = 1000
+SetTryDespawnOnConditionsInvalid = true
+SetFaction = Boss
+
+[WorldSpawner.666]
+Name = Mushroom Meadows
+PrefabName = MushroomMeadows_MP
+Biomes = Meadows
+Enabled = true
+MaxSpawned = 1
+# aligned for sparse mushrooms
+SpawnInterval = 1500
+# aligned across biomes for consistent POI density
+SpawnChance = 4.50
+# aligned for sparse mushroom encounters
+ConditionDistanceToCenterMin = 500
+
+[WorldSpawner.667]
+Name = Mushroom Forest
+PrefabName = MushroomForest_MP
+Biomes = BlackForest
+Enabled = true
+MaxSpawned = 1
+# aligned for sparse mushrooms
+SpawnInterval = 1500
+# aligned across biomes for consistent POI density
+SpawnChance = 4.50
+# aligned for sparse mushroom encounters
+ConditionDistanceToCenterMin = 500
+
+[WorldSpawner.668]
+Name = Mushroom Swamp
+PrefabName = MushroomSwamp_MP
+Biomes = Swamp
+Enabled = true
+MaxSpawned = 1
+# aligned for sparse mushrooms
+SpawnInterval = 1500
+# aligned across biomes for consistent POI density
+SpawnChance = 4.50
+# aligned for sparse mushroom encounters
+ConditionDistanceToCenterMin = 500
+
+[WorldSpawner.669]
+Name = Mushroom Mountain
+PrefabName = MushroomMountain_MP
+Biomes = Mountain
+Enabled = true
+MaxSpawned = 1
+# aligned for sparse mushrooms
+SpawnInterval = 1500
+# aligned across biomes for consistent POI density
+SpawnChance = 4.50
+# aligned for sparse mushroom encounters
+ConditionDistanceToCenterMin = 500
+
+[WorldSpawner.670]
+Name = Mushroom Plains
+PrefabName = MushroomPlains_MP
+Biomes = Plains
+Enabled = true
+MaxSpawned = 1
+# aligned for sparse mushrooms
+SpawnInterval = 1500
+# aligned across biomes for consistent POI density
+SpawnChance = 4.50
+# aligned for sparse mushroom encounters
+ConditionDistanceToCenterMin = 500
+
+[WorldSpawner.671]
+Name = Mushroom Mistlands
+PrefabName = MushroomMistlands_MP
+Biomes = Mistlands
+Enabled = true
+MaxSpawned = 1
+# aligned for sparse mushrooms
+SpawnInterval = 1500
+# aligned across biomes for consistent POI density
+SpawnChance = 4.50
+# aligned for sparse mushroom encounters
+ConditionDistanceToCenterMin = 500
+
+[WorldSpawner.672]
+Name = Mushroom Ashlands
+PrefabName = MushroomAshLands_MP
+Biomes = AshLands
+Enabled = true
+MaxSpawned = 1
+# aligned for sparse mushrooms
+SpawnInterval = 1500
+# aligned across biomes for consistent POI density
+SpawnChance = 4.50
+# aligned for sparse mushroom encounters
+ConditionDistanceToCenterMin = 500
+
+[WorldSpawner.673]
+# Mushroom Deep North (POI)
+PrefabName = MushroomDeepNorth_MP
+Biomes = DeepNorth
+Enabled = true
+MaxSpawned = 1
+# aligned for sparse mushrooms
+SpawnInterval = 1500
+# aligned across biomes for consistent POI density
+SpawnChance = 4.50
+# aligned for sparse mushroom encounters
+ConditionDistanceToCenterMin = 2500
+# was 500 → deeper exploration
+
+[WorldSpawner.674]
+Name = Frost Dragon
+PrefabName = Dragon
+Biomes = DeepNorth
+Enabled = true
+MaxSpawned = 1
+SpawnInterval = 1800
+# was 1200
+SpawnChance = 3.50
+# was 7.50
+RequiredEnvironments = SnowStorm
+ConditionAltitudeMin = 120
+# was 100
+
+[WorldSpawner.674.CreatureLevelAndLootControl]
+ConditionWorldLevelMin = 7
+
+[WorldSpawner.675]
+Name = Coin Troll
+PrefabName = CoinTroll
+Biomes = BlackForest
+Enabled = true
+MaxSpawned = 1
+SpawnInterval = 1500
+SpawnChance = 5.25
+TemplateId = CoinTroll
+
+[WorldSpawner.675.CreatureLevelAndLootControl]
+ConditionWorldLevelMin = 2
+
+
+[WorldSpawner.677]
+Name = Avalanche Drake
+PrefabName = Dragon
+Biomes = Mountain
+Enabled = true
+MaxSpawned = 1
+SpawnInterval = 1800
+SpawnChance = 5.25
+RequiredEnvironments = SnowStorm
+ConditionAltitudeMin = 100
+TemplateId = AvalancheDrake
+
+[WorldSpawner.677.CreatureLevelAndLootControl]
+ConditionWorldLevelMin = 4
+
+[WorldSpawner.678]
+Name = Tempest Serpent
+PrefabName = Serpent
+Biomes = Ocean
+Enabled = true
+MaxSpawned = 1
+SpawnInterval = 2400
+SpawnChance = 26.25
+RequiredEnvironments = ThunderStorm
+LevelMin = 6
+LevelMax = 6
+TemplateId = TempestSerpent
+
+[WorldSpawner.678.CreatureLevelAndLootControl]
+ConditionWorldLevelMin = 3
+
+[WorldSpawner.679]
+Name = Royal Lox
+PrefabName = Lox
+Biomes = Plains
+Enabled = true
+MaxSpawned = 1
+SpawnInterval = 1500
+SpawnChance = 52.50
+RequiredGlobalKey = RoyalLoxEvent
+TemplateId = RoyalLox
+
+[WorldSpawner.679.CreatureLevelAndLootControl]
+ConditionWorldLevelMin = 5
+
+[WorldSpawner.680]
+Name = Ashlands Golem
+PrefabName = StoneGolem
+Biomes = AshLands
+Enabled = true
+MaxSpawned = 1
+SpawnInterval = 1500
+SpawnChance = 13.13
+RequiredEnvironments = Clear
+TemplateId = MagmaGolem
+
+[WorldSpawner.680.CreatureLevelAndLootControl]
+ConditionWorldLevelMin = 7
+
+[WorldSpawner.681]
+Name = Seeker Queen
+PrefabName = SeekerQueen
+Biomes = Mistlands
+Enabled = true
+MaxSpawned = 1
+SpawnInterval = 1500
+SpawnChance = 2.10
+TemplateId = SeekerQueen
+
+[WorldSpawner.681.CreatureLevelAndLootControl]
+ConditionWorldLevelMin = 6
+
+[WorldSpawner.682]
+Name = Leech Matron
+PrefabName = Leech
+Biomes = Swamp
+Enabled = true
+MaxSpawned = 1
+SpawnInterval = 2400
+SpawnChance = 2.45
+# 30% reduction
+RequiredEnvironments = Rain
+SpawnDuringDay = false
+SpawnDuringNight = true
+OceanDepthMin = 4
+TemplateId = LeechMatron
+
+[WorldSpawner.682.CreatureLevelAndLootControl]
+ConditionWorldLevelMin = 3
+
+[WorldSpawner.683]
+Name = Weaver Queen
+PrefabName = SeekerQueen
+Biomes = Mistlands
+Enabled = true
+MaxSpawned = 1
+SpawnInterval = 1500
+SpawnChance = 2.10
+SpawnDuringDay = false
+SpawnDuringNight = true
+TemplateId = WeaverQueen
+
+[WorldSpawner.683.CreatureLevelAndLootControl]
+ConditionWorldLevelMin = 6
+
+[WorldSpawner.684]
+Name = Frost Wyrm
+PrefabName = Dragon
+Biomes = DeepNorth
+Enabled = true
+MaxSpawned = 1
+SpawnInterval = 1500
+SpawnChance = 3.50
+RequiredEnvironments = SnowStorm
+ConditionAltitudeMin = 50
+TemplateId = FrostWyrm
+
+[WorldSpawner.684.CreatureLevelAndLootControl]
+ConditionWorldLevelMin = 7
+
+[WorldSpawner.901]
+Name = Arctic Wolf Patrol
+PrefabName = ArcticWolf
+Biomes = DeepNorth
+Enabled = true
+MaxSpawned = 2
+SpawnInterval = 900
+SpawnChance = 60.00
+LevelMin = 2
+LevelMax = 4
+GroupSizeMin = 2
+GroupSizeMax = 3
+
+[WorldSpawner.901.CreatureLevelAndLootControl]
+ConditionWorldLevelMin = 7
+
+[WorldSpawner.902]
+Name = Jotunn Scout
+PrefabName = JotunnShaman
+Biomes = DeepNorth
+Enabled = true
+MaxSpawned = 1
+SpawnInterval = 2400
+SpawnChance = 3.50
+GroupSizeMin = 1
+GroupSizeMax = 1
+ConditionAltitudeMin = 20
+
+[WorldSpawner.902.CreatureLevelAndLootControl]
+ConditionWorldLevelMin = 8
+
+[WorldSpawner.33003]
+Name = giant_brain
+Biomes = Mistlands
+PrefabName = giant_brain
+Enabled = true
+HuntPlayer = false
+MaxSpawned = 1
+SpawnInterval = 1500
+SpawnChance = 7
+SpawnDistance = 138
+SpawnRadiusMin = 0
+SpawnRadiusMax = 0
+GroupSizeMin = 1
+GroupSizeMax = 1
+GroupRadius = 1
+GroundOffset = -6
+ConditionAltitudeMin = 10
+ConditionAltitudeMax = 120
+ConditionPositionMustNotBeNearPrefabs = giant_brain, giant_brain_frac
+ConditionPositionMustNotBeNearPrefabsDistance = 138
+BiomeArea = Median
+
+# Calmer days, spikier nights for swamp ambient spawns
+
+# Disable vanilla swamp skeleton spawner
+[WorldSpawner.32]
+Enabled=False
+
+# Daytime poison skeletons with reduced activity
+[WorldSpawner.32032]
+Name=SwampSkeletonDay
 Enabled=True
-Biomes=BlackForest
+Biomes=Swamp
 PrefabName=Skeleton_Poison
 HuntPlayer=False
 MaxSpawned=2
 SpawnInterval=600
-SpawnChance=10
+SpawnChance=3.5
+LevelMin=1
+LevelMax=3
+LevelUpChance=-1
 LevelUpMinCenterDistance=0
-SpawnDistance=64
+SpawnDistance=20
+SpawnRadiusMin=0
+SpawnRadiusMax=0
+RequiredGlobalKey=
+RequiredEnvironments=
+GroupSizeMin=1
+GroupSizeMax=2
+GroupRadius=4
+GroundOffset=0.5
+SpawnDuringDay=True
+SpawnDuringNight=False
+ConditionAltitudeMin=-1
+ConditionAltitudeMax=10
+ConditionTiltMin=0
+ConditionTiltMax=35
+SpawnInForest=True
+SpawnOutsideForest=True
+OceanDepthMin=0
+OceanDepthMax=0
+BiomeArea=7
+SetFaction=Undead
+
+# Nighttime poison skeletons with higher activity
+[WorldSpawner.32033]
+Name=SwampSkeletonNight
+Enabled=True
+Biomes=Swamp
+PrefabName=Skeleton_Poison
+HuntPlayer=False
+MaxSpawned=2
+SpawnInterval=900
+SpawnChance=10.5
+LevelMin=1
+LevelMax=3
+LevelUpChance=-1
+LevelUpMinCenterDistance=0
+SpawnDistance=20
 SpawnRadiusMin=0
 SpawnRadiusMax=0
 RequiredGlobalKey=
 RequiredEnvironments=
 GroupSizeMin=1
 GroupSizeMax=1
-GroupRadius=5
+GroupRadius=4
 GroundOffset=0.5
 SpawnDuringDay=False
 SpawnDuringNight=True
-ConditionAltitudeMin=0.1
-ConditionAltitudeMax=1000
-ConditionLocation=Crypt2, Crypt3, Crypt4
-SetTryDespawnOnConditionsInvalid=true
-SetFaction=Boss
-
-[WorldSpawner.32001]
-Name=
-Enabled=True
-Biomes=BlackForest
-PrefabName=Troll
-HuntPlayer=False
-MaxSpawned=1
-SpawnInterval=300
-SpawnChance=15
-SpawnDistance=64
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=1
-GroupRadius=3
-GroundOffset=0.5
-SpawnDuringDay=False
-SpawnDuringNight=True
-ConditionAltitudeMin=0
-ConditionAltitudeMax=1000
+ConditionAltitudeMin=-1
+ConditionAltitudeMax=10
 ConditionTiltMin=0
 ConditionTiltMax=35
 SpawnInForest=True
 SpawnOutsideForest=True
-ConditionDistanceToCenterMin=1000
-SetTryDespawnOnConditionsInvalid=true
-SetFaction=Boss
-
-[WorldSpawner.32002]
-Name=
+OceanDepthMin=0
+OceanDepthMax=0
+BiomeArea=7
+SetFaction=Undead
+
+# Abominations only roam at night and are more common
+[WorldSpawner.52]
+Name=Abomination
 Enabled=True
-Biomes=Ocean
-PrefabName=HelWraith_TW
+Biomes=Swamp
+PrefabName=Abomination
 HuntPlayer=False
 MaxSpawned=1
-SpawnInterval=200
-SpawnChance=5
-SpawnDistance=100
+SpawnInterval=3000
+SpawnChance=35
+LevelUpChance=-1
+LevelUpMinCenterDistance=0
+SpawnDistance=30
 SpawnRadiusMin=0
 SpawnRadiusMax=0
-RequiredGlobalKey= defeated_bonemass
-RequiredEnvironments= Misty
-GroupSizeMin=1
-GroupSizeMax=1
-GroupRadius=10
-GroundOffset=35
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin= -30
-ConditionAltitudeMax= 1000
-ConditionDistanceToCenterMin=2000
-SetTryDespawnOnConditionsInvalid=true
-SetFaction=Boss
-
-[WorldSpawner.32003]
-Name=
-Enabled=True
-Biomes=Ocean
-PrefabName=Hatchling
-HuntPlayer=False
-MaxSpawned=1
-SpawnInterval=200
-SpawnChance=5
-SpawnDistance=100
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey= defeated_dragon
-RequiredEnvironments= Rain
-GroupSizeMin=1
-GroupSizeMax=1
-GroupRadius=10
-GroundOffset=35
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin= -30
-ConditionAltitudeMax= 1000
-ConditionDistanceToCenterMin=2000
-SetTryDespawnOnConditionsInvalid=true
-SetFaction=Boss
-
-[WorldSpawner.32004]
-Name=
-Enabled=True
-Biomes=Ocean
-PrefabName=Deathsquito
-HuntPlayer=False
-MaxSpawned=2
-SpawnInterval=200
-SpawnChance=5
-SpawnDistance=100
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey= defeated_goblinking
-RequiredEnvironments= Clear
-GroupSizeMin=2
-GroupSizeMax=2
-GroupRadius=10
-GroundOffset=30
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin= -30
-ConditionAltitudeMax= 1000
-ConditionDistanceToCenterMin=2000
-SetTryDespawnOnConditionsInvalid=true
-SetFaction=Boss
-
-[WorldSpawner.32005]
-Name=
-Enabled=True
-Biomes=Plains,
-PrefabName=GoblinBrute
-HuntPlayer=False
-MaxSpawned=2
-SpawnInterval=300
-SpawnChance=10
-LevelUpMinCenterDistance=0
-SpawnDistance=30
-SpawnRadiusMin=10
-SpawnRadiusMax=20
-RequiredGlobalKey=
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=2
-GroupRadius=3
-GroundOffset=0.5
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin=0
-ConditionAltitudeMax=1000
-ConditionTiltMin=0
-ConditionTiltMax=35
-SpawnInForest=True
-SpawnOutsideForest=True
-ConditionLocation=StoneTower1
-DistanceToTriggerPlayerConditions=5
-SetFaction=Boss
-
-[WorldSpawner.32006]
-Name=
-Enabled=True
-Biomes=Meadows,
-PrefabName=Fox_TW
-HuntPlayer=False
-MaxSpawned=4
-SpawnInterval=300
-SpawnChance=10
-LevelUpMinCenterDistance=0
-SpawnDistance=64
-SpawnRadiusMin=10
-SpawnRadiusMax=20
-RequiredGlobalKey=
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=2
-GroupRadius=3
-GroundOffset=0.5
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin=0
-ConditionAltitudeMax=1000
-ConditionTiltMin=0
-ConditionTiltMax=35
-SpawnInForest=True
-SpawnOutsideForest=True
-ConditionLocation=Runestone_Meadows, StoneCircle
-DistanceToTriggerPlayerConditions=5
-SetFaction=ForestMonsters
-
-[WorldSpawner.32007]
-Name=Shark
-Enabled=True
-Biomes=Ocean
-PrefabName=Shark_TW
-HuntPlayer=False
-MaxSpawned=1
-SpawnInterval=500
-SpawnChance=10
-SpawnDistance=50
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=
+RequiredGlobalKey= defeated_gdking
 RequiredEnvironments=
 GroupSizeMin=1
 GroupSizeMax=1
-GroupRadius=3
-GroundOffset=0.5
-SpawnDuringDay=True
+GroupRadius=1
+GroundOffset=0
+SpawnDuringDay=False
 SpawnDuringNight=True
-ConditionAltitudeMin=-1000
-ConditionAltitudeMax=-5
+ConditionAltitudeMin=-2
+ConditionAltitudeMax=5
 ConditionTiltMin=0
 ConditionTiltMax=35
 SpawnInForest=True
@@ -228,94 +503,4 @@ OceanDepthMin=0
 OceanDepthMax=0
 BiomeArea=Median
-ConditionDistanceToCenterMin=3000
-SetFaction=Boss
-
-[WorldSpawner.32008]
-Name=Morgen [Sleeping]
-Enabled=True
-Biomes=AshLands
-PrefabName=Morgen
-HuntPlayer=False
-MaxSpawned=2
-SpawnInterval=2000
-SpawnChance=5
-LevelUpChance=-1
-LevelUpMinCenterDistance=0
-SpawnDistance=60
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=1
-GroupRadius=3
-GroundOffset=0
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin=0
-ConditionAltitudeMax=1000
-ConditionTiltMin=0
-ConditionTiltMax=35
-SpawnInForest=True
-SpawnOutsideForest=True
-OceanDepthMin=0
-OceanDepthMax=0
-BiomeArea=Everything
-ConditionPositionMustNotBeNearPrefabs=Morgen_NonSleeping
-
-###################
-# Index: 32100+ Pickables
-###################
-
-[WorldSpawner.32100]
-Name=Pickable_SeedOnion
-Enabled=True
-Biomes=Mountain
-PrefabName=Pickable_SeedOnion
-HuntPlayer=False
-MaxSpawned=1
-SpawnInterval=600
-SpawnChance=10
-SpawnDistance=64
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=defeated_bonemass
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=2
-GroupRadius=2
-GroundOffset=0.1
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin=120
-ConditionAltitudeMax=1000
-SpawnInForest=True
-SpawnOutsideForest=True
-ConditionPositionMustNotBeNearPrefabs=Pickable_SeedOnion
-
-[WorldSpawner.32101]
-Name=TurnipSeeds
-Enabled=True
-Biomes=Swamp
-PrefabName=Pickable_SeedTurnip
-HuntPlayer=False
-MaxSpawned=1
-SpawnInterval=600
-SpawnChance=10
-SpawnDistance=120
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=defeated_gdking
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=2
-GroupRadius=2
-GroundOffset=0.1
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin=0
-ConditionAltitudeMax=1000
-SpawnInForest=True
-SpawnOutsideForest=True
-ConditionPositionMustNotBeNearPrefabs=Pickable_SeedTurnip+SetFaction=

```

---

#### spawn_that.local_spawners_advanced.cfg

**Status**: Modified

**Summary**: -189, ~17 changes

**Key Changes**:

**Total changes**: 206 (showing top 8)

• **AbandonedLogCabin02.StoneGolem.LevelMax**: `6` *(removed)*
• **AbandonedLogCabin02.StoneGolem.LevelMin**: `1` *(removed)*
• **AbandonedLogCabin02.StoneGolem.LevelUpChance**: `50` *(removed)*
• **AbandonedLogCabin02.StoneGolem.RespawnTime**: `0` *(removed)*
• **AbandonedLogCabin02.StoneGolem.TriggerDistance**: `60` *(removed)*
• **AbandonedLogCabin03.Skeleton.LevelMax**: `6` *(removed)*
• **AbandonedLogCabin03.Skeleton.LevelMin**: `1` *(removed)*
• **AbandonedLogCabin03.Skeleton.LevelUpChance**: `10` *(removed)*
• ... and 198 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| SwampHut3.Wraith.RespawnTime | 0 | 2400 | +2400 |
| SwampHut3.Wraith.TriggerDistance | 60 | 35 | -25 |
| SwampHut4.Draugr.RespawnTime | 0 | 2400 | +2400 |
| SwampHut4.Draugr.TriggerDistance | 60 | 35 | -25 |
| SwampHut4.Draugr_Ranged.RespawnTime | 0 | 2400 | +2400 |
| SwampHut4.Draugr_Ranged.TriggerDistance | 60 | 35 | -25 |
| SwampHut5.Wraith.RespawnTime | 0 | 2400 | +2400 |
| SwampHut5.Wraith.TriggerDistance | 60 | 35 | -25 |
| SwampWell1.Draugr_Elite.RespawnTime | 0 | 2400 | +2400 |
| SwampWell1.Draugr_Elite.TriggerDistance | 60 | 35 | -25 |

**Full Diff**:

```diff
--- backup/spawn_that.local_spawners_advanced.cfg+++ current/spawn_that.local_spawners_advanced.cfg@@ -1,257 +1,43 @@-####################
-# BlackForest
-####################
+# Auto-generated file for adding Local Spawner configurations.
+# This file is empty by default. It is intended to contains changes only, to avoid unintentional modifications as well as to reduce unnecessary performance cost.
+# Full documentation can be found at https://asharppen.github.io/Valheim.SpawnThat.
+# To get started: 
+#     1. Generate default configs in BepInEx/Debug folder, by enabling WriteSpawnTablesToFileBeforeChanges in 'spawn_that.cfg'.
+#     2. Start game and enter a world, and wait a short moment (ca. 10 seconds) for files to generate.
+#     3. Go to generated file, and copy the creatures you want to modify into this file. Multiple local spawner files will have been generated, use either the one for locations or dungeons, depending on what you want to modify.
+#     4. Make your changes.
 
-[Ruin1.Greydwarf_Shaman]
-PrefabName=GreydwarfMage_TW
-Enabled=True
-SpawnAtDay=True
-SpawnAtNight=True
-LevelMin=1
-LevelMax=6
-LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
+# Tweaks to swamp structure spawners to avoid stacking pressure.
+# HelWraith swaps and bone piles previously caused permanent red-alert zones.
+# Limiting each structure to a single occupant with long respawn times preserves threat without spam.
 
-####################
-# Swamp
-####################
+# Swamp huts retain a single Wraith with an extended respawn interval.
 
 [SwampHut3.Wraith]
-PrefabName=HelWraith_TW
-Enabled=True
-SpawnAtDay=True
-SpawnAtNight=True
-LevelMin=1
-LevelMax=6
-LevelUpChance=15
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
+RespawnTime=2400
+TriggerDistance=35
+SetPatrolPoint=False
 
+[SwampHut5.Wraith]
+RespawnTime=2400
+TriggerDistance=35
+SetPatrolPoint=False
+
+# Disable additional Draugr spawns in huts to keep only one occupant active.
 [SwampHut4.Draugr]
-PrefabName=Draugr_Elite
-Enabled=True
-SpawnAtDay=True
-SpawnAtNight=True
-LevelMin=1
-LevelMax=6
-LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
+Enabled=False
+RespawnTime=2400
+TriggerDistance=35
+SetPatrolPoint=False
 
 [SwampHut4.Draugr_Ranged]
-PrefabName=Draugr_Elite
-Enabled=True
-SpawnAtDay=True
-SpawnAtNight=True
-LevelMin=1
-LevelMax=6
-LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
+Enabled=False
+RespawnTime=2400
+TriggerDistance=35
+SetPatrolPoint=False
 
-[SwampHut5.Wraith]
-PrefabName=HelWraith_TW
-Enabled=True
-SpawnAtDay=True
-SpawnAtNight=True
-LevelMin=1
-LevelMax=6
-LevelUpChance=15
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
-
+# Wells retain their elite guard but with a long respawn to prevent piling.
 [SwampWell1.Draugr_Elite]
-PrefabName=HelWraith_TW
-Enabled=True
-SpawnAtDay=True
-SpawnAtNight=True
-LevelMin=1
-LevelMax=6
-LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
-
-[SunkenCrypt4.Draugr]
-PrefabName=Draugr_Elite
-Enabled=True
-SpawnAtDay=True
-SpawnAtNight=True
-LevelMin=1
-LevelMax=6
-LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
-
-[SunkenCrypt4.BlobElite]
-PrefabName=Draugr_Elite
-Enabled=True
-SpawnAtDay=True
-SpawnAtNight=True
-LevelMin=1
-LevelMax=6
-LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
-
-[FireHole.Surtling]
-PrefabName=Surtling
-Enabled=True
-SpawnAtDay=True
-SpawnAtNight=True
-LevelMin=1
-LevelMax=1
-LevelUpChance=10
-RespawnTime=15
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
-SetFaction=Boss
-
-[FireHole.Surtling.CreatureLevelAndLootControl]
-UseDefaultLevels=true
-
-####################
-# Mountains
-####################
-
-[AbandonedLogCabin02.StoneGolem]
-PrefabName=FenringMage_TW
-Enabled=True
-SpawnAtDay=True
-SpawnAtNight=True
-LevelMin=1
-LevelMax=6
-LevelUpChance=50
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
-
-[AbandonedLogCabin03.Skeleton]
-PrefabName=Fenring
-Enabled=True
-SpawnAtDay=False
-SpawnAtNight=True
-LevelMin=1
-LevelMax=6
-LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
-
-[AbandonedLogCabin03.StoneGolem]
-PrefabName=StoneGolem
-Enabled=True
-SpawnAtDay=True
-SpawnAtNight=True
-LevelMin=1
-LevelMax=6
-LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
-
-[AbandonedLogCabin04.Skeleton]
-PrefabName=Wolf
-Enabled=True
-SpawnAtDay=True
-SpawnAtNight=True
-LevelMin=1
-LevelMax=6
-LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
-
-[StoneTowerRuins04.Skeleton]
-PrefabName=Skeleton
-Enabled=True
-SpawnAtDay=True
-SpawnAtNight=True
-LevelMin=1
-LevelMax=6
-LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
-
-[StoneTowerRuins04.Draugr]
-PrefabName=Hatchling
-Enabled=True
-SpawnAtDay=True
-SpawnAtNight=True
-LevelMin=1
-LevelMax=6
-LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
-
-[StoneTowerRuins05.Skeleton]
-PrefabName=Skeleton
-Enabled=True
-SpawnAtDay=True
-SpawnAtNight=True
-LevelMin=1
-LevelMax=6
-LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True
-
-####################
-# Plains
-####################
-
-[StoneHenge5.Goblin]
-PrefabName=GoblinMage_TW
-Enabled=True
-SpawnAtDay=True
-SpawnAtNight=True
-LevelMin=1
-LevelMax=6
-LevelUpChance=10
-RespawnTime=0
-TriggerDistance=60
-TriggerNoise=0
-SpawnInPlayerBase=False
-SetPatrolPoint=True+RespawnTime=2400
+TriggerDistance=35
+SetPatrolPoint=False

```

---

#### spawn_that.spawnarea_spawners.cfg

**Status**: Modified

**Summary**: -127, ~1 changes

**Key Changes**:

**Total changes**: 128 (showing top 8)

• **BonePileSpawner.ConditionPlayerWithinDistance**: `20` *(removed)*
• **BonePileSpawner.DistanceConsideredClose**: `20` *(removed)*
• **BonePileSpawner.DistanceConsideredFar**: `1000` *(removed)*
• **BonePileSpawner.LevelUpChance**: `15` *(removed)*
• **BonePileSpawnerMountain.ConditionPlayerWithinDistance**: `20` *(removed)*
• **BonePileSpawnerMountain.DistanceConsideredClose**: `20` *(removed)*
• **BonePileSpawnerMountain.DistanceConsideredFar**: `1000` *(removed)*
• **BonePileSpawnerMountain.LevelUpChance**: `15` *(removed)*
• ... and 120 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| Spawner_GreydwarfNest.SpawnInterval | 15 | 25 | +10 |

**Full Diff**:

```diff
--- backup/spawn_that.spawnarea_spawners.cfg+++ current/spawn_that.spawnarea_spawners.cfg@@ -1,188 +1,14 @@-####################
-# BlackForest
-####################
+# Auto-generated file for adding SpawnArea Spawner configurations.
+# This file is empty by default. It is intended to contains changes only, to avoid unintentional modifications as well as to reduce unnecessary performance cost.
+# Full documentation can be found at https://asharppen.github.io/Valheim.SpawnThat.
+# To get started: 
+#     1. Generate default configs in BepInEx/Debug folder, by enabling WriteSpawnTablesToFileBeforeChanges in 'spawn_that.cfg'.
+#     2. Start game and enter a world, and wait a short moment (ca. 10 seconds) for files to generate.
+#     3. Go to generated file, and copy the spawners you want to modify into this file
+#     4. Make your changes.
+# To find modded configs and change those, enable WriteConfigsToFile in 'spawn_that.cfg', and do as described above.
 
 [Spawner_GreydwarfNest]
-IdentifyByName=Spawner_GreydwarfNest
-LevelUpChance=15
-SpawnInterval=15
-SetPatrol=True
-ConditionPlayerWithinDistance=60
-ConditionMaxCloseCreatures=2
-ConditionMaxCreatures=100
-DistanceConsideredClose=20
-DistanceConsideredFar=1000
-OnGroundOnly=True
+IdentifyByName = Spawner_GreydwarfNest
+SpawnInterval = 25
 
-[Spawner_GreydwarfNest.0]
-Enabled=True
-TemplateEnabled=True
-PrefabName=Greydwarf
-SpawnWeight=5
-
-[Spawner_GreydwarfNest.1]
-Enabled=True
-TemplateEnabled=True
-PrefabName=Greydwarf_Elite
-SpawnWeight=1
-
-[Spawner_GreydwarfNest.2]
-Enabled=True
-TemplateEnabled=True
-PrefabName=Greydwarf_Shaman
-SpawnWeight=1
-
-[Spawner_GreydwarfNest.3]
-Enabled=True
-TemplateEnabled=True
-PrefabName=GreydwarfMage_TW
-SpawnWeight=0.2
-
-####################
-
-[BonePileSpawner]
-IdentifyByName=BonePileSpawner
-IdentifyByBiome=BlackForest
-LevelUpChance=15
-SpawnInterval=15
-SetPatrol=True
-ConditionPlayerWithinDistance=20
-ConditionMaxCloseCreatures=2
-ConditionMaxCreatures=100
-DistanceConsideredClose=20
-DistanceConsideredFar=1000
-OnGroundOnly=False
-
-[BonePileSpawner.0]
-Enabled=True
-TemplateEnabled=True
-PrefabName=Skeleton
-SpawnWeight=2
-
-[BonePileSpawner.1]
-Enabled=True
-TemplateEnabled=True
-PrefabName=Ghost
-SpawnWeight=0.5
-
-[BonePileSpawner.2]
-Enabled=True
-TemplateEnabled=True
-PrefabName=Skeleton_Poison
-SpawnWeight=0.2
-
-####################
-# Swamp
-####################
-
-[BonePileSpawnerSwamp]
-IdentifyByName=BonePileSpawner
-IdentifyByBiome=Swamp
-LevelUpChance=15
-SpawnInterval=15
-SetPatrol=True
-ConditionPlayerWithinDistance=20
-ConditionMaxCloseCreatures=2
-ConditionMaxCreatures=100
-DistanceConsideredClose=20
-DistanceConsideredFar=1000
-OnGroundOnly=False
-
-[BonePileSpawnerSwamp.0]
-Enabled=True
-TemplateEnabled=True
-PrefabName=Skeleton
-SpawnWeight=4
-
-[BonePileSpawnerSwamp.1]
-Enabled=True
-TemplateEnabled=True
-PrefabName=Skeleton_Poison
-SpawnWeight=1
-
-[BonePileSpawnerSwamp.2]
-Enabled=True
-TemplateEnabled=True
-PrefabName=SkeletonMage_TW
-SpawnWeight=0.2
-
-####################
-
-[Spawner_DraugrPile]
-IdentifyByName=Spawner_DraugrPile
-LevelUpChance=15
-SpawnInterval=15
-SetPatrol=True
-ConditionPlayerWithinDistance=20
-ConditionMaxCloseCreatures=3
-ConditionMaxCreatures=100
-DistanceConsideredClose=20
-DistanceConsideredFar=1000
-OnGroundOnly=False
-
-[Spawner_DraugrPile.0]
-Enabled=True
-TemplateEnabled=True
-PrefabName=Draugr
-SpawnWeight=4
-
-[Spawner_DraugrPile.1]
-Enabled=True
-TemplateEnabled=True
-PrefabName=Draugr_Ranged
-SpawnWeight=4
-
-[Spawner_DraugrPile.2]
-Enabled=True
-TemplateEnabled=True
-PrefabName=Draugr_Elite
-SpawnWeight=1
-
-[Spawner_DraugrPile.3]
-Enabled=True
-TemplateEnabled=True
-PrefabName=Crawler_TW
-SpawnWeight=0.1
-
-####################
-# Mountain
-####################
-
-[BonePileSpawnerMountain]
-IdentifyByName=BonePileSpawner
-IdentifyByBiome=Mountain
-LevelUpChance=15
-SpawnInterval=15
-SetPatrol=True
-ConditionPlayerWithinDistance=20
-ConditionMaxCloseCreatures=3
-ConditionMaxCreatures=100
-DistanceConsideredClose=20
-DistanceConsideredFar=1000
-OnGroundOnly=False
-
-[BonePileSpawnerMountain.0]
-Enabled=True
-TemplateEnabled=True
-PrefabName=Skeleton
-SpawnWeight=1
-
-[Spawner_Kvastur]
-IdentifyByName=Spawner_Kvastur
-LevelUpChance=10
-SpawnInterval=300
-SetPatrol=True
-ConditionPlayerWithinDistance=60
-ConditionMaxCloseCreatures=1
-ConditionMaxCreatures=1
-DistanceConsideredClose=0.5
-DistanceConsideredFar=1000
-OnGroundOnly=False
-
-[Spawner_Kvastur.0]
-Enabled=True
-TemplateEnabled=True
-PrefabName=BogWitchKvastur
-SpawnWeight=10
-LevelMin=1
-LevelMax=1
```

---

#### spawn_that.simple.cfg

**Status**: Modified

**Summary**: +336, -292 changes

**Key Changes**:

**Total changes**: 628 (showing top 8)

• **ABOMINATION.GroupSizeMaxMultiplier**: `1` *(new setting)*
• **ABOMINATION.GroupSizeMinMultiplier**: `1` *(new setting)*
• **ABOMINATION.SpawnFrequencyMultiplier**: `1` *(new setting)*
• **ABOMINATION.SpawnMaxMultiplier**: `1` *(new setting)*
• **BLACKBEAR_TW.GroupSizeMaxMultiplier**: `1` *(new setting)*
• **BLACKBEAR_TW.GroupSizeMinMultiplier**: `1` *(new setting)*
• **BLACKBEAR_TW.SpawnFrequencyMultiplier**: `1` *(new setting)*
• **BLACKBEAR_TW.SpawnMaxMultiplier**: `1` *(new setting)*
• ... and 620 more changes

**Full Diff**:

```diff
--- backup/spawn_that.simple.cfg+++ current/spawn_that.simple.cfg@@ -1,321 +1,726 @@-###################
-# Index: 32000+ Extra_Spawns
-###################
-
-[WorldSpawner.32000]
-Name=RancidRemains
-Enabled=True
-Biomes=BlackForest
-PrefabName=Skeleton_Poison
-HuntPlayer=False
-MaxSpawned=2
-SpawnInterval=600
-SpawnChance=10
-LevelUpMinCenterDistance=0
-SpawnDistance=64
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=1
-GroupRadius=5
-GroundOffset=0.5
-SpawnDuringDay=False
-SpawnDuringNight=True
-ConditionAltitudeMin=0.1
-ConditionAltitudeMax=1000
-ConditionLocation=Crypt2, Crypt3, Crypt4
-SetTryDespawnOnConditionsInvalid=true
-SetFaction=Boss
-
-[WorldSpawner.32001]
-Name=
-Enabled=True
-Biomes=BlackForest
-PrefabName=Troll
-HuntPlayer=False
-MaxSpawned=1
-SpawnInterval=300
-SpawnChance=15
-SpawnDistance=64
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=1
-GroupRadius=3
-GroundOffset=0.5
-SpawnDuringDay=False
-SpawnDuringNight=True
-ConditionAltitudeMin=0
-ConditionAltitudeMax=1000
-ConditionTiltMin=0
-ConditionTiltMax=35
-SpawnInForest=True
-SpawnOutsideForest=True
-ConditionDistanceToCenterMin=1000
-SetTryDespawnOnConditionsInvalid=true
-SetFaction=Boss
-
-[WorldSpawner.32002]
-Name=
-Enabled=True
-Biomes=Ocean
-PrefabName=HelWraith_TW
-HuntPlayer=False
-MaxSpawned=1
-SpawnInterval=200
-SpawnChance=5
-SpawnDistance=100
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey= defeated_bonemass
-RequiredEnvironments= Misty
-GroupSizeMin=1
-GroupSizeMax=1
-GroupRadius=10
-GroundOffset=35
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin= -30
-ConditionAltitudeMax= 1000
-ConditionDistanceToCenterMin=2000
-SetTryDespawnOnConditionsInvalid=true
-SetFaction=Boss
-
-[WorldSpawner.32003]
-Name=
-Enabled=True
-Biomes=Ocean
-PrefabName=Hatchling
-HuntPlayer=False
-MaxSpawned=1
-SpawnInterval=200
-SpawnChance=5
-SpawnDistance=100
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey= defeated_dragon
-RequiredEnvironments= Rain
-GroupSizeMin=1
-GroupSizeMax=1
-GroupRadius=10
-GroundOffset=35
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin= -30
-ConditionAltitudeMax= 1000
-ConditionDistanceToCenterMin=2000
-SetTryDespawnOnConditionsInvalid=true
-SetFaction=Boss
-
-[WorldSpawner.32004]
-Name=
-Enabled=True
-Biomes=Ocean
-PrefabName=Deathsquito
-HuntPlayer=False
-MaxSpawned=2
-SpawnInterval=200
-SpawnChance=5
-SpawnDistance=100
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey= defeated_goblinking
-RequiredEnvironments= Clear
-GroupSizeMin=2
-GroupSizeMax=2
-GroupRadius=10
-GroundOffset=30
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin= -30
-ConditionAltitudeMax= 1000
-ConditionDistanceToCenterMin=2000
-SetTryDespawnOnConditionsInvalid=true
-SetFaction=Boss
-
-[WorldSpawner.32005]
-Name=
-Enabled=True
-Biomes=Plains,
-PrefabName=GoblinBrute
-HuntPlayer=False
-MaxSpawned=2
-SpawnInterval=300
-SpawnChance=10
-LevelUpMinCenterDistance=0
-SpawnDistance=30
-SpawnRadiusMin=10
-SpawnRadiusMax=20
-RequiredGlobalKey=
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=2
-GroupRadius=3
-GroundOffset=0.5
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin=0
-ConditionAltitudeMax=1000
-ConditionTiltMin=0
-ConditionTiltMax=35
-SpawnInForest=True
-SpawnOutsideForest=True
-ConditionLocation=StoneTower1
-DistanceToTriggerPlayerConditions=5
-SetFaction=Boss
-
-[WorldSpawner.32006]
-Name=
-Enabled=True
-Biomes=Meadows,
-PrefabName=Fox_TW
-HuntPlayer=False
-MaxSpawned=4
-SpawnInterval=300
-SpawnChance=10
-LevelUpMinCenterDistance=0
-SpawnDistance=64
-SpawnRadiusMin=10
-SpawnRadiusMax=20
-RequiredGlobalKey=
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=2
-GroupRadius=3
-GroundOffset=0.5
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin=0
-ConditionAltitudeMax=1000
-ConditionTiltMin=0
-ConditionTiltMax=35
-SpawnInForest=True
-SpawnOutsideForest=True
-ConditionLocation=Runestone_Meadows, StoneCircle
-DistanceToTriggerPlayerConditions=5
-SetFaction=ForestMonsters
-
-[WorldSpawner.32007]
-Name=Shark
-Enabled=True
-Biomes=Ocean
-PrefabName=Shark_TW
-HuntPlayer=False
-MaxSpawned=1
-SpawnInterval=500
-SpawnChance=10
-SpawnDistance=50
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=1
-GroupRadius=3
-GroundOffset=0.5
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin=-1000
-ConditionAltitudeMax=-5
-ConditionTiltMin=0
-ConditionTiltMax=35
-SpawnInForest=True
-SpawnOutsideForest=True
-OceanDepthMin=0
-OceanDepthMax=0
-BiomeArea=Median
-ConditionDistanceToCenterMin=3000
-SetFaction=Boss
-
-[WorldSpawner.32008]
-Name=Morgen [Sleeping]
-Enabled=True
-Biomes=AshLands
-PrefabName=Morgen
-HuntPlayer=False
-MaxSpawned=2
-SpawnInterval=2000
-SpawnChance=5
-LevelUpChance=-1
-LevelUpMinCenterDistance=0
-SpawnDistance=60
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=1
-GroupRadius=3
-GroundOffset=0
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin=0
-ConditionAltitudeMax=1000
-ConditionTiltMin=0
-ConditionTiltMax=35
-SpawnInForest=True
-SpawnOutsideForest=True
-OceanDepthMin=0
-OceanDepthMax=0
-BiomeArea=Everything
-ConditionPositionMustNotBeNearPrefabs=Morgen_NonSleeping
-
-###################
-# Index: 32100+ Pickables
-###################
-
-[WorldSpawner.32100]
-Name=Pickable_SeedOnion
-Enabled=True
-Biomes=Mountain
-PrefabName=Pickable_SeedOnion
-HuntPlayer=False
-MaxSpawned=1
-SpawnInterval=600
-SpawnChance=10
-SpawnDistance=64
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=defeated_bonemass
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=2
-GroupRadius=2
-GroundOffset=0.1
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin=120
-ConditionAltitudeMax=1000
-SpawnInForest=True
-SpawnOutsideForest=True
-ConditionPositionMustNotBeNearPrefabs=Pickable_SeedOnion
-
-[WorldSpawner.32101]
-Name=TurnipSeeds
-Enabled=True
-Biomes=Swamp
-PrefabName=Pickable_SeedTurnip
-HuntPlayer=False
-MaxSpawned=1
-SpawnInterval=600
-SpawnChance=10
-SpawnDistance=120
-SpawnRadiusMin=0
-SpawnRadiusMax=0
-RequiredGlobalKey=defeated_gdking
-RequiredEnvironments=
-GroupSizeMin=1
-GroupSizeMax=2
-GroupRadius=2
-GroundOffset=0.1
-SpawnDuringDay=True
-SpawnDuringNight=True
-ConditionAltitudeMin=0
-ConditionAltitudeMax=1000
-SpawnInForest=True
-SpawnOutsideForest=True
-ConditionPositionMustNotBeNearPrefabs=Pickable_SeedTurnip+# This file was auto-generated by Spawn That 1.2.18 at 2025-07-27 00:01:58Z, with Valheim '0.220.5'.
+# The entries listed here is a manually written list of world spawned creatures, and changes only apply to world spawners.
+# Changes are applied after other Spawn That configs, so be careful not to do things like increase spawns in both world spawner and simple configs
+# The list only contains the default vanilla spawns, but can be manually expanded to modded creatures too. Just add more sections.
+
+[CROW]
+# Prefab name of entity to modify.
+PrefabName = Crow
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[FIREFLIES]
+# Prefab name of entity to modify.
+PrefabName = FireFlies
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[DEER]
+# Prefab name of entity to modify.
+PrefabName = Deer
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[FISH1]
+# Prefab name of entity to modify.
+PrefabName = Fish1
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[FISH2]
+# Prefab name of entity to modify.
+PrefabName = Fish2
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[FISH3]
+# Prefab name of entity to modify.
+PrefabName = Fish3
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[SEAGAL]
+# Prefab name of entity to modify.
+PrefabName = Seagal
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[LEVIATHAN]
+# Prefab name of entity to modify.
+PrefabName = Leviathan
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[BOAR]
+# Prefab name of entity to modify.
+PrefabName = Boar
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[NECK]
+# Prefab name of entity to modify.
+PrefabName = Neck
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[GREYLING]
+# Prefab name of entity to modify.
+PrefabName = Greyling
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[GREYDWARF]
+# Prefab name of entity to modify.
+PrefabName = Greydwarf
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[GREYDWARF_ELITE]
+# Prefab name of entity to modify.
+PrefabName = Greydwarf_Elite
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[GREYDWARF_SHAMAN]
+# Prefab name of entity to modify.
+PrefabName = Greydwarf_shaman
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[TROLL]
+# Prefab name of entity to modify.
+PrefabName = Troll
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[GHOST]
+# Prefab name of entity to modify.
+PrefabName = Ghost
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[SKELETON]
+# Prefab name of entity to modify.
+PrefabName = Skeleton
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[SKELETON_NOARCHER]
+# Prefab name of entity to modify.
+PrefabName = Skeleton_NoArcher
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[SKELETON_POISON]
+# Prefab name of entity to modify.
+PrefabName = Skeleton_poison
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[BLOB]
+# Prefab name of entity to modify.
+PrefabName = Blob
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[BLOBELITE]
+# Prefab name of entity to modify.
+PrefabName = BlobElite
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[DRAUGR]
+# Prefab name of entity to modify.
+PrefabName = Draugr
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[DRAUGR_RANGED]
+# Prefab name of entity to modify.
+PrefabName = Draugr_Ranged
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[DRAUGR_ELITE]
+# Prefab name of entity to modify.
+PrefabName = Draugr_Elite
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[LEECH]
+# Prefab name of entity to modify.
+PrefabName = Leech
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[SURTLING]
+# Prefab name of entity to modify.
+PrefabName = Surtling
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[WRAITH]
+# Prefab name of entity to modify.
+PrefabName = Wraith
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[WOLF]
+# Prefab name of entity to modify.
+PrefabName = Wolf
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[HATCHLING]
+# Prefab name of entity to modify.
+PrefabName = Hatchling
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[STONEGOLEM]
+# Prefab name of entity to modify.
+PrefabName = StoneGolem
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[FENRING]
+# Prefab name of entity to modify.
+PrefabName = Fenring
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[DEATHSQUITO]
+# Prefab name of entity to modify.
+PrefabName = Deathsquito
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[LOX]
+# Prefab name of entity to modify.
+PrefabName = Lox
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[GOBLIN]
+# Prefab name of entity to modify.
+PrefabName = Goblin
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[GOBLINARCHER]
+# Prefab name of entity to modify.
+PrefabName = GoblinArcher
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[GOBLINBRUTE]
+# Prefab name of entity to modify.
+PrefabName = GoblinBrute
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[GOBLINSHAMAN]
+# Prefab name of entity to modify.
+PrefabName = GoblinShaman
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[SERPENT]
+# Prefab name of entity to modify.
+PrefabName = Serpent
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+[ABOMINATION]
+# Prefab name of entity to modify.
+PrefabName = Abomination
+# Enable/Disable this set of modifiers.
+Enable = true
+# Change maximum of total spawned entities. 2 means twice as many.
+SpawnMaxMultiplier = 1
+# Change min number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMinMultiplier = 1
+# Change max number of entities that will spawn at once. 2 means twice as many.
+GroupSizeMaxMultiplier = 1
+# Change how often the game will try to spawn in new creatures.
+# Higher means more often. 2 is twice as often, 0.5 is double the time between spawn checks.
+SpawnFrequencyMultiplier = 1
+
+# Modded creature spawns
+[FOX_TW]
+PrefabName = Fox_TW
+Enable = true
+SpawnMaxMultiplier = 1
+GroupSizeMinMultiplier = 1
+GroupSizeMaxMultiplier = 1
+SpawnFrequencyMultiplier = 1
+
+[SHEEP_TW]
+PrefabName = Sheep_TW
+Enable = true
+SpawnMaxMultiplier = 1
+GroupSizeMinMultiplier = 1
+GroupSizeMaxMultiplier = 1
+SpawnFrequencyMultiplier = 1
+
+[RAZORBACK_TW]
+PrefabName = Razorback_TW
+Enable = true
+SpawnMaxMultiplier = 1
+GroupSizeMinMultiplier = 1
+GroupSizeMaxMultiplier = 1
+SpawnFrequencyMultiplier = 1
+
+[BLACKBEAR_TW]
+PrefabName = BlackBear_TW
+Enable = true
+SpawnMaxMultiplier = 1
+GroupSizeMinMultiplier = 1
+GroupSizeMaxMultiplier = 1
+SpawnFrequencyMultiplier = 1
+
+[GDANCIENTSHAMAN_TW]
+PrefabName = GDAncientShaman_TW
+Enable = true
+SpawnMaxMultiplier = 1
+GroupSizeMinMultiplier = 1
+GroupSizeMaxMultiplier = 1
+SpawnFrequencyMultiplier = 1
+
+[GREYDORFMAGE_TW]
+PrefabName = GreydwarfMage_TW
+Enable = true
+SpawnMaxMultiplier = 1
+GroupSizeMinMultiplier = 1
+GroupSizeMaxMultiplier = 1
+SpawnFrequencyMultiplier = 1
+
+[ROTTINGELK_TW]
+PrefabName = RottingElk_TW
+Enable = true
+SpawnMaxMultiplier = 1
+GroupSizeMinMultiplier = 1
+GroupSizeMaxMultiplier = 1
+SpawnFrequencyMultiplier = 1
+
+[CRAWLER_TW]
+PrefabName = Crawler_TW
+Enable = true
+SpawnMaxMultiplier = 1
+GroupSizeMinMultiplier = 1
+GroupSizeMaxMultiplier = 1
+SpawnFrequencyMultiplier = 1
+
+[HELWRAITH_TW]
+PrefabName = HelWraith_TW
+Enable = true
+SpawnMaxMultiplier = 1
+GroupSizeMinMultiplier = 1
+GroupSizeMaxMultiplier = 1
+SpawnFrequencyMultiplier = 1
+
+[SKELETONMAGE_TW]
+PrefabName = SkeletonMage_TW
+Enable = true
+SpawnMaxMultiplier = 1
+GroupSizeMinMultiplier = 1
+GroupSizeMaxMultiplier = 1
+SpawnFrequencyMultiplier = 1
+
+[OBSIDIANGOLEM_TW]
+PrefabName = ObsidianGolem_TW
+Enable = true
+SpawnMaxMultiplier = 1
+GroupSizeMinMultiplier = 1
+GroupSizeMaxMultiplier = 1
+SpawnFrequencyMultiplier = 1
+
+[GRIZZLYBEAR_TW]
+PrefabName = GrizzlyBear_TW
+Enable = true
+SpawnMaxMultiplier = 1
+GroupSizeMinMultiplier = 1
+GroupSizeMaxMultiplier = 1
+SpawnFrequencyMultiplier = 1
+
+[FENRINGMAGE_TW]
+PrefabName = FenringMage_TW
+Enable = true
+SpawnMaxMultiplier = 1
+GroupSizeMinMultiplier = 1
+GroupSizeMaxMultiplier = 1
+SpawnFrequencyMultiplier = 1
+
+[PROWLER_TW]
+PrefabName = Prowler_TW
+Enable = true
+SpawnMaxMultiplier = 1
+GroupSizeMinMultiplier = 1
+GroupSizeMaxMultiplier = 1
+SpawnFrequencyMultiplier = 1
+
+[GOBLINMAGE_TW]
+PrefabName = GoblinMage_TW
+Enable = true
+SpawnMaxMultiplier = 1
+GroupSizeMinMultiplier = 1
+GroupSizeMaxMultiplier = 1
+SpawnFrequencyMultiplier = 0.85
+
+[CORRUPTEDDVERGERMAGE_TW]
+PrefabName = CorruptedDvergerMage_TW
+Enable = true
+SpawnMaxMultiplier = 1
+GroupSizeMinMultiplier = 1
+GroupSizeMaxMultiplier = 1
+SpawnFrequencyMultiplier = 0.85
+
+[SUMMONEDSEEKER_TW]
+PrefabName = SummonedSeeker_TW
+Enable = true
+SpawnMaxMultiplier = 1
+GroupSizeMinMultiplier = 1
+GroupSizeMaxMultiplier = 1
+SpawnFrequencyMultiplier = 0.85

```

---


## Changed Files List

| Status | Category | File | Summary |
|--------|----------|------|--------|
| Modified | Azumatt Mods | `Azumatt.AzuCraftyBoxes.cfg` | +15, -51 changes |
| Modified | Azumatt Mods | `Azumatt.FactionAssigner.cfg` | +1, -30 changes |
| Modified | Creature Config | `CreatureConfig_Bosses.yml` | +18, ~9 changes |
| Modified | Creature Config | `CreatureConfig_Creatures.yml` | +4 changes |
| Modified | Custom Raids | `custom_raids.cfg` | ~2 changes |
| Modified | Custom Raids | `custom_raids.raids.cfg` | -18 changes |
| Modified | Custom Raids | `custom_raids.supplemental.deathsquitoseason.cfg` | +23, -819 changes |
| Modified | Custom Raids | `custom_raids.supplemental.ragnarok.cfg` | +148, -819 changes |
| Modified | Drop That | `drop_that.cfg` | ~1 changes |
| Modified | Drop That | `drop_that.character_drop.cfg` | +693, -870 changes |
| Modified | Drop That | `drop_that.character_drop.elite_additions.cfg` | +420, -870 changes |
| Modified | Drop That | `drop_that.drop_table.cfg` | -357 changes |
| Modified | Enchantment System | `ValheimEnchantmentSystem/kg.ValheimEnchantmentSystem.cfg` | ~2 changes |
| Modified | Enchantment System | `kg.ValheimEnchantmentSystem.cfg` | No changes detected |
| Modified | EpicLoot | `randyknapp.mods.epicloot.cfg` | No changes detected |
| Modified | EpicMMO | `WackyMole.EpicMMOSystem.cfg` | ~29 changes |
| Modified | Item Config | `ItemConfig_Base.yml` | -39 changes |
| Modified | Mushroom Monsters | `horemvore.MushroomMonsters.cfg` | +2, -72 changes |
| Modified | Other | `EpicLoot/patches\RelicHeimPatches\AdventureData_Bounties_RelicHeim.json` | +20, -2 changes |
| Modified | Other | `EpicLoot/patches\RelicHeimPatches\MagicEffects_RelicHeim.json` | +1, -13 changes |
| Modified | Other | `EpicLoot/patches\RelicHeimPatches\zLootables_CreatureDrops_RelicHeim.json` | +2, -1, ~3 changes |
| Modified | Other | `EpicLoot/patches\RelicHeimPatches\zLootables_TreasureLoot_RelicHeim.json` | +1, ~3 changes |
| Modified | Other | `_RelicHeimFiles/Drop,Spawn_That/RockPiles/drop_that.drop_table.PileOres.cfg` | -2 changes |
| Modified | Other | `_RelicHeimFiles/Drop,Spawn_That/RockPiles/spawn_that.world_spawners.PileOres.cfg` | ~11 changes |
| Modified | Other | `_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Bosses.cfg` | ~26 changes |
| Modified | Other | `_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.GoldTrophy.cfg` | ~9 changes |
| Modified | Other | `_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Wizardry.cfg` | ~1 changes |
| Modified | Other | `_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.zBase.cfg` | +1, -116, ~1 changes |
| Modified | Other | `_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.Chests.cfg` | +296, -33, ~1 changes |
| Modified | Other | `_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.EpicLootChest.cfg` | ~17 changes |
| Modified | Other | `_RelicHeimFiles/Drop,Spawn_That/spawn_that.local_spawners.Locals.cfg` | -12, ~27 changes |
| Modified | Other | `_RelicHeimFiles/Drop,Spawn_That/spawn_that.local_spawners.LocalsDungeons.cfg` | -12, ~1 changes |
| Modified | Other | `_RelicHeimFiles/Drop,Spawn_That/spawn_that.spawnarea_spawners.PilesNests.cfg` | ~15 changes |
| Modified | Other | `_RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zBase.cfg` | ~23 changes |
| Modified | Other | `_RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zBossSpawns.cfg` | ~8 changes |
| Modified | Other | `_RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zVanilla.cfg` | ~32 changes |
| Modified | Other | `_RelicHeimFiles/Raids/custom_raids.supplemental.MonstrumDNRaids.cfg` | ~21 changes |
| Modified | Other | `_RelicHeimFiles/Raids/custom_raids.supplemental.MonstrumRaids.cfg` | ~13 changes |
| Modified | Other | `_RelicHeimFiles/Raids/custom_raids.supplemental.MoreRaids.cfg` | ~33 changes |
| Modified | Other | `_RelicHeimFiles/Raids/custom_raids.supplemental.VanillaRaids.cfg` | ~44 changes |
| Modified | Other | `_RelicHeimFiles/Raids/custom_raids.supplemental.WizardryRaids.cfg` | ~11 changes |
| Modified | Other | `wackysDatabase/Items\_RelicHeimWDB2.0\Food\Feasts\Item_FeastAshlands.yml` | ~2 changes |
| Modified | Other | `wackysDatabase/Items\_RelicHeimWDB2.0\Food\Feasts\Item_FeastMistlands.yml` | ~2 changes |
| Modified | Other | `wackysDatabase/Items\_RelicHeimWDB2.0\Food\Item_SerpentMeatCooked.yml` | ~2 changes |
| Modified | Other | `wackysDatabase/Items\_RelicHeimWDB2.0\Food\Item_SerpentStew.yml` | ~2 changes |
| Modified | Plant Everything | `advize.PlantEverything.cfg` | ~12 changes |
| Modified | Smart Containers | `flueno.SmartContainers.cfg` | +45, -31 changes |
| Modified | Smoothbrain | `org.bepinex.plugins.blacksmithing.cfg` | ~9 changes |
| Modified | Smoothbrain | `org.bepinex.plugins.building.cfg` | ~6 changes |
| Modified | Smoothbrain | `org.bepinex.plugins.conversionsizespeed.cfg` | +18 changes |
| Modified | Smoothbrain | `org.bepinex.plugins.cooking.cfg` | +13, -30 changes |
| Modified | Smoothbrain | `org.bepinex.plugins.creaturelevelcontrol.cfg` | ~12 changes |
| Modified | Smoothbrain | `org.bepinex.plugins.exploration.cfg` | +9, -30 changes |
| Modified | Smoothbrain | `org.bepinex.plugins.farming.cfg` | ~7 changes |
| Modified | Smoothbrain | `org.bepinex.plugins.foraging.cfg` | ~5 changes |
| Modified | Smoothbrain | `org.bepinex.plugins.groups.cfg` | +12, -30 changes |
| Modified | Smoothbrain | `org.bepinex.plugins.lumberjacking.cfg` | ~2 changes |
| Modified | Smoothbrain | `org.bepinex.plugins.mining.cfg` | ~2 changes |
| Modified | Smoothbrain | `org.bepinex.plugins.packhorse.cfg` | ~2 changes |
| Modified | Smoothbrain | `org.bepinex.plugins.ranching.cfg` | +7, -30 changes |
| Modified | Smoothbrain | `org.bepinex.plugins.sailing.cfg` | +56, ~11 changes |
| Modified | Smoothbrain | `org.bepinex.plugins.tenacity.cfg` | ~2 changes |
| Modified | Spawn That | `spawn_that.cfg` | +19, -292 changes |
| Modified | Spawn That | `spawn_that.local_spawners_advanced.cfg` | -189, ~17 changes |
| Modified | Spawn That | `spawn_that.simple.cfg` | +336, -292 changes |
| Modified | Spawn That | `spawn_that.spawnarea_spawners.cfg` | -127, ~1 changes |
| Modified | Spawn That | `spawn_that.world_spawners_advanced.cfg` | +350, -268, ~9 changes |

## Information Items

| Type | Description | Summary |
|------|-------------|--------|
| System | Unmapped other Files | Found 5127 other files not mapped: Azumatt.AzuClock.cfg, Azumatt.AzuCraftyBoxes.yml, Azumatt.AzuExtendedPlayerInventory.cfg and 5124 more |
| System | Unmapped shudnal Files | Found 21 shudnal files not mapped: shudnal.Seasons\Cache settings\Defaults\Color positions.json, shudnal.Seasons\Cache settings\Defaults\Color ranges.json, shudnal.Seasons\Cache settings\Defaults\Colors.json and 18 more |
| System | Unused Backup Files | Found 90 backup files not mapped: EpicMMOSystembackup\Default.json, EpicMMOSystembackup\Jewelcrafting.json, EpicMMOSystembackup\Monstrum_DeepNorth.json, EpicMMOSystembackup\Therzie_Monstrum.json, EpicMMOSystembackup\Therzie_Wizardry.json and 85 more |


---

*Report generated by Config Change Tracker*
*Base RelicHeim version: 5.4.10*
*Note: Only changed files are shown. Files identical to backup or with no backup are filtered out.*
