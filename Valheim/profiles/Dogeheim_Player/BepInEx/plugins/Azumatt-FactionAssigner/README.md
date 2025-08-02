# Description

## Mod that allows you to (via YAML config) change the factions of the creatures in the game. Yaml file is located in BepInEx/config/Azumatt.FactionAssigner.yml

`Version checks with itself. If installed on the server, it will kick clients who do not have it installed.`

`This mod uses ServerSync, if installed on the server and all clients, it will sync all configs to client`

`This mod uses a file watcher. If the configuration file is not changed with BepInEx Configuration manager, but changed in the file directly on the server, upon file save, it will sync the changes to all clients.`

Made by request of Majestic in my discord a.k.a `majestic._.`

### Please note:

Should you need to see the factions or prefab names of characters in your game, you can turn on the logging of them in
the config file (`Azumatt.FactionAssigner.cfg`). By the time you reach the main menu, it will be logged to the console.

---

<details>
<summary><b>Installation Instructions</b></summary>

***You must have BepInEx installed correctly! I can not stress this enough.***

### Manual Installation

`Note: (Manual installation is likely how you have to do this on a server, make sure BepInEx is installed on the server correctly)`

1. **Download the latest release of BepInEx.**
2. **Extract the contents of the zip file to your game's root folder.**
3. **Download the latest release of FactionAssigner from Thunderstore.io.**
4. **Extract the contents of the zip file to the `BepInEx/plugins` folder.**
5. **Launch the game.**

### Installation through r2modman or Thunderstore Mod Manager

1. **Install [r2modman](https://valheim.thunderstore.io/package/ebkr/r2modman/)
   or [Thunderstore Mod Manager](https://www.overwolf.com/app/Thunderstore-Thunderstore_Mod_Manager).**

   > For r2modman, you can also install it through the Thunderstore site.
   ![](https://i.imgur.com/s4X4rEs.png "r2modman Download")

   > For Thunderstore Mod Manager, you can also install it through the Overwolf app store
   ![](https://i.imgur.com/HQLZFp4.png "Thunderstore Mod Manager Download")
2. **Open the Mod Manager and search for "FactionAssigner" under the Online
   tab. `Note: You can also search for "Azumatt" to find all my mods.`**

   `The image below shows VikingShip as an example, but it was easier to reuse the image.`

   ![](https://i.imgur.com/5CR5XKu.png)

3. **Click the Download button to install the mod.**
4. **Launch the game.**

</details>

<br>
<br>

<details>
<summary><b>Example Yaml</b></summary>
<br/>

```yaml
Abomination: Undead
Bat: MountainMonsters
Blob: Undead
BlobElite: Undead
BlobTar: Undead
Boar: ForestMonsters
Boar_piggy: ForestMonsters
Bonemass: Boss
Chicken: ForestMonsters
Deathsquito: PlainsMonsters
Deer: ForestMonsters
Dragon: Boss
Draugr: Undead
Draugr_Elite: Undead
Draugr_Ranged: Undead
Dverger: Dverger
DvergerMage: Dverger
DvergerMageFire: Dverger
DvergerMageIce: Dverger
DvergerMageSupport: Dverger
DvergerTest: Dverger
Eikthyr: Boss
Fenring: MountainMonsters
Fenring_Cultist: MountainMonsters
Fenring_Cultist_Hildir: MountainMonsters
Fenring_Cultist_Hildir_nochest: MountainMonsters
gd_king: Boss
Ghost: Undead
Gjall: MistlandsMonsters
Goblin: PlainsMonsters
GoblinArcher: PlainsMonsters
GoblinBrute: PlainsMonsters
GoblinBruteBros: PlainsMonsters
GoblinBruteBros_nochest: PlainsMonsters
GoblinBrute_Hildir: PlainsMonsters
GoblinKing: Boss
GoblinShaman: PlainsMonsters
GoblinShaman_Hildir: PlainsMonsters
GoblinShaman_Hildir_nochest: PlainsMonsters
Greydwarf: ForestMonsters
Greydwarf_Elite: ForestMonsters
Greydwarf_Shaman: ForestMonsters
Greyling: ForestMonsters
Hare: AnimalsVeg
Hatchling: MountainMonsters
Hen: ForestMonsters
Hive: Boss
Leech: Undead
Leech_cave: Undead
Lox: PlainsMonsters
Lox_Calf: PlainsMonsters
Mistile: Dverger
Neck: ForestMonsters
Seeker: MistlandsMonsters
SeekerBrute: MistlandsMonsters
SeekerBrood: MistlandsMonsters
SeekerQueen: Boss
Serpent: SeaMonsters
Skeleton: Undead
Skeleton_Friendly: Players
Skeleton_Hildir: Undead
Skeleton_Hildir_nochest: Undead
Skeleton_NoArcher: Undead
Skeleton_Poison: Undead
StoneGolem: ForestMonsters
Surtling: Demon
TentaRoot: Boss
TheHive: MistlandsMonsters
Tick: MistlandsMonsters
Troll: ForestMonsters
TrainingDummy: Undead
Ulv: MountainMonsters
Wolf: MountainMonsters
Wolf_cub: MountainMonsters
Wraith: Undead
```

</details>

`Feel free to reach out to me on discord if you need manual download assistance.`

# Author Information

### Azumatt

`DISCORD:` Azumatt#2625

`STEAM:` https://steamcommunity.com/id/azumatt/

For Questions or Comments, find me in the Odin Plus Team Discord or in mine:

[![https://i.imgur.com/XXP6HCU.png](https://i.imgur.com/XXP6HCU.png)](https://discord.gg/Pb6bVMnFb2)
<a href="https://discord.gg/pdHgy6Bsng"><img src="https://i.imgur.com/Xlcbmm9.png" href="https://discord.gg/pdHgy6Bsng" width="175" height="175"></a>