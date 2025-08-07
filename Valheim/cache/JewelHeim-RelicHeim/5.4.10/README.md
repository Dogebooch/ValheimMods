<details>
<summary><b>READ ME!</b></summary>
<br/>

### Getting Started
  - Make the Enchanting Table as soon as possible by gathering the required materials.
  - You will need Novus materials to do Novus Enchanting which will mainly be what you can only do in beginning
### Couple things to keep in mind
  - **__Find Haldor in BlackForest as soon as possible in order to do Maps, Bounties and buy materials to help enchant your items.__**
  - Small monsters aka Deer, Wolf etc will not drop enchanted loot 
  - Chests of any kind will not contain any enchanted loot but will contain magic materials to help with enchanting.
  - All small monsters will drop Novus Runestones, Shards or Dust
  - Elite creatures aka Trolls etc have a 15% chance of dropping enchanted loot
  - Bosses have 100% chance to drop loot
  - With the above mentioned, the rarities and amounts are nerfed to be balanced, sometimes you'll get something good and other times it will be trash, utilize the Enchanting Table to sacrifice those items to get materials back.
  - Majority of all non boss trophies when sacrificed will give Novus Reagent
  - In order to make higher tier magic materials you will need to use Essence which is bought from Haldor and upgrade the materials at the Enchanting Table
  - Augmenting the first effect requires Novus Dust and Reagent of that rarity, augmenting any other effects will also require Tokens which are obtained from doing Maps and Bounties from Haldor.
### What can be found in Chests in the world.
- Dust, Runestone, Shard, Essence of any rarity
  - Rarity is weighted with Novus being most common and Relic being Rare.
### Which creatures can drop enchanted loot?
As mentioned only Elite type creatures of each biome will have a 15% to drop loot when killed
  - Fox [ Meadows ]
  - Troll, GreydwarfBrute [ BlackForest ]
  - DraugrElite, Abomination, Wraith, HelWraith [ Swamp ]
  - Fenring, Cultist, StoneGolem [ Mountain ]
  - Lox, GoblinBrute, Prowler [ Plains ]
  - SeekerSoldier, Gjall [ Mistlands ]
  - FallenValkyrie, BonemawSerpent,Morgen [ Ashlands ]
</details>

#

# What is RelicHeim?
- This modpack is different from all the other modpacks on thunderstore, my modpack are meant for ANYONE to play and it comes pre-configured based on my vision, majority of all modpacks on thunderstore are meant for their server and doesn't come with any configuration.
- This modpack uses EpicLoot and is balanced to make players not feel over powered, it comes with medium to hard difficulty based on player style.
  - All magiceffect values and set values have been nerfed
  - The magiceffects have been changed to be only applied on specific equipment and some you have to choose between one effect or the other 
    - Ex: `health regen or regen per tick`
  - Some magiceffects have been disabled due to being to overpowered or cause issues
  - EpicLoot in this modpack is drastically different compared to default, but feel free to ask questions in my discord
- EpicLoot: This modpack is designed around players enchanting their own gear so creatures will not be dropping massive amounts of loot, you will need to find Haldor to help with further enchanting.
- Only bosses and elite mobs aka trolls etc will have a chance at dropping enchanted loot, this loot is usually not the best and is better to sacrifice it to get materials in return to enchant yourself.
- More legendary sets and single legendary sets added to give a more different playstyle
- Notes:
  - 1: If playing with more than 2 players, please adjust the CLLC settings for HP/DMG per player to your liking
  - 2: EpicLoot patches will not work with this modpack.
  - 3: DO NOT CHANGE WORLD MODIFIERS FOR DIFFICULTY.
    - Why? because my modpack is tested and balanced around default difficulty in valheim and enhanced with CLLC mod, if you increase with modifiers don't complain it's too hard.

#
<details>
<summary><b>What is Incompatible</b></summary>
<br/>

