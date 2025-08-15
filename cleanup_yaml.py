#!/usr/bin/env python3
import re

# Groups to remove (with their exact names from the file)
groups_to_remove = [
    'BlackforestPack1Loot1', 'BlackforestPack1Loot2', 'BlackforestPack1Loot3', 'BlackforestPack1Loot4',
    'BlackforestPack2ForgeLoot1', 'BlackforestPack2GraveLoot1', 'BlackforestPack2HouseLoot1',
    'BlackforestPack2RuinsLoot1', 'BlackforestPack2SkullLoot1', 'BlackforestPack2TowerLoot1',
    'MistLoot1',
    'MistlandsPack1Loot1', 'MistlandsPack1Loot2', 'MistlandsPack1Loot3', 'MistlandsPack1Loot4',
    'MistlandsPack1Loot5', 'MistlandsPack1Loot6', 'MistlandsPack1Loot7', 'MistlandsPack1Loot8',
    'PlainsLoot1', 'PlainsLoot2', 'PlainsLoot3',
    'SwampPack1Loot1', 'SwampPack1Loot2', 'SwampPack1Loot3', 'SwampPack1Loot4', 'SwampPack1Loot5',
    'SwampPack1Loot6', 'SwampPack1Loot7', 'SwampPack1Loot8', 'SwampPack1Loot9', 'SwampPack1Loot10'
]

input_file = 'Valheim/profiles/Dogeheim_Player/BepInEx/config/warpalicious.More_World_Locations_LootLists.yml'
output_file = 'Valheim/profiles/Dogeheim_Player/BepInEx/config/warpalicious.More_World_Locations_LootLists_cleaned.yml'

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Split content into lines
lines = content.split('\n')
cleaned_lines = []
skip_group = False
current_group = None

for i, line in enumerate(lines):
    # Check if this line starts a new group (ends with ':' and not indented)
    if line and not line.startswith(' ') and line.endswith(':'):
        group_name = line[:-1]  # Remove the ':'
        
        if group_name in groups_to_remove:
            skip_group = True
            current_group = group_name
            print(f"Removing group: {group_name}")
            continue
        else:
            skip_group = False
            current_group = group_name
    
    # If we're not skipping and it's not the start of a group to remove, keep the line
    if not skip_group:
        cleaned_lines.append(line)

# Join lines back together
cleaned_content = '\n'.join(cleaned_lines)

# Remove any excessive blank lines (more than 2 consecutive)
cleaned_content = re.sub(r'\n\n\n+', '\n\n\n', cleaned_content)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(cleaned_content)

print(f"Cleaned YAML file saved as: {output_file}")
print(f"Removed {len(groups_to_remove)} old loot groups")
