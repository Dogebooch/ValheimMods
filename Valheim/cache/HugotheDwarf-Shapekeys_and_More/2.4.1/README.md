This is a client-side mod that acts as a utility and a soft library for other mods to use to make use of Shapekeys(Blendkeys) for a having a fit for males and females. It also supports male and female swap outs for models if the prefabs are assembled correctly, as well as custom Itemstand layouts and "attach_other" for creating sheathes for items. 


Allows a male and female deformation for 3D models (skinned mesh renderers) if there is a shapekey named "female" it will activate that if the player model is female.

Allows for different models to be used for males and females if the "Attach_Skin" has children named "male" and "female" and will "enable" the correct one based on the player model (male or female)

Allows for creation of sheathes or any other "extra wearable" for weapons if a new child is added to the base prefab called "attach_other"

Can create different placements for items if you assign a "attach_stand" if you wish for different looks for horizontal and/or vertical itemstands you can nest child nodes "h" for horizontal and "v' for vertical.

Allows for "variants" aka Styles of models for things if there is a "style_#" child that matches (Starts at 0, like 'style_0' for default/style)
Allows for "levels" aka Quality of models for things if there is a "level_#" child that matches (Starts at 0, like 'level_0' for quality 1)

Nexus Page: https://www.nexusmods.com/valheim/mods/1858