from __future__ import annotations
import json
import re
from typing import Iterable, Dict, List, Tuple
from ..models import MaterialMetric
from .base import Parser

class RelicHeimLootParser(Parser):
    source_type = "relicheim_loot"
    exts = (".json",)
    
    def parse(self, path: str, materials: set[str], aliases: dict[str, str]) -> Iterable[MaterialMetric]:
        """Parse RelicHeim loot configuration files and calculate actual drop rates"""
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return []
        
        out = []
        
        # Check if this is a RelicHeim loot file
        if not self._is_relicheim_loot_file(data):
            return []
        
        # Parse loot tables and calculate drop rates
        loot_tables = self._extract_loot_tables(data)
        drop_rates = self._calculate_drop_rates(loot_tables, materials, aliases)
        
        # Create MaterialMetric objects
        for material, rate in drop_rates.items():
            out.append(MaterialMetric(
                material=material,
                source=self.source_type,
                file_path=path,
                weight=rate,
                chance=rate
            ))
        
        return out
    
    def _is_relicheim_loot_file(self, data: dict) -> bool:
        """Check if this is a RelicHeim loot configuration file"""
        # Look for RelicHeim-specific patterns
        if "TargetFile" in data and "loottables.json" in data.get("TargetFile", ""):
            return True
        
        # Look for RelicHeim patches
        if "Patches" in data:
            for patch in data["Patches"]:
                if "Path" in patch and "ItemSets" in patch.get("Path", ""):
                    return True
        
        return False
    
    def _extract_loot_tables(self, data: dict) -> Dict[str, Dict[str, float]]:
        """Extract loot tables from RelicHeim configuration"""
        loot_tables = {}
        
        if "Patches" not in data:
            return loot_tables
        
        for patch in data["Patches"]:
            if patch.get("Path") == "$.ItemSets" and patch.get("Action") == "AppendAll":
                for item_set in patch.get("Value", []):
                    if "Name" in item_set and "Loot" in item_set:
                        table_name = item_set["Name"]
                        loot_items = {}
                        
                        for loot_item in item_set["Loot"]:
                            if "Item" in loot_item:
                                item_name = loot_item["Item"]
                                weight = loot_item.get("Weight", 1.0)
                                loot_items[item_name] = weight
                        
                        loot_tables[table_name] = loot_items
        
        return loot_tables
    
    def _calculate_drop_rates(self, loot_tables: Dict[str, Dict[str, float]], 
                            materials: set[str], aliases: dict[str, str]) -> Dict[str, float]:
        """Calculate actual drop rates for materials based on RelicHeim weight system"""
        material_rates = {}
        
        # Define the tier weights from RelicHeim baseline
        tier_weights = {
            "MaterialsA": 2.0,      # Magic tier
            "MaterialsB": 1.0,      # Rare tier
            "MaterialsC": 0.6,      # Epic tier
            "MaterialsD": 0.3,      # Legendary tier
            "MaterialsF": 0.1       # Mythic tier
        }
        
        # Process each loot table
        for table_name, items in loot_tables.items():
            # Check if this is a tiered materials table
            if table_name in tier_weights:
                tier_weight = tier_weights[table_name]
                
                # Each tier contains 4 materials (Dust, Runestone, Shard, Essence)
                # Each material has equal probability within the tier
                material_weight = tier_weight / 4.0
                
                for item_name in items:
                    # Check if this is a material we're tracking
                    material = aliases.get(item_name, item_name)
                    if material in materials:
                        if material not in material_rates:
                            material_rates[material] = 0.0
                        material_rates[material] += material_weight
            
            # Check if this is a composite table (like MagicMaterials)
            elif any(tier in items for tier in tier_weights.keys()):
                total_weight = sum(items.values())
                
                for tier_name, tier_weight in items.items():
                    if tier_name in tier_weights:
                        # Calculate the contribution of this tier
                        tier_contribution = (tier_weight / total_weight) * tier_weights[tier_name]
                        material_weight = tier_contribution / 4.0  # 4 materials per tier
                        
                        # Map tier to materials
                        tier_materials = self._get_tier_materials(tier_name)
                        for material in tier_materials:
                            if material in materials:
                                if material not in material_rates:
                                    material_rates[material] = 0.0
                                material_rates[material] += material_weight
        
        return material_rates
    
    def _get_tier_materials(self, tier_name: str) -> List[str]:
        """Get the materials associated with a tier"""
        tier_materials = {
            "MaterialsA": ["DustMagic", "RunestoneMagic", "ShardMagic", "EssenceMagic"],
            "MaterialsB": ["DustRare", "RunestoneRare", "ShardRare", "EssenceRare"],
            "MaterialsC": ["DustEpic", "RunestoneEpic", "ShardEpic", "EssenceEpic"],
            "MaterialsD": ["DustLegendary", "RunestoneLegendary", "ShardLegendary", "EssenceLegendary"],
            "MaterialsF": ["DustMythic", "RunestoneMythic", "ShardMythic", "EssenceMythic"]
        }
        
        return tier_materials.get(tier_name, [])
