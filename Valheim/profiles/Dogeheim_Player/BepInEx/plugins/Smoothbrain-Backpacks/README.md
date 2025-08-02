# Backpacks

Adds a backpack that can be equipped, without having to decide between wearing your cloak or utility item and your backpack. Can be upgraded to increase the size of the backpack.

Assets provided by CookieMilk. Thanks a lot!

Can be installed on a server, to enforce the configuration.

### Build your own backpack!

You can create a Backpacks.yml file in your config folder and use it to create your very own backpack, unique to you!

On a server, creating the file in the config folder of the server is enough, the clients don't need the file.

Make sure to toggle the "use external YAML file" option to on in your cfg file or it won't work.

Example configuration for your own backpack:
```yml
Blaxxunpack: # Give your backpack an amazing name! Quote the name, if you want to use special characters. "Blaxxun's Pack":
  description: "A huge backpack, just for dandelions!" # And a descriptive description!
  size: 6x3 # This means 6 columns and 3 rows, so 18 slots in your backpack. Keep it small! Don't go higher than 8 here. Valheim doesn't like that at all.
  unique: global # This sets how many backpacks you can have in your inventory. See below for more info.
  effect: SE_Warm # Name of a status effect to apply to the player, if the backpack is equipped.
  appearance: # Now make it really unique and personalized, it's just your backpack after all!
    Sleepbag: hidden # Hide the sleepbag at the top of the backpack.
    BackpackStrapTop: hidden # Hide the straps that were holding the sleepbag as well.
    BackpackFlap: ff00fe # Color the flap at the top pink.
  crafting: # Make your backpack craftable.
    station: Workbench # The crafting station where you can craft your backpack.
    level: 3 # The required crafting station level to craft your backpack.
    costs: # The cost for crafting your backpack.
      Wood: 3 # Needs 3 wood.
      Stone: 5 # And 5 stone.
  valid items: # Define what items can go into your backpack.
    - Dandelion # Use the prefab name! One item per line! Like making a shopping list.
  upgrade: # Can your backpack be upgraded? Define as many upgrades as you want!
    1: # Config for the first upgrade.
      Wood: 5 # Need 5 wood
      Stone: 10 # And 10 stone.
      size: 6x4 # The new size after upgrading the backpack for the first time. 6 columns and 4 rows, so one row more than the base!

# You can also use weight factor to make items in your backpack lighter!
# weight factor: 0.8
# Would mean that items in your backpack only weigh 80% of their original weight!
# You can use teleport to allow every content in your backpack to be taken through a portal, even if it wouldn't work otherwise!
# teleport: true
# Would mean that you can put your ore into the backpack and take it through a portal!

# If you want no item restriction for your backpack, simply remove the "valid items" section of the config.

# Unique flags:
# global: Exclusive with any other backpack.
# restricted: Exclusive with backpacks that have no item restrictions.
# type: Exclusive with backpacks with the same type.
# bypass: Not exclusive, bypass all restrictions. Supersedes any other flag.
# none: Same as bypass, but doesn't overrule all other flags.

# Backpack parts can either be 'visible' or 'hidden'. To color them, use the hex code of the color you want to use.
# Valid backpack parts are: ToolstrapBottom, Pickaxe, RingBottomLeft, BackpackBody, MetalclipLeft, ToolstrapTop, PouchFront, PouchLeft, Knifesheath, Knife, MetalclipFrontRight, Pot, Sleepbag, BackpackStrapTop, BackpackStrapBottom, MetalclipFrontLeft, BackpackFlap, Teapot.
# Predefined item groups you can use for the valid items are:
# ore, metal, food, potions, woods, trophy, boss trophy, valuable, seed, crop, stackable.
# pants, chest, helmet, cape, armor.
# axes, clubs, knives, pickaxes, polearms, spears, swords, bows, crossbows, weapon, arrows, bolts, ammo.
# round shield, tower shield, shield.
# special (fishing rod and megingjord), tool, equipment.

# You can also define your very own item groups!
# groups:
#   content of my backpack:
#     - Stone
#     - Wood
#   content of my other backpack:
#     - Silver
#     - Iron
# This would create the groups "content of my backpack" and "content of my other backpack" and allows you to use these groups as valid items for your backpack.
```

