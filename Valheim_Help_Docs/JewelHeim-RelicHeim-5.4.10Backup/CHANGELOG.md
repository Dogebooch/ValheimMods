#
```yaml
📌 Changelog for RelicHeim v5.4.10 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Modified some patch files to stop throwing warings when logging enabled.
- BloodLust will now only appear as an available effect when augmenting if you have lifesteal.
- AttackHealthUse will now properly appear when you have bloodlust on your weapon.
- Slightly increase the values for AttackHealthUse effect
- To help make lifesteal bit better on one-handed weapons, you can now enchant shields with lifesteal
- Lifesteal values were adjusted.
  ➼ Please let me know if this change makes lfiesteal too strong.
- Several values and increments for effects were adjusted
# DropThat:
- Disabled AlwaysAutoStack in the config to prevent issues with items
- Items will not drop in stacks.
  ➼ This is vanillas default behaviour
# Other:
- Trolls will now drop Rubys instead of coins
- Goblin family will now drop AmberPearls instead of coins
- Dverger family will now drop Amber instead of coins 
  ➼ The above are to match the default coins values when dropped (or more)
  ➼ This is to prevent massive amounts of coins dropping or cause lag.
# New Mod:
- Azumatt-Azus_UnOfficial_ConfigManager-18.4.1
  ➼ Client mod.
# Removed Mod:
- Azumatt-TrueInstantLootDrop-1.0.2
  ➼ Causing issues with DropThat in multiplayer with item stacks and not following loot tables.
  ➼ Remove TrueInstantLootDrop on your server if you're not using it anymore.
```
*-If you're playing on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
!Configs:
- Folder: _RelicHeimFiles
- Folder: EpicLoot [Don't copy YOUR "BountySaves" folder]
- File: drop_that.cfg
```
*-If you're playing on a server, update the plugin(s) folder on your server*
```yaml
!Plugins:
- None
```
#

<details>
<summary><b>Changelog History v5.3.0+ [Bog Witch Update]</b> (<i>click to expand</i>)</summary>
<br/>

#
```yaml
📌 Changelog for RelicHeim v5.4.9 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Fixed some errors in patches.
- Bounties have been changed.
  ➼ Each bounty has 3 difficulties, No Token, Iron Token and Gold Token
  ➼ All bounty coin rewards were adjusted for each difficulty
  ➼ All bounty token rewards were adjusted for each difficulty
- Quickdraw enchant will be fixed in next EpicLoot update, Crossbows will work with it as well.
# ToneDowntheTwang:
- Adjusted draw time on bows when at level 100
# Other
- Adjusted base draw time for Bows
- Adjusted base draw time for Greatbows [Excluding Moder G.Bow]
- Slightly lowered the base reload speed of Crossbows.
# New Mod:
- WackyMole-ToneDowntheTwang-1.0.0
  ➼ If playing on server it needs to be added
```
*-If you're playing on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
!Configs:
- Folder: _RelicHeimFiles
- Folder: EpicLoot [Don't copy YOUR "BountySaves" folder]
- Folder: wackysDatabase
- File: WackyMole.Tone_Down_the_Twang.cfg
```
*-If you're playing on a server, update the plugin(s) folder on your server*
```yaml
!Plugins:
- WackyMole-Tone_Down_the_Twang
```
#
```yaml
📌 Changelog for RelicHeim v5.4.8 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Increased prices for all items in the gamble section.
- Adjusted what will appear on the Gamble section.
- Added missing Mistwalker to gamble section.
- Slightly increased the chances for elite creatures to drop enchanted loot.
# Other
- Raid files were updated with the new setting to help with raids sometimes not spawning anything.
- Adjusted the values in Tenacity a bit.
```
*-If you're playing on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
!Configs:
- Folder: _RelicHeimFiles
- Folder: EpicLoot [Don't copy YOUR "BountySaves" folder]
- File: org.bepinex.plugins.tenacity.cfg
```
*-If you're playing on a server, update these plugins on your server*
```yaml
!Plugins:
- Jotunn
- CustomRaids
```
#
```yaml
📌 Changelog for RelicHeim v5.4.7 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# Tenacity:
- Adjusted some values to balance with other mods that give reduced damage.
  ➼ If further adjustments are needed please provide feedback on it.
# SmartSkills:
- Weapon bonus xp back to default.
# EpicMMO:
- Added reset trophy to Haldors store.
# Other:
- Fixed a raid setting causing raids to not end when they should.
- New WishboneBackpack
- Changed WispPotion recipe to use Wisps over Demister to prevent taking Wisplight in inventory.
- Updated AzuCraftyBoxes.yml for backpack filters.
# NewMods:
- Smoothbrain-Tenacity
  ➼ If playing on server it needs to be added
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
!Configs:
- Folder: _RelicHeimFiles
- Folder: wackysDatabase
- File: Azumatt.AzuCraftyBoxes.yml
- File: Backpacks.Majestic.yml
- File: CreatureConfig_Bosses.yml
- File: org.bepinex.plugins.smartskills.cfg
- File: org.bepinex.plugins.tenacity.cfg
- File: WackyMole.EpicMMOSystem.cfg
```
*-If you're on a server, update these plugins on your server*
```yaml
!Plugins:
- Tenacity
- WackyEpicMMOSystem
```
#
```yaml
📌 Changelog for RelicHeim v5.4.6 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot
- Cleaned up and fixed materialconversion file.
- Can convert NovusRunestones in to NovusDust at the enchanting table.
- Can convert InfusedCrystals in to coins at the enchanting table.
- Cleaned up Zeta/Relic single set enchants to be more random.
# EpicMMO:
- Some updates to creatures.
# Other:
- none
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
!Configs:
- Folder: _RelicHeimFiles
- Folder: EpicLoot [Don't copy YOUR "BountySaves" folder]
- Folder: EpicMMOSystem
```
*-If you're on a server, update these plugins on your server*
```yaml
!Plugins:
- NONE
```
#
```yaml
📌 Changelog for RelicHeim v5.4.5 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot
- LeatherBelt now gives +25 weight
# WackysDatabase:
- 4 more skill type potions, that give you 5% increased skill exp gain and damage towards the specific skill. These are crafted at the MeadCauldron station.
  ➼ Swords/Knives/Clubs/Axes
# Other:
- Fixed raid spawning (Hopefully)
- Fixed Charred raid causing the monument from not despawning, it's now replaced with a charred warrior.
- Fixed bows having accuracy issues due to my dumbass uploading wrong files.
- Fixed missing Flametal drops
- Fixed SummonedTrolls having CLLC effects.
- Adjusted Fortress loot in Ashlands.
- Strong creatures in Ashlands will have a small chance to drop the Gemstones.
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
!Configs:
- Folder: _RelicHeimFiles
- Folder: wackysDatabase
- File: CreatureConfig_Bosses.yml
- File: CreatureConfig_Creatures.yml
```
*-If you're on a server, update these plugins on your server*
```yaml
!Plugins:
- NONE
```
#
```yaml
📌 Changelog for RelicHeim v5.4.4 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Added BurstShot and Eruptors to patches so theyre categorized correctly.
- Fixed some effects being applied incorrectly.
- Fixed Crossbows Skill enchant on the "Crossbow Master" Zeta/Relic item when enchanted.
- Added new Zeta/Relic item for Unarmed when enchanted.
- Fixed "ThornyEmbrace" being applied to BurstShot type weapons.
# WackysDatabase:
- I created 3 new skill type potions for now, they give you 5% increased skill exp gain and damage towards the specific skill. These are crafted at the MeadCauldron station.
  ➼ Unarmed
  ➼ Spears
  ➼ Polearms
# Other:
- Fixed some Monstrum bosses dropping more than one boss weapon.
- Campfires can now be placed on wood.
- Balanced summons damage.
- Moved WispPotion to MeadCauldron.
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
!Configs:
- Folder: _RelicHeimFiles
- Folder: EpicLoot [Don't copy YOUR "BountySaves" folder]
- Folder: wackysDatabase
- File: CreatureConfig_BiomeIncrease.yml
- File: CreatureConfig_Creatures.yml
- File: CreatureConfig_Wizardry.yml
- File: RandomSteve.BreatheEasy.cfg
```
*-If you're on a server, update these plugins on your server*
```yaml
!Plugins:
- NONE
```
#
```yaml
📌 Changelog for RelicHeim v5.4.3 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Adjustments to SecretStash prices.
- The SecretStash is now on a shorter cooldown and will have 2 random items on sale instead of 1. 
# BreatheEasy:
- Updated config due to update.
# WackysDatabase:
- The "Blood Drinker" and "Blood Thirster" weapon can now be upgraded to level 12.
 ➼ If these don't feel overpowered I will look in to the other boss weapons going past level 4, Please let me know how these feel.
# SmartSkills:
- Adjusted config values.
# Other:
- Changed all the values on Feast food making them slightly better, added Eitr to most Feasts.
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
!Configs:
- Folder: _RelicHeimFiles
- Folder: EpicLoot [Don't copy YOUR "BountySaves" folder]
- Folder: wackysDatabase
- File: org.bepinex.plugins.smartskills.cfg
- File: RandomSteve.BreatheEasy.cfg
```
*-If you're on a server, update these plugins on your server*
```yaml
!Plugins:
- BreatheEasy
```
#
```yaml
📌 Changelog for RelicHeim v5.4.2 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Slightly lowered the cost of Zeta and Relic Essence in the shop
- Removed Zeta and Relic Essence from the reduced price pool since the cost is now lowered.
- Lowered the cost of the Andvaranaut ring by half.
- Organized SecretStash by rarity.
- Adjusted Gamble chances and loot.
- Removed the yellow text on set pieces so it's easier to know if a piece is equipped.
# CLLC:
- Set default size of creatures per star back to default.
# PassivePowers:
- Slightly reduced the actives percentage for Bonemass and Yagluth to be in line with original values.
- Removed Bonus Fire Damage on yagluth due to causing every attack to add fire damage and active effect being way too strong.
 ➼ Added Eitr Regen Increase instead.
- Increased passive carry weight for Fader.
# BreathEasy:
- Turned on dust from destroying trees.
- Left on dust when killing creatures in case it gets fixed.
 ➼ These can be configured to your liking as usual, keep backups as mentioned. 
# Other:
- Reduced the amount of greydwarf eyes required for the wood portal.
- During raids, "Infused Crystals" will have a higher drop chance.
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
!Configs:
- Folder: _RelicHeimFiles
- Folder: EpicLoot [Don't copy YOUR "BountySaves" folder]
- Folder: wackysDatabase
- File: CreatureConfig_BiomeIncrease.yml
- File: CreatureConfig_Bosses.yml
- File: CreatureConfig_Creatures.yml
- File: org.bepinex.plugins.creaturelevelcontrol.cfg
- File: org.bepinex.plugins.passivepowers.cfg
- File: RandomSteve.BreatheEasy.cfg
```
*-If you're on a server, update these plugins on your server*
```yaml
!Plugins:
- no updates
```
#
```yaml
📌 Changelog for RelicHeim v5.4.1 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# BreatheEasy:
- Config Changes, This mod also removes a lot of the "dust" like creatures upon death, using the hoe etc.
  ➼ Smelters won't have infinite fuel
  ➼ Ovens won't have infinite fuel
  ➼ Until updated, Smelters and Ovens won't show press "E" on the coal insert but still works.
# Other:
- Fixed Backpack config file, I turned off "Auto Open Backpack" by mistake.
- NeckTail, SeekerAspic will no longer float due to a CLLC bug making them float in the air. will remove this entry in ItemConfig once its fixed.
- Updated CreatureConfig files.
- Updated EpicMMO file due to update.
# NewMods:
- RandomSteve-BreatheEasy-1.0.2
  ➼ Mod needs to be on Server
  ➼ This mod is replacing NoSmokeStayLit by TastyChickenLegs for performance reasons.
  ➼ Azumatt's NoDust series override's this mod. The patches that handle that will not run if Azumatt's NoDust series (or singular mods) is/are installed.
# RemovedMods:
- NoSmokeStayLit by TastyChickenLegs
  ➼ Uninstall after updating modpack, remove from your server as well.
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
!Configs:
- Folder: _RelicHeimFiles
- Folder: wackysDatabase
- File: CreatureConfig_Bosses.yml
- File: CreatureConfig_Creatures.yml
- File: CreatureConfig_Monstrum.yml
- File: CreatureConfig_Wizardry.yml
- File: ItemConfig_Base.yml
- File: org.bepinex.plugins.backpacks.cfg
- File: RandomSteve.BreatheEasy.cfg
- File: WackyMole.EpicMMOSystem.cfg
```
*-If you're on a server, update these plugins on your server*
```yaml
!Plugins:
- WackyEpicMMOSystem 
- BreatheEasy
- NoSmokeStayLit [Remove from server]
```
#
```yaml
📌 Changelog for RelicHeim v5.4.0 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Fixed QuickDraw values.
- Bounties with adds have coin rewards increased.
# ValheimEnchantmentSystem
- SkillOrbs no longer drop per player due to not being proximity based.
  ➼ Higher creatures level the better the chance of them dropping, Spawner type mobs are excluded.
# Other:
- Fixed WindRun potions movement speed.
- Increased the chances of valuables and enchanting items to drop during raids.
- Fixed WizardryBackpacks crafting station not being able to upgrade.
- Added Chitin to all mudpiles, chance is low to not reduce IronScrap from dropping.
- Adjusted SunkenCrypt chest loot.
  ➼ Added Chitin to loottable
  ➼ Removed all valuables but increased the amount of coins.
# RemovedMods:
- FishTrap.
# AddedMods:
- Azumatt-MouseTweaks
  ➼ Client Side Mod, doesn't need to be on server
- Azumatt-SaveCrossbowState
  ➼ Client Side Mod, doesn't need to be on server
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
!Configs:
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: wackysDatabase
- File: Backpacks.Majestic.yml
- File: Backpacks.Wizardry.yml
- File: CreatureConfig_Creatures.yml
- File: org.bepinex.plugins.backpacks.cfg
```
*-If you're on a server, update these plugins on your server*
```yaml
!Plugins:
- JsonDotNET
```
#
```yaml
📌 Changelog for RelicHeim v5.3.30 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Added missing items.
# ValheimEnchantmentSystem:
- Fixed SkillOrbs not dropping one per player via DropThat (Hopefully this time)
- Disabled SkillOrbs from dropping in config file of VES to avoid conflicts.
# FishTrap:
- Decided to add config to help make the trap better, if you have configured this already please be sure to make backup of your config
- Production Rate: 600s
- Chance to Catch: 100%
# Other:
- All creatures once tamed will revert to default size regardless of stars due to reports of having issues trying to ride tames.
- Removed the AncientShaman from spawning in the Elder fight.
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
!Configs:
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: ValheimEnchantmentSystem
- Folder: wackysDatabase
- File: CreatureConfig_Bosses.yml
- File: CreatureConfig_Creatures.yml
- File: CreatureConfig_Monstrum.yml
- File: CreatureConfig_Wizardry.yml
- File: RustyMods.FishTrap.cfg
```
*-If you're on a server, update these plugins on your server*
```yaml
!Plugins:
- SpawnThat
```
#
```yaml
📌 Changelog for RelicHeim v5.3.29 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# Other:
- Updated "Azumatt.AzuCraftyBoxes.yml" for "SmallerKiln" to only use Wood to match the default for Kiln in the file, If not using AzuCraftyBoxes, the SmallerKiln will take any wood. Delete it in the file if wish to use any wood.
- Lowered the size of Lox a bit more to help with riding due to the increase in size per star.
- Reverted the attack type change to the DeepNorth Fist weapons causing them to attack super fast, possible bug in actual weapons, if fixed ill change it back to dualknives attack type.
- Adjusted damage to all BurstShot and Eruptors, Angle to shoot should be more near the reticle now
- Wizardry Changes:
 ➼ The below changes are adjusted to balance the weapons especially when enchanted, socketed or scroll-enchanted.
  ➼ Slight damage nerf to UnderworldStaff and ChaosStaff secondary attack.
  ➼ Slight damage increase to TempestStaff secondary attack.
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
!Configs:
- Folder: _RelicHeimFiles
- Folder: wackysDatabase
- File: Azumatt.AzuCraftyBoxes.yml
- File: CreatureConfig_BiomeIncrease.yml
- File: CreatureConfig_Bosses.yml
- File: CreatureConfig_Creatures.yml
- File: CreatureConfig_Monstrum.yml
- File: CreatureConfig_Wizardry.yml
```
*-If you're on a server, update these plugins on your server*
```yaml
!Plugins:
- None in this update.
```
#
```yaml
📌 Changelog for RelicHeim v5.3.28 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Added missing Gamble items.
- Disabled Bulk enchant as it removes all your HealthRegen and is required to go along with LowHealth enchants which arent part of modpack.
- Enabled SpellSword enchant
- Adjusted stats for EitrWeaving and SpellSword
- Fixed some enchants being put on weapons that didn't benefit them.
# ValheimEnchantmentSystem:
- SkillOrbs are now controlled via DropThat.
  - If you're using Hunting by Blacks7ar please adjust your config settings or remove mod entirely since DropThat and Hunting don't play well together.
  - Hunting: "Need to turn drop system off and hunting yield to 1"
- SkillOrbs will drop based on the creature instead of biome.
- SkillOrbs will now drop one per player.
# Backpacks:
- Requested "Ammo Backpack" to store arrows and bolts only, no you cannot use them from inside the backpack.
# Weapon Changes: [Vanilla and Warfare]
- Fixed walking speed after shooting with a GreatBow.
- All Fist weapons main attack was changed to use dualknives attack animation with 3 combo chains, wider attack range and slight movement increase when attacking.
# Other:
- Adjusted experience points for Bosses in EpicMMO.
- Added -10% RunStaminaUsage to WindPotion.
- Adjusted spawns during boss fights to only be max of 1 at a time and longer spawn interval between.
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: EpicMMOSystem
- Folder: ValheimEnchantmentSystem
- Folder: wackysDatabase
- File: Backpacks.Majestic.yml
```
#
```yaml
📌 Changelog for RelicHeim v5.3.27 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# Epicloot:
- Fixed missing translations for effects.
- Adjusted values on a majority of enchants.
- Capes can now have Armor enchant.
- All 4 armor type pieces can have Elemental or Physical type enchants.
- To better distinguish if a Zeta/Relic item is an Item or SetBonus
  - Zeta/Relic Items text are colored in Cyan
  - Zeta/Relic SetBonus text are colored in Yellow
# Raids:
- Changed messages for raids to be more lore wise.
# Other:
- Fixed the Elder fight where the Shaman was spawning too frequently.
- Ancient Shaman health and health per star is reduced, creature was tougher than a brute making it difficult to take down.
- Changed burst weapons materials to look more based on the element and remove shard like material.
- Changed all Fists weapons BlockArmor and ParryBonus to feel more useful to use now.
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: wackysDatabase
- File: CreatureConfig_Creatures.yml
- File: CreatureConfig_Monstrum.yml
- File: CreatureConfig_Wizardry.yml
```
#
```yaml
📌 Changelog for RelicHeim v5.3.26 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Fist Weapons can now get AddBlunt or AddSlash effects.
- Fixed the set naming translation to normal.
- When defeating creatures in raids they will now have a small chance to drop enchanting materials ranging from Nexus to Zeta.
  - Zodiac and Zeta materials will not drop if raids are in the Meadows.
- Recipes for Belt and Rings should now show up properly due to update of mod.
- Crafting trophies should now be removed due to update of mod.
# Other:
- Increased the amount of valuables creatures will drop.
- Increased the amount of valuables creatures will drop from raids.
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: wackysDatabase
```
#
```yaml
📌 Changelog for RelicHeim v5.3.25 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Due to a looping issue, changes were made to some conversions.
- Fixed some Localization errors.
# Other:
- Lowered cost of SurtlingCores for WindRun and TailWind potions due to having cooldowns now.
- Slightly increased the timers on the Healing staffs till new heals can be applied.
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: wackysDatabase
```
#
```yaml
📌 Changelog for RelicHeim v5.3.24 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Cooldowns on Stash, Gamble and Maps are increased by 1 interval.
- Slight adjustments to the weights that were done in previous patch for TreasureMaps.
# Wackysdatabase:
- TailWind potion now has a cooldown.
- WindRun potion now has a cooldown.
# Other:
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: wackysDatabase
```
#
```yaml
📌 Changelog for RelicHeim v5.3.23 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Loot inside the chest from treasuremaps are now weighted based on biomes and progression.
- Loot insided Enchanted chest should hopefully now be more rewarding and different quantities per rarity and item.
- Removed files inside BountySaves I copied over by mistake from v5.3.22
# Other:
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: wackysDatabase
```
#
```yaml
📌 Changelog for RelicHeim v5.3.22 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Slightly increased how many items bosses drop.
- Sacrificing enchanted items now gives Dust.
- Disenchant upgrade chances were increased.
- Disenchant costs were slightly changed.
- New set piece for Zeta/Relic called "Cleric"
  - Total Sets: Offensive/Defensive/Magic/Cleric
- When items become a set, they will now have the name in the set.
  - Ex: "Enchanted Helmet" -> "Enchanted Offensive Helmet"
  - Ex: "Enchanted Chest" -> "Enchanted Defensive Chest"
- Increased the chance to get a Set Name for Zeta/Relic due to the amount in modpack giving more chances.
  - PLEASE share feedback if this need to be adjusted again, TY
# EpicMMO:
- Fixed experience ranges on some creatures.
# PassivePowers:
- Fixed Moders default values for WindSpeedModifier, increased passive chance slightly for TailWindChance.
# Other:
- Fixed Tail Wind Potion not being on Mead Kettle and changed vfx and sfx when consumed.
- New potion "Wind Run Potion" run faster when with the wind for a brief time.
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: EpicMMOSystem
- Folder: wackysDatabase
- File: CreatureConfig_Creatures.yml
- File: org.bepinex.plugins.passivepowers.cfg
- File: randyknapp.mods.epicloot.cfg
```
#
```yaml
📌 Changelog for RelicHeim v5.3.21 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Enabled Gamble and adjusted percentages.
- Some bounties per biome will have minions now since the issue of minions were fixed.
# ValheimEnchantmentSystem:
- Blessed Scrolls recipes no longer require coins, they use x5 material from regular scroll.
- Enchanting shields are now changed to better balance them out due to higher tier shields getting too strong.
  - Max level for all shields are now 15, success chance are reduced to match a level 20 enchant
  - Instead of percentage they're flat level increase.
  - Ex: Level 10 gives +10 block armor.
# Other:
- Adjusted all spawns during boss fights with a chance to spawn and reduced amount instead of being guaranteed.
- Burst Shot secondary attacks animation is changed, Eitr required to cast is increased based on tier of weapon.
- Poison Burst Shot changes
  - Removed lightning, causing to be too strong
  - Reduced base poison damage a bit, more poison per upgrade
  - Pierce damage per upgrade
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: ValheimEnchantmentSystem
- Folder: wackysDatabase
```
#
```yaml
📌 Changelog for RelicHeim v5.3.20 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- NEW FOLDER: "RelicHeimPatches"
  - This has updated file names.
  - The old folder "RelicHeim" will be auto deleted with ThisGoesHere mod.
- Updated files to work with new version of EpicLoot
- Gamble is disabled until it is fixed
- Enabled AttackSpeed effect due to being fixed
- Augmenter Relic and Enchanter Relic no longer give comfort and are just a decoration piece due to epicloot update.
- Localization folder inside EpicLoot folder is added for English file.
- Adjusted MaxRadius for bounty/maps Swamp&Mountain to hopefully not go far due to removal of 2 entry being obsolete, pray it returns <3.
# Backpacks:
- Andvaranaut Backpack is currently broken due to the effect, will need to use ring for now.
# Other:
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: wackysDatabase
```
#
```yaml
📌 Changelog for RelicHeim v5.3.19 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Fixed 2 Zeta/Relic items that would go on BloodMagic weapons giving it ElementalMagic skill enchant.
- Added 4 new Zeta/Relic items
- Fixed a few other Zeta/Relic items that had useless effects on them.
- Increased LifeSteal values.
# Backpacks
- Hopefully fixed some items not wanting to go in backpacks due to multiplayer issues.
# Other:
- Removed Elementalist from Bonemass as the increase to poison is very small making it pretty much useless.
- Adjusted all spawns during boss fights due to incorrect values.
- Increased TailWind Potion from 30s to 45s, final adjustment.
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: wackysDatabase
- File: Backpacks.Majestic.yml
- File: Backpacks.MajesticEpicLoot.yml
- File: CreatureConfig_BiomeIncrease.yml
- File: CreatureConfig_Bosses.yml
- File: CreatureConfig_Monstrum.yml
```
#
```yaml
📌 Changelog for RelicHeim v5.3.18 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Balanced out the rewards from Treasure Chests and Map Chests and adjusted the weights, added in Relic.
- Fixed the EnchantedChest rewards.
- Essences now convert in to equivalent dust instead of Novus Essence.
# ValheimEnchantmentSystem:
- Removed the bright glow from weapons based on level and adjusted some colors.
# Other:
- Increased coin stack to 9999.
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: ValheimEnchantmentSystem
- Folder: wackysDatabase
- File: ItemConfig_Base.yml
```
#
```yaml
📌 Changelog for RelicHeim v5.3.17 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Augment upgrades now have 50% reduction of tokens when upgrading the table.
- Reduced the salvage price on tokens, due to the quantity you can get, the prices were too high.
- Boss items can now be sacrificed.
- Only Novus materials will be salvaged.
- Changed few required mats for upgrading enchanting table for Augment
- New recipes under Salvage junk to turn higher tier materials in to Novus if have no use for them, Thanks Milkstout.
  - Essence is 1:1 until I can confirm there is no loop.
# EpicMMO:
- Increased the CriticalDamage starting value and Multiplier up to 50%.
- Increased AddCarryWeight value.
# Farming:
- Increased the experience received for the Farming skill due to not giving experience when harvesting as the skill is now Vanilla.
# Backpacks:
- Removed "Lumberjack Backpack" since "Foraging Backpack" basically does same thing.
# Other:
- Adjusted affix chances for Bosses.
- Reduced the WindPotions duration to 30s.
- Updated mod versions
# New Mod:
- CurrencyPocket by Azumatt
  - With EpicLoot, you need to take the coins out of your pocket to buy things at Haldor.
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: wackysDatabase
- File: Backpacks.Majestic.yml
- File: CreatureConfig_Bosses.yml
- File: org.bepinex.plugins.farming.cfg
- File: org.bepinex.plugins.creaturelevelcontrol.cfg
- File: WackyMole.EpicMMOSystem.cfg
```
#
```yaml
📌 Changelog for RelicHeim v5.3.16 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Added Warmth and Waterproof back as enchantable on capes.
- Capes can only have 1 of the 2 enchants at a time, Waterproof or Warmth. 
- Featherfall, Waterproof and Warmth effects are changed to only be on Zodiac or higher.
- Fixed a typo in an effect for HealthRegen enchant.
# Other:
- Fixed description of Fish Trap.
- Updated CreatureConfig files.
- Updated mod versions
# AzuCraftyBoxes: [File]
- I am including the yml file for this mod in the modpack to help with backpack issues that have been reported to help fix those issues, once the issue has been fixed I will remove this file from this modpack.
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: wackysDatabase
- File: Azumatt.AzuCraftyBoxes.yml [New File]
- File: CreatureConfig_BiomeIncrease.yml
- File: CreatureConfig_Bosses.yml
- File: CreatureConfig_Creatures.yml
- File: CreatureConfig_Monstrum.yml
- File: CreatureConfig_Wizardry.yml
```
#
```yaml
📌 Changelog for RelicHeim v5.3.15 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Removed recalling appearing on Warpikes
- Changed translation for Stagger Chance to better understand
- Stagger Chance effect can now be applied on TwoHandedWeapons and Chest only, Shields was removed. The values for this effect were slightly reduced.
- EnchantedChest has a very rare chance of containing an EnchantedKey along with a Ring or Belt containing one of the 3 sets.
- Fixed selection weight on addblunt that was left in.
- Added description for the Set pieces.
- Adjusted the prices for discounted items and added various different amounts so its more random.
# Other:
- Increased SutureKit healing to 100, gave Bandages some HealthRegen.
- Adjusted damage done to mobs after killing boss for that biome.
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: wackysDatabase
- File: CreatureConfig_BiomeIncrease.yml
```
#
```yaml
📌 Changelog for RelicHeim v5.3.14 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Discounted item in secret stash is back, only one this time.
- EnchantedKeys are set to 20 Tokens again due to increase in ForestTokens from chests.
- Adjusted some enchants to not be on BloodMagic type weapons since they are useless on them
- Changed description of NovusEssence.
- Slightly increased Armor, Stamina and Health enchant values.
# TargetPortal:
- Changed keybind to show portals on map from "P" to "KeypadDivide" to avoid turning off and on when typing.
  - This key "/" is on your keypad.
# Other:
- Hopefully fixed offspring tames from having chaos or poison infused causing damage to player when killing them.
- BandageImproved recipe no longer uses Root and is replaced with Withered Bone
- Draugrs have a chance now to drop Withered Bone.
- Increased the damage and projectiles for the Eruptor weapons.
- Slightly tweaked the damage and projectiles for the Burst weapons
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: wackysDatabase
- File: CreatureConfig_Creatures.yml
- File: org.bepinex.plugins.creaturelevelcontrol.cfg
- File: org.bepinex.plugins.targetportal.cfg
```
#
```yaml
📌 Changelog for RelicHeim v5.3.13 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot: [Bounty Hotfix]
- Fix to the bounty system from last patch which caused maps and bountys to go further out than intended, this hotfix should now make it little more better.
# Other:
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: EpicLoot
```
#
```yaml
📌 Changelog for RelicHeim v5.3.12 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot: [Enchanting Changes]
- Removed QuickDraw for crossbows.
- Slightly increased the coin rewards on bounties
- Slightly increased amount of Forest Tokens from Maps and reduced price slightly.
- Hopefully fixed bounties going to further out.
- Secret Stash prices slightly reduced.
- Sacrificing items will now give a Runestone and Shard.
- Upgrading Shards are now x2NovusShard + x1Essence(rarity) = x2 Shard(rarity)
- Upgrading Dust are now x2NovusDust + x1Essence(rarity) = x2 Dust(rarity)
- Upgrading Runestones are now x2NovusRunestone + x1Essence(rarity) = x2 Runestone(rarity)
- Novus Dust,Runestone and Shard can now be turned in to 5 coins at the enchanting table under Salvage Junk to help with excess amounts.
# Other:
- MiningBackpack valid items update to allow ore/metals in case other mods add any new types.
- Fixed status effect icon for WindPotion
- Adjusted inputs for SmallVersion pieces to match what they would have based on boss kills when unlocked, these arent changed with ConversionSizeAndSpeed mod so this is best I can do.
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: wackysDatabase
- File: Backpacks.Majestic.yml
```
#
```yaml
📌 Changelog for RelicHeim v5.3.11 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot: [Notice]
- In a future update I will either be removing the Gamble section or making major changes to it, It's not a feature I like so this is just a heads up.
  - I will provide information in my discord on how to add it back when I do decide to change it.
- Adjusted Eikthyrs drops.
- Increased Andvaranaut Range
  - Backpack version might not use the new value.
# EpicMMO:
- Adjusted some vanilla creature experience.
- Change scaling exp, overall reduced experience needed to level up.
# Backpacks:
- Added new "Scroll Backpack" to put your scrolls inside.
# Other:
- Added a WindPotion to help with sailing, this is only for RelicHeim.
  - Please provide feedback, this is just to help until you get Moder Power etc.
- Adjusted some spawns.
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: EpicMMOSystem
- Folder: wackysDatabase
- File: Backpacks.Majestic.yml
- File: randyknapp.mods.epicloot.cfg
- File: WackyMole.EpicMMOSystem.cfg
```
#
```yaml
📌 Changelog for RelicHeim v5.3.10 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Increased values of AddCarryWeight enchant for all rarity so it feels worth to have even at Novus.
# Other:
- Fixed CrudeCrossbow to be bit more balanced in the meadows, will remove file once Therzie updates Warfare with the changes.
- Fixed Shark spawn world distance value.
- Allowed Small Kiln to take FineWood and CoreWood.
- Increased prices for Golden Trophies.
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: wackysDatabase
```
#
```yaml
📌 Changelog for RelicHeim v5.3.9 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# Backpacks:
- Removed Weaponry and Armory Backpacks for now until fixed.
- Disabled original backpack and created duplicate version with correct workbench level, gave it small percentage for reduced weight for items inside
# Other:
- Small fix to boss fight spawns again, everything should be more balanced, fixed a typo.
# New Mod:
- PetPantry by:Azumatt
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: wackysDatabase
- File: Backpacks.Majestic.yml
- File: CreatureConfig_Bosses.yml
- File: org.bepinex.plugins.backpacks.cfg
```
#
```yaml
📌 Changelog for RelicHeim v5.3.8 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Adjusted loot drops for bosses and rarity.
# EpicMMO:
- MaxLevelRange is now 15 instead of 10, this should hopefully help with players trying to level up, if not, use XP Potions and kill shit.
  - I'll mention this again, EpicMMO is NOT needed in order to do anything in the modpack, it is just to help with more stats if needed.
# FactionAssigner:
- Updated most factions to be assigned based on their biome, most creatures will now attack each other if in nearby biomes.
# WackysDatabase:
- As a request there is now smaller version of some pieces.
  - Kiln, Smelter, BlastFurnace, WindMill, EitrRefinery and KingdomOven.
- All of these should act just as normal but just smaller.
- New category in Hammer called "TinyVersions"
- New folder in "config\wackysDatabase\Pieces\JewelHeimWDB2.0" called "SmallerVersions" where all of the files will be located.
# Other:
- Adjusted the stamina use for Eruptor Weapons and Magic Burst weapon.
- Fixed Foxs HP being too high.
- Fixed Darkhorns HP.
- Fixed the extra spawns I made to boss fights, made them too difficult (sorry lol)
- Updated mod versions
# NewMod:
- Azumatt-TrueInstantLootDrop (Client Only)
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: wackysDatabase
- File: Azumatt.FactionAssigner.yml
- File: Backpacks.Majestic.yml
- File: CreatureConfig_Bosses.yml
- File: CreatureConfig_Monstrum.yml
- File: CreatureConfig_Wizardry.yml
- File: WackyMole.EpicMMOSystem.cfg
```
#
```yaml
📌 Changelog for RelicHeim v5.3.7 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicMMO:
- Added EliteCreatures to drop Mobchunks at 5%.
- Haldor now sells Exp Potions.
# CLLC:
- Fixed config file of wrong Mending values and lock configuration back to On.
- Slightly increased Wolfs overall HP, slightly nerfed Wolfs overall DMG
- Slightly reduced Grizzly Bear stat values
- First 3 bosses were slightly tweaked.
- Stone and Obsidian Golems no longer spawn as Splitting since they get yeeted when killed. (Hopefully)
# Other:
- Fixed SerpentStew material quantity.
- Added new Backpack for Trophys
- Fixed FoodBackpack not allowing Wizardry Mushrooms.
- Updated the 3 craftable belts carry weight values and added movement speed.
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: wackysDatabase
- File: Backpacks.Majestic.yml
- File: CreatureConfig_Bosses.yml
- File: CreatureConfig_Creatures.yml
- File: CreatureConfig_Monstrum.yml
- File: org.bepinex.plugins.creaturelevelcontrol.cfg
- File: WackyMole.EpicMMOSystem.cfg
```
#
```yaml
📌 Changelog for RelicHeim v5.3.6 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# CLLC:
- Added "Affix Power" to YML file to make sure all bosses with Mending are set to "0.1" power in case config file makes things weird
- Slightly increased the difficulty of Meadows.
- Adjusted the sector levels amount and when killing elite creatures the amount is increased.
- Turned off the sector ping on minimap (The red circle).
# Other:
- Adjustments to StaffOfFrost values.
- Removed Spirit off the Frost Burst Shot and replaced with Pierce.
- Increased Flint Eruptors damage by 1.
- Added 1 Spirit damage to Magic Burst Shot.
- Removed TanningRack being a crafting station and its recipes, it was preventing spawns in GoblinCamps.
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: wackysDatabase
- File: CreatureConfig_Bosses.yml
- File: CreatureConfig_Creatures.yml
- File: CreatureConfig_Monstrum.yml
- File: org.bepinex.plugins.creaturelevelcontrol.cfg
```
#
```yaml
📌 Changelog for RelicHeim v5.3.5 [Patch 0.220.5]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Renamed the old Augmenter and Enchanter pieces and changed description to help players know its only for decoration+comfort.
# Backpacks:
- YML file turned on, files updated.
- ExplorerBackpacks weight is 95%
- Backpacks can be put in chests
- Auto Open Backpack is OFF
  - If you have customized this config already please make a backup of your file, otherwise use the one added in this update.
# Other:
- Adjustments to Rag Armor.
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: wackysDatabase
- File: Backpacks.Majestic.yml
- File: Backpacks.MajesticEpicLoot.yml
- File: Backpacks.Wizardry.yml
- File: org.bepinex.plugins.backpacks.cfg
```
#
```yaml
📌 Changelog for RelicHeim v5.3.4 [Patch 0.220.4]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- In enchanting table, Enchant and ConvertMaterials will now be unlocked for free, players will need to still unlock Augment and Disenchant.
 - This change is due to recently seeing players confused on how to use the table or how to start enchanting.
- Added the option to buy the Andvaranaut ring for 2k coins as well.
- Adjustments to the loot inside Enchanted Chest when using Enchanted Key.
# WackysDatabase:
- Lingering Stamina Potions are in its own category now which allows the player to use stamina potions now.
- New Staff of Healing (Major) for mountains.
 - Ranges on healing staffs I can't adjust. (Cuddle Up)
 - Removed Stamina from HealingStaffs due to issues with it being spammable.
# CLLC:
- Reduced the chances for "Armored" to appear on creatures.
- Adjustments to some values.
# Other:
- Fixed NoiseReduction naming.
- Fixed stone pickaxe repair issue. (hopefully)
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: wackysDatabase
- File: CreatureConfig_BiomeIncrease.yml
- File: CreatureConfig_Bosses.yml
- File: org.bepinex.plugins.creaturelevelcontrol.cfg
```
#
```yaml
📌 Changelog for RelicHeim v5.3.3 [Patch 0.220.3]
```
```markdown
Note: Any files you configure make sure to make backups.
# Other:
- Updated mod versions
- Removed AfterDeath from modpack
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
-
```
#
```yaml
📌 Changelog for RelicHeim v5.3.2 [Patch 0.220.3]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Fixed translation for activated set effects.
- New file with corrected cooldowns for activated effects.
- Bulwark and Berserker cooldowns are 5m.
- Complete overhaul of Zeta/Relic set items, all sets were removed except Shiva.
- 6 new sets based off of "Offensive, Defensive, Magic", all information on these sets are in my discord.
- These changes were made to help with confusion of what can be enchanted or not in order to get specific set items. If your current set items are ruined then I do apologize but I needed to make this change as too many sets were causing issues.
# Other:
- Updated mod versions
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
```
#
```yaml
📌 Changelog for RelicHeim v5.3.1 [Patch 0.220.3]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Legendary/Mythic set that used Rings/Belts are removed and are replaced as Utility so other items in that tier can be rolled on as well.
# Other:
- Updated mod versions
- TargetPortal and Groups works now.
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
```
#
```yaml
📌 Changelog for RelicHeim v5.3.0 [Patch 0.220.3]
```
```markdown
Note: Any files you configure make sure to make backups.
# EpicLoot:
- Added new Warfare items to files.
# VES:
- Added new Warfare items to files.
# Other:
- Updated mod versions
- New mod dependency added for EpicLoot "JsonDotNET"
```
*-If you're on a server, just copy the below updated files/folders to your server after updating*
*-Always delete the cache folder inside __config\wackysDatabase\Cache__*
```yaml
- Folder: _RelicHeimFiles
- Folder: EpicLoot
- Folder: ValheimEnchantmentSystem
```
```yaml
Disable these mods until they're updated
- Groups
- TargetPortal
```
</details>