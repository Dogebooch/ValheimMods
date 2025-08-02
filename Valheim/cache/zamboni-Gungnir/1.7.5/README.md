## Brief

**Gungnir** is an enhancement suite for the in-game console! It provides a brand new aesthetic, helpful commands, and for other programmers who want to contribute, a very easy way to add new commands!

Check it out on nexus mods, there's usually more discussion there, and it's easier for me to communicate with users! https://www.nexusmods.com/valheim/mods/1921

## Features

-   New color scheme for the console and all Gungnir-related output.
-   Popup hints to show you how to use the command you're typing, and highlight which parameter you're entering.
-   Console history scrolling, up to 1,000 lines.
-   Many new commands.
-   Chain multiple commands together (e.g., `/fly 1;/creative;/god`)
-   Create custom names for commands or sequences of commands with /alias.
-   Bind commands to any key, right from the console, with /bind.
-   Helpful terrain modification and restoration commands.
-   …and more on the way!

Some of you may use or know of SkToolbox, and Gungnir is quite similar, but seeing as the author stated it is no longer maintained, I thought I'd start work on my own console instead. I will not be adding things such as the on-screen menu or enemy detection features, as I feel those are out of the scope of what this mod should be.
This mod is obviously incompatible with SkToolbox and anything that may do something similar.

## Commands

```
/alias <String name> <String[] commandText>
Create a shortcut or alternate name for a command, or sequence of commands.

/bind <String keyCode> <String[] commandText>
Bind a console command to a key. See the Unity documentation for KeyCode names.

/butcher [Decimal radius = 50f] [Boolean killTamed = false]
Kills all living creatures within a radius (meters), excluding players.

/clear
Clears the console's output.

/creative [Boolean enabled = none]
Toggles creative mode, which removes the need for resources.

/echo <String[] values>
Shout into the void.

/fly [Boolean noCollision = false]
Toggles the ability to fly. Can also disable collisions with the second argument.

/ghost [Boolean enabled = none]
Toggles ghost mode. Prevents hostile creatures from detecting you.

/give <String itemName> [Number amount = 1] [Player player = none] [Number level = 1]
Give an item to yourself or another player.

/god [Boolean enabled = none]
Toggles invincibility.

/goto <Player player>
Teleport yourself to another player.

/heal
Heal all of your wounds.

/help [String commandOrPageNum = none]
Prints the command list, or looks up the syntax of a specific command. Also accepts a page number, in case of many commands.

/listaliases [String alias = none]
List all of your custom aliases, or check what a specific alias does.

/listbinds [String keyCode = none]
List all of your custom keybinds, or check what an individual keycode is bound to.

/listitems [String itemName = none]
List every item in the game, or search for one that contains your text.

/listportals
List every portal tag.

/listprefabs [String prefabName = none]
List every prefab in the game, or search for one that contains your text.

/listskills
List every available skill in the game.

/listweather
Get a list of all available weather types.

/nomana [Boolean enabled = none]
Toggles infinite eitr (mana).

/nores [Boolean enabled = none]
Toggle building restrictions. Allows you to place objects even when the preview is red.

/noslide [Boolean enabled = none]
Toggle the ability to walk up steep angles without sliding.

/nostam [Boolean enabled = none]
Toggles infinite stamina.

/nosup [Boolean enabled = none]
Toggle the need for structural support.

/pos
Print your current position as XZY coordinates. (XZY is used for tp command.)

/puke
Clears all food buffs and makes room for you to eat something else.

/removedrops [Decimal radius = 50f]
Clears all item drops in a radius (meters).

/repair
Repairs every item in your inventory.

/repairbuilds [Decimal radius = 50f]
Repairs all nearby structures within a radius (meters).

/seed
Print the seed used by this world.

/setmaxweight [Decimal maxWeight = 300f]
Set your maximum carry weight.

/setskill <String skillName> <Number level>
Set the level of one of your skills.

/spawn <String prefab> [Number levelOrQuantity = 1]
Spawn a prefab/creature/item. If it's a creature, levelOrQuantity will set the level, or if it's an item, set the stack size.

/spawntamed <String creature> [Number level = 1]
Spawn a tamed version of a creature.

/tame [Decimal radius = 10f]
Pacify all tameable creatures in a radius.

/time <Decimal time>
Overrides the time of day for you only (0 to 1 where 0.5 is noon). Set to a negative number to disable.

/tlevel [Decimal radius = 10f]
Level the terrain in a radius.

/tlower [Decimal radius = 10f] [Decimal depth = 1f] [Decimal strength = 0.01f]
Lower the terrain in a radius by some amount. Strength values closer to 0 make the terrain edges steep, while values further from 0 make them smoother.

/tp <Decimal x> <Decimal z> [Decimal y = none]
Teleport to specific coordinates. The Y value is optional. If omitted, will attempt to find the best height to put you at automagically.

/tpaint [Decimal radius = 5f] [String paintType = "reset"]
Paint terrain in a radius. Available paint types are: dirt, paved, cultivate, and reset.

/traise [Decimal radius = 10f] [Decimal height = 1f] [Decimal strength = 0.01f]
Raise the terrain in a radius by some amount. Strength values closer to 0 make the terrain edges steep, while values further from 0 make them smoother.

/treset [Decimal radius = 10f]
Reset all terrain modifications in a radius.

/tshape <String shape>
Choose the shape of terrain modifications with 'circle' or 'square'.

/tsmooth [Decimal radius = 10f] [Decimal strength = 0.5f]
Smooth terrain in a radius with some strength. Higher strengths mean more aggressive smoothing.

/unalias <String alias>
Remove an alias you've created.

/unaliasall <Boolean confirm>
Removes all of your custom command aliases. Requires a true/1/yes as parameter to confirm you mean it.

/unbind <String keyCode>
Removes a custom keybind.

/unbindall <Boolean confirm>
Unbinds ALL of your Gungnir-related keybinds. Requires a true/1/yes as parameter to confirm you mean it.

/weather <String weatherType>
Overrides the weather for you only. Use -1 to clear the override.
```

## Usage

Press F5 and type /help to get a nice overview of what commands you can run. Each command will give you a list of arguments that are expected, what type it should be, and if it is required or not.

For example, the help text for /give says: /give \<String itemName\> \[Number amount=1\] \[Player player=none\] \[Number level=1\]
This says that there are 4 possible arguments to this command, and 3 are optional.
Any argument surrounded by \[square brackets\] is **optional**, while anything in \<chevrons\> is **required**.
The value after the equals sign tells you what the default will be. Sometimes **none** will be shown if the default value can't be described well, but that should typically only show for Player name arguments. If a player argument defaults to none, it means it will choose you by default.

## Possible argument types

| Type      | Possible values                                                                                                                            |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| String    | Any text you want.                                                                                                                         |
| Number    | A whole number, no fractions or decimals allowed.                                                                                          |
| (+)Number | A positive whole number.                                                                                                                   |
| Decimal   | A number with as many decimal places as you'd like.                                                                                        |
| Boolean   | A true/false value. There are only four things you can type that mean true: "yes", "1", "on", and "true". Everything else counts as false. |
| Player    | The name of a player currently on the server.                                                                                              |

Any of these can also have square brackets on the end, like String[], which means that, starting from that parameter, everything you type from then on will be used as the argument.

## Command Chaining/Aliases and Binds

Commands can be stitched together to execute them all in one go.
To execute multiple commands in sequence, separate them with a semicolon. Example:

`/god;/ghost;/nostam;/nores;/fly true`

This feature pairs well with the /bind command, allowing you to make easy toggles or quick access to utilities. You will need to use quotes around the command being bound to avoid confusing the command chaining. Example:

`/bind k "/butcher;/removedrops 100"`

Similarly, when creating an alias, if you intend to create an alias that runs multiple commands, please be sure to surround your command set with double quotes like the above example.

It's hard to tell whether you want to run multiple commands, or whether your alias/bind is supposed to include the extra commands. Using double quotes lets the mod know you want it to take everything in the quotes as the argument value.

## To-Do

-   More commands.
-   Auto-run commands when joining a game.
-   Better auto-complete. The game's built-in autocomplete system is pretty bad, and only supports auto-complete on the first argument. I have a plan to extend it to work for every argument of a command, and show the command format as you're typing.
-   Framework to allow mods to register their commands with Gungnir instead of the base game.
-   Ability to select text in the console.
-   More customization options (color scheme selection, maybe? Font size control, etc.)

## Installation

This mod requires BepInEx, and is installed the same as any other BepInEx mod. Place it in your plugins folder.
Please make sure the version of BepInEx you install also includes Harmony. If it doesn't please install that as well.

## Contributing/Bug Reporting

If you'd like to add your own command, you found a bug, or just want to browse the source code, head over to [Gungnir's GitHub page](https://github.com/zambony/Gungnir) and get involved!