### Something that vaguely resembles a change log

#### V1.3.6

Fixed place stacks button, so that it places stacks again.

#### V1.3.5

Updates for Bog Witch. To make Azu happy.

#### V1.3.4

Added even more features to the API, to make Azu happy.

#### V1.3.3

Added more features to the API.

#### V1.3.2

Various bug fixes for bugs reported by you.

#### V1.3.1

Removed the directory not found error, when using bows before boes.

#### V1.3.0

Added a lot of new options to the mod. There is an auto fill option for backpacks now, which stores items in the backpack automatically. You can hide the backpack visual on your back now. Backpacks open automatically, if you open the inventory (there is also a config option to disable this). Added a close button to the backpack, so you don't have to close the entire inventory, to close the backpack. Backpacks can now be unique, which means players can only have on backpack in their inventory. You can now add status effects that will be applied to players, if they equip the backpack. And probably some other stuff I've already forgot about. Also increased the performance of backpacks.

#### V1.2.11

Iron Gate made me update the mod again. Thanks.

#### V1.2.10

If you are using Azus ExtendedPlayerInventory mod, there will be an equipment slot for your backpacks now.

#### V1.2.9

Removed an error that could occur on logout.

#### V1.2.8

Restored compatibility with certain quivers.

#### V1.2.7

Iron Gate thought I am bored and made me update again.

#### V1.2.6

If you are looking for the take all button, it moved from the bottom left to the top left!

#### V1.2.5

Your character will no longer greet you naked in the start menu, if you logged out with an equipped backpack. While some people enjoyed the view, others did not.

#### V1.2.4

Fixes for the Hildirs Request update.

#### V1.2.3

Some other mods could break backpacks on logout. Now they don't.

#### V1.2.2

Just some minor bug fixes again. You can also use spaces in backpack names now.

#### V1.2.1

Some very minor bug fixes for the last update. I am surprised how well this works overall already.

#### V1.2.0

Slowly starting to go big now. Added "build your own backpack". Yes, you can create your very own backpack via a YAML file now. Or build 20 different backpacks, one for each player on your server! Give them their favorite color or make their backpack look extra stupid! Ban them from your server, when they use your backpack, instead of their backpack. See the huge "build your own backpack" section above this "changelog" for more information, if you haven't read it yet. Or read it again, just to make sure.

#### V1.1.1

Based on popular demand, I made the mod more casual friendly by allowing players to die without their game crashing.

Also added a lot of duct tape to other parts of the mod, so I am somewhat positive that the previous update actually works now.

#### V1.1.0

Okay, time to finally turn this into a real backpack mod. You can now equip backpacks. This doesn't make you stronger, but lets other players know that you are carrying a backpack. Has a custom slot for this, so you don't have to decide between wearing a cloak or a backpack. Or a utility item. Just wear everything at once to look extra fabulous!

Your backpack can also level up alongside your adventure now. This will increase its size. Not that size is important or anything. Make sure to check the upgrade tab on your workbench.

You might have to delete your config file for everything to work flawlessly.

More to come soonish.

#### V1.0.4

Iron Gate made me update the mod with their Valheim update today. Sometimes, I am wondering where it all went wrong. It started out with a simple "Wow, this game is way too easy, I'll make a mod that lets creatures spawn with up to 5 stars." about two years ago. Can't really remember what happened after that, but here I am, managing 70 mods and 30 of them need updates today. About 20 mods in, I am really starting to regret my life choices.

#### V1.0.3

There is a config option that can prevent players from putting backpacks with items inside into a chest, turning the chest into some kind of infinite wormhole for items. Modding would be fun, if it wasn't for the users. How dare you coming up with stuff like that.

#### V1.0.2

Someone said that backpack weight should be a slider. I thought a lot about it, to be able to disagree, but couldn't come up with an argument. So, it's a slider now, have fun.

#### V1.0.1

In the beginning God created the backpacks. The backpacks were without config options and couldn't be used on servers, for all the cheaters would abuse the backpacks. And the spirit of God was hovering over the backpacks.
Then God said 'Let there be config options'; and there were config options. And god saw the config options, that they were good; and God decided that the backpacks can now be used on servers.