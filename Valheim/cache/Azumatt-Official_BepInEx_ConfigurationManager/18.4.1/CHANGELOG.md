> `v18.4.1`
> - Fixed decimal for Scandinavian and similar Culture by [@zzzbatmand](https://github.com/zzzbatmand) in [#105](https://github.com/BepInEx/BepInEx.ConfigurationManager/pull/105)
> - Catch exceptions during settings search by [@RikkiBalboa](https://github.com/RikkiBalboa) in [#108](https://github.com/BepInEx/BepInEx.ConfigurationManager/pull/108)
>
> Full Changelog: [v18.4...v18.4.1](https://github.com/BepInEx/BepInEx.ConfigurationManager/compare/v18.4...v18.4.1)
>
> `v18.4`
> - Keep original category order by @ManlyMarco in [#102](https://github.com/BepInEx/BepInEx.ConfigurationManager/pull/102)
>
> Full Changelog: [v18.3.1...v18.4](https://github.com/BepInEx/BepInEx.ConfigurationManager/compare/v18.3.1...v18.4)
>
> `v18.3.1`
> - Harden against null plugin Metadata
> - Add 'Known Issues' section to README.md by @ManlyMarco in [#91](https://github.com/BepInEx/BepInEx.ConfigurationManager/pull/91)
>
> Full Changelog: [v18.3...v18.3.1](https://github.com/BepInEx/BepInEx.ConfigurationManager/compare/v18.3...v18.3.1)
>
> `v18.3`
> - Fixed a bug that caused an exception if DLLs that failed to load were mixed in by @takahiro0327 in #84
> - Do not throw ArgumenNullException in ConfigSettingEntry.GetAcceptedValues by @MrAgeo in #89
>
> `v18.2`
> - 67b4eef @ManlyMarco Improve Color settings: Dec/Hex numbers, Visualize alpha
> - 9047ead @ManlyMarco Add ConfigurationManager.IsWindowFullscreen
>
> `v18.1` 
> - Improve Color settings: Dec/Hex numbers, Visualize alpha
> - Add ConfigurationManager.IsWindowFullscreen
>
> `v18.0.1` 
> - [8fc53a4](https://github.com/BepInEx/BepInEx.ConfigurationManager/commit/8fc53a4820624052794fd7cd9d367d01a0101aec) @ManlyMarco Fixed not detecting plugins if the `HideManagerGameObject` setting is set to `true` in BepInEx config.
Full Changelog: [v18.0...v18.0.1](https://github.com/BepInEx/BepInEx.ConfigurationManager/compare/v18.0...v18.0.1)
>
> `v18.0.0` 
> - ConfigurationManager window can now be dragged to move it to the side of the screen. After being dragged the window will switch to a background mode where it will stay open while letting you freely interact with the game.
> - `Warning: At least BepInEx v5.4.20 is required!`