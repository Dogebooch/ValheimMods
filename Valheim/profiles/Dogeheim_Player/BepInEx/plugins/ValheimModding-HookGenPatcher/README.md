# HookGenPatcher

Generates [MonoMod.RuntimeDetour.HookGen's](https://github.com/MonoMod/MonoMod) `MMHOOK` file during the [BepInEx](https://github.com/BepInEx/BepInEx) preloader phase. 

Installation:
Put the config folder in the `BepInEx\` folder.
Put the patchers folder in the `BepInEx\` folder.

**This project is not officially linked with BepInEx nor with MonoMod.**

Latest Changelog :

Remove assembly_steamworks.dll from the config as it can be missing due to valheim also existing on the microsoft store