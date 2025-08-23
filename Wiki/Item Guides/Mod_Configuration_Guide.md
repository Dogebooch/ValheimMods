# Mod Configuration Guide

## Overview

This guide covers the configuration of inventory and storage management mods, with a focus on **SmarterContainers** and similar mods that handle item organization and auto-sorting. These mods help manage complex inventory systems with leveled items, augmented weapons, and various material types.

---

## SmarterContainers Configuration

### **Mod Overview**
SmarterContainers is an intelligent inventory management mod that automatically sorts items into appropriate containers based on predefined groups, item types, and custom configurations.

### **Key Features**
- **Smart Auto-Sorting**: Automatically places items in the best nearby container
- **Custom Item Groups**: Create personalized item categories
- **GUI Buttons**: In-game interface for managing groups and unloading items
- **Key-Based Control**: Choose when auto-sorting occurs
- **Prefix/Postfix Grouping**: Automatic grouping based on item naming patterns

---

## Installation & Setup

### **Prerequisites**
- BepInEx installed
- Configuration Manager mod (recommended for in-game configuration)

### **Configuration File Location**
```
Valheim/BepInEx/config/flueno.SmartContainers.cfg
```

### **In-Game Configuration**
1. **Enable Console**: Add `-console` to your Valheim launch options
2. **Install BepInEx Configuration Manager**: Provides GUI for mod settings
3. **Access Settings**: Press F1 in-game to open Configuration Manager

---

## Configuration Options

### **General Settings**

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | true | Enables/disables the mod |
| `range` | 14 | Distance (meters) to search for containers |
| `hkeyModifier` | LeftControl | Key for triggering smart sorting |
| `groupingKeyModifier` | LeftControl + LeftShift | Key for grouping behavior |
| `hudMessageEnabled` | true | Shows messages when items are routed |
| `audioFeedbackEnabled` | true | Plays sound on successful transfers |
| `effectFeedbackEnabled` | true | Highlights target containers |

### **Grouping System**

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | true | Enables item grouping logic |
| `itemTypeGroupsEnabled` | true | Groups by item type (Tool, Weapon, etc.) |
| `fuzzyGroupingEnabled` | false | Broader grouping criteria |
| `createGroupBtnEnabled` | true | Shows ☼ button in chest UI |
| `mergePromptEnabled` | true | Shows merge dialog for existing groups |

### **Predefined Item Groups**

The mod includes several built-in groups:

```cfg
[ItemGroup]
valuables = ruby,coins,amber,amberpearl
ore = copperore,flametalore,ironore,silverore,tinore,ironscrap,blackmetalscrap
wood = wood,finewood,corewood,elderbark,roundlog
mushrooms = Mushroom,MushroomBlue,MushroomYellow,mushroomcommon
berries = Blueberries,raspberries,cloudberries,honey
vegetables = Carrot,Turnip
cookedMeat = CookedLoxMeat,NeckTailGrilled,MeatCooked,FishCooked,SerpentMeatCooked
food = CarrotSoup,Sausages,QueensJam,SerpentStew,TurnipStew,BloodPudding
```

---

## Creating Custom Groups

### **Method 1: In-Game UI (Recommended)**

1. **Place Items**: Put the items you want to group in a chest
2. **Click ☼ Button**: Located at bottom-left of chest interface
3. **Create Group**: Choose to create a new group or merge with existing
4. **Name Group**: Give your group a descriptive name

### **Method 2: Manual Configuration**

Add custom groups to the configuration file:

```cfg
[ItemGroup]
## Custom spell groups
fireSpells = Fireball_I,Fireball_II,Fireball_III,Fireball_IV,Fireball_V
iceSpells = IceSpell_I,IceSpell_II,IceSpell_III,IceSpell_IV
lightningSpells = LightningBolt_I,LightningBolt_II,LightningBolt_III

## Weapon augmentation groups
swordAugments = Sword_Augment_Fire,Sword_Augment_Ice,Sword_Augment_Lightning
axeAugments = Axe_Augment_Fire,Axe_Augment_Ice,Axe_Augment_Lightning

## Material tier groups
magicMaterials = DustMagic,RunestoneMagic,EssenceMagic
rareMaterials = DustRare,RunestoneRare,EssenceRare
epicMaterials = DustEpic,RunestoneEpic,EssenceEpic
legendaryMaterials = DustLegendary,RunestoneLegendary,EssenceLegendary
```

---

## Handling Leveled Items

### **Spells of Different Levels**

**Example Setup for Magic Revamp Spells:**

```cfg
[ItemGroup]
## Fire magic spells (all levels)
fireMagic = Fireball_I,Fireball_II,Fireball_III,Fireball_IV,Fireball_V
fireBurst = FireBurst_I,FireBurst_II,FireBurst_III
fireStorm = FireStorm_I,FireStorm_II,FireStorm_III

## Ice magic spells (all levels)
iceMagic = IceSpell_I,IceSpell_II,IceSpell_III,IceSpell_IV
frostNova = FrostNova_I,FrostNova_II,FrostNova_III
iceBarrier = IceBarrier_I,IceBarrier_II,IceBarrier_III

## Lightning magic spells (all levels)
lightningMagic = LightningBolt_I,LightningBolt_II,LightningBolt_III
chainLightning = ChainLightning_I,ChainLightning_II,ChainLightning_III
thunderStrike = ThunderStrike_I,ThunderStrike_II,ThunderStrike_III
```

**How to Set Up:**
1. Create a dedicated "Spells" chest
2. Place one of each spell level in the chest
3. Click the ☼ button to create a group
4. Name it "spells" or "magic"
5. All spell levels will now auto-sort to this chest

### **Weapon Augmentations**

**Example Setup for Augmented Weapons:**

```cfg
[ItemGroup]
## Fire-augmented weapons
fireWeapons = Sword_Augment_Fire,Axe_Augment_Fire,Mace_Augment_Fire
fireBows = Bow_Augment_Fire,Crossbow_Augment_Fire

## Ice-augmented weapons
iceWeapons = Sword_Augment_Ice,Axe_Augment_Ice,Mace_Augment_Ice
iceBows = Bow_Augment_Ice,Crossbow_Augment_Ice

## Lightning-augmented weapons
lightningWeapons = Sword_Augment_Lightning,Axe_Augment_Lightning,Mace_Augment_Lightning
lightningBows = Bow_Augment_Lightning,Crossbow_Augment_Lightning
```

**Alternative: Prefix-Based Grouping**

If your augmented weapons follow a naming pattern, you can use prefix grouping:

```cfg
[PrefixedItemGroups]
prefixes = trophy,mead,arrow,armor,cape,helmet,atgeir,bow,battleaxe,knife,mace,shield,sledge,spear,sword,tankard,club,mushroom,arrow,Sword_Augment,Axe_Augment,Bow_Augment
```

---

## Preventing Auto-Sorting for Specific Items

### **Excluding Items from Auto-Sorting**

Add problematic items to the `itemsSkipList`:

```cfg
[Unload]
## List of item-names to exclude from being 'unloaded'
itemsSkipList = ProblemItem1,ProblemItem2,ItemYouWantToPlaceManually
```

### **Using Different Key Combinations**

Configure the mod to only auto-sort with specific key combinations:

```cfg
[General]
## Regular click = no auto-sorting
hkeyModifier = LeftControl

[Grouping]
## Ctrl + Click = smart sorting
## Ctrl + Shift + Click = grouping behavior
groupingKeyModifier = LeftControl + LeftShift
```

**Usage:**
- **Regular Click**: Manual placement, no auto-sorting
- **Ctrl + Click**: Smart sorting (exact matches first)
- **Ctrl + Shift + Click**: Grouping behavior (similar items)

---

## GUI Buttons

### **☼ Button (Create Group)**
- **Location**: Bottom-left of chest interface
- **Function**: Creates custom item groups
- **Usage**: Place items in chest → Click ☼ → Create group

### **⇓⇓ Button (Unload Items)**
- **Location**: Bottom-left of chest interface (above ☼ button)
- **Function**: Unloads items from inventory to nearby chests
- **Usage**: Click to batch-unload items based on configured groups

### **Button Positioning**
```cfg
## Adjust button positions if needed
createGroupBtnPos = {"x":1.5,"y":10.699999809265137}  # ☼ button
btnPos = {"x":1.5,"y":8.149999618530274}              # ⇓⇓ button
```

---

## Similar Mods & Mechanics

### **EpicLoot System**
- **Auto-sorting**: EpicLoot items can be grouped by rarity
- **Configuration**: `config/randyknapp.mods.epicloot.cfg`
- **Groups**: Magic, Rare, Epic, Legendary, Mythic

### **Valheim Enchantment System (VES)**
- **Enchanted Items**: Can be grouped by enchantment type
- **Configuration**: `config/kg.ValheimEnchantmentSystem.cfg`
- **Groups**: Fire, Ice, Lightning, Poison enchanted items

### **Wacky's Database**
- **Custom Items**: Supports custom item definitions
- **Configuration**: `config/WackyMole.WackysDatabase.cfg`
- **Integration**: Works well with SmarterContainers grouping

---

## Troubleshooting

### **Common Issues**

**Problem**: Items not auto-sorting correctly
**Solution**: 
1. Check item names in configuration
2. Verify container range settings
3. Ensure groups are properly defined

**Problem**: GUI buttons not visible
**Solution**:
1. Verify `createGroupBtnEnabled = true`
2. Check button positioning
3. Restart game after configuration changes

**Problem**: Items going to wrong containers
**Solution**:
1. Add problematic items to `itemsSkipList`
2. Create more specific custom groups
3. Use different key combinations for different behaviors

### **Performance Tips**

1. **Limit Range**: Keep `range` setting reasonable (10-20 meters)
2. **Disable Unused Groups**: Clear empty group definitions
3. **Use Specific Groups**: Create targeted groups rather than broad categories
4. **Regular Maintenance**: Periodically review and update groups

---

## Advanced Configuration Examples

### **Complete Spell Management Setup**

```cfg
[ItemGroup]
## All fire spells (all levels)
fireSpells = Fireball_I,Fireball_II,Fireball_III,Fireball_IV,Fireball_V,FireBurst_I,FireBurst_II,FireBurst_III,FireStorm_I,FireStorm_II,FireStorm_III

## All ice spells (all levels)
iceSpells = IceSpell_I,IceSpell_II,IceSpell_III,IceSpell_IV,FrostNova_I,FrostNova_II,FrostNova_III,IceBarrier_I,IceBarrier_II,IceBarrier_III

## All lightning spells (all levels)
lightningSpells = LightningBolt_I,LightningBolt_II,LightningBolt_III,ChainLightning_I,ChainLightning_II,ChainLightning_III,ThunderStrike_I,ThunderStrike_II,ThunderStrike_III

## All utility spells
utilitySpells = Teleport_I,Teleport_II,Teleport_III,Shield_I,Shield_II,Shield_III,Heal_I,Heal_II,Heal_III
```

### **Weapon Augmentation Management**

```cfg
[ItemGroup]
## Fire-augmented weapons (all types)
fireAugments = Sword_Augment_Fire,Axe_Augment_Fire,Mace_Augment_Fire,Bow_Augment_Fire,Crossbow_Augment_Fire,Atgeir_Augment_Fire

## Ice-augmented weapons (all types)
iceAugments = Sword_Augment_Ice,Axe_Augment_Ice,Mace_Augment_Ice,Bow_Augment_Ice,Crossbow_Augment_Ice,Atgeir_Augment_Ice

## Lightning-augmented weapons (all types)
lightningAugments = Sword_Augment_Lightning,Axe_Augment_Lightning,Mace_Augment_Lightning,Bow_Augment_Lightning,Crossbow_Augment_Lightning,Atgeir_Augment_Lightning

## Poison-augmented weapons (all types)
poisonAugments = Sword_Augment_Poison,Axe_Augment_Poison,Mace_Augment_Poison,Bow_Augment_Poison,Crossbow_Augment_Poison,Atgeir_Augment_Poison
```

### **Material Tier Management**

```cfg
[ItemGroup]
## Magic tier materials
magicMaterials = DustMagic,RunestoneMagic,EssenceMagic,ShardMagic,CrystalMagic

## Rare tier materials
rareMaterials = DustRare,RunestoneRare,EssenceRare,ShardRare,CrystalRare

## Epic tier materials
epicMaterials = DustEpic,RunestoneEpic,EssenceEpic,ShardEpic,CrystalEpic

## Legendary tier materials
legendaryMaterials = DustLegendary,RunestoneLegendary,EssenceLegendary,ShardLegendary,CrystalLegendary

## Mythic tier materials
mythicMaterials = DustMythic,RunestoneMythic,EssenceMythic,ShardMythic,CrystalMythic
```

---

## Best Practices

1. **Start Simple**: Begin with basic groups and expand gradually
2. **Use Descriptive Names**: Name groups clearly for easy identification
3. **Test Configurations**: Verify groups work as expected before expanding
4. **Backup Configurations**: Keep backups of working configurations
5. **Document Changes**: Note what changes work for future reference
6. **Regular Updates**: Update groups as new items are added to the modpack

---

## Additional Resources

- **Mod Page**: [SmarterContainers on Thunderstore](https://thunderstore.io/c/valheim/p/Roses/SmarterContainers/)
- **Configuration Manager**: [BepInEx Configuration Manager](https://thunderstore.io/c/valheim/p/Azumatt/Azus_UnOfficial_ConfigManager/)
- **Community Support**: Check mod Discord servers for additional help

---

## Seasonal Clothing Considerations

### Summer Clothing
- **Overheating**: You will overheat in summer if you wear too hot clothing
- **Recommendations**: Use lighter armor sets during summer months
- **Mod Interactions**: Some mods may add seasonal clothing effects

### Winter Clothing
- **Building Protection**: Snow does not damage buildings in the winter
- **Clothing Requirements**: Consider using warmer clothing for winter exploration
- **Mod Interactions**: Seasonal mods may affect clothing effectiveness

---

*This guide covers the essential configuration options for inventory management mods. For specific mod interactions or advanced configurations, refer to individual mod documentation.*