## Incompatible
- ValheimPlus
- RTMN
- JewelHeim
- Any other modpacks
</details>

#
<details>
<summary><b>What mods are ok to Disable?</b></summary>
<br/>

### These mods are ok to disable:
- ReliableBlock
- PressurePlate
- Any of Smoothbrains mods that adds new "Skills" aka Mining etc.
- Groups
- SmartSkills
- Backpacks
- TargetPortal
- NoSmokeStayLit
- WackyEpicMMOSystem
- FishTrap
</details>

#
<details>
<summary><b>Experiencing low FPS etc?</b></summary>
<br/>

- If you're experiencing issues, you can try this to help boost your fps a bit more as it's been proven to help.
  - Quit the game
  - Open Steam and go to your library and right click on Valheim->Manage->Browse Local File
  - Open Folder `valheim_Data`
  - Open file `boot.config`
  - Add these lines to the file
    - gfx-enable-gfx-jobs=1
    - gfx-enable-native-gfx-jobs=1
    - vr-enabled=0
    - scripting-runtime-version=latest

</details>

#

<details>
<summary><b>How to install this modpack</b></summary>
<br/>

- Download and Install `R2modman`, please don't use `thunderstore mod manager`.
- Select Valheim in R2modman and create a new profile (name it whatever you want)
- Go to Online tab and search for RelicHeim and click download
- Launch `Start Modded` and you're good to go.
- [How to install R2modman (Video)](https://www.youtube.com/watch?v=L9ljm2eKLrk)

</details>

#

<details>
<summary><b>Installing on Server</b></summary>
<br/>

- Grab the contents inside your `config` folder and place them inside your servers `config` folder
- Grab the contents inside your `plugins` folder and place them inside your servers `plugins` folder
- Grab the contents inside your `patchers` folder and place them inside your servers `patchers` folder
* This modpack uses "ThisGoesHere" to remove, move or clean up specific files.
* If you have issues on server being different then client, its probably due to not having this mod on your server
* Make sure content inside "Patchers" folder is also installed on your server.
* I would recommend making a clean profile, install RelicHeim, start game so all files are loaded, then copy **_plugins, patchers, configs_** to your server.

If you're getting the `Mod must not be installed` when trying connect to your server then you didn't add the mod(s) correctly to your server or BepinEx isnt enabled on your server
- Make sure your server is OFF before doing any of the below.
- Check your server provider and enable or install `BepinEx` from your provider
└> __Ex: DatHost- Under `Mods & Plugins` click Individual Installation and enable `BepinEx`__
- Download and Install `FileZilla Client` on your computer. <https://filezilla-project.org/>
- Open Filezilla and connect to your server provider via FTP, you'll need to check where this address is since every provider has it located differently and we cant help you find that.
└> __Ex: DatHost- Under `FileManager` at the bottom will show FTP information__
- Once connected to your provider if you see BepinEx folder with all necessary folders then you did it correctly and now simply add your plugins,patchers,config files to the server
- Note: Do NOT install mods through your providers thunderstore integration or whatever they have, ALWAYS manually install your mods to your server through FileZilla.

</details>

## Support
<p align="center">Like my work and want to support what I do?</a>
<p align="center"><a href="https://www.buymeacoffee.com/ZQnHBcxknE"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-violet.png" width="350" height="75"></a>

## My Other Modpack
<p align="left"><a href="https://valheim.thunderstore.io/package/JewelHeim/JewelHeim/"><img src="https://imgur.com/Uu7rlTQ.png" width="150" height="150"></a>
<a href="https://valheim.thunderstore.io/package/JewelHeim/Road_To_Muspelheim_and_Niflheim/"><img src="https://imgur.com/rMu13Yp.png" width="150" height="150"></a></p>

## Discord Server
### Please join my discord for any support
<p align="left"><a href="https://discord.gg/6HMJ6uqmKJ"><img src="https://imgur.com/LaSb7Gu.png" width="200" height="200"></a>