
from __future__ import annotations
from .parsers.epicloot_cfg import EpicLootChestCfg
from .parsers.drop_that import DropThatListCfg, DropThatCharCfg
from .parsers.world_locations_yml import WorldLocationsYml
from .parsers.epicloot_json import EpicLootJson
from .parsers.backpack_cfg import BackpacksCfg
from .parsers.relicheim_loot import RelicHeimLootParser

ALL_PARSERS = [EpicLootChestCfg(), DropThatListCfg(), DropThatCharCfg(), WorldLocationsYml(), EpicLootJson(), BackpacksCfg(), RelicHeimLootParser()]

# Create a mapping from source_type to parser class
PARSERS = {parser.source_type: type(parser) for parser in ALL_PARSERS}
