import re
from enum import IntEnum

from BaseClasses import Region, Entrance, LocationProgressType
from . import locations
from .locations import *

class CardRegion(IntEnum):
    BASIC = 0
    RARE = 1
    EPIC = 2
    LEGENDARY = 3
    DESTINY_BASIC = 4
    DESTINY_RARE = 5
    DESTINY_EPIC = 6
    DESTINY_LEGENDARY = 7

card_region_names = {
    CardRegion.BASIC: "Basic Card Pack",
    CardRegion.RARE: "Rare Card Pack",
    CardRegion.EPIC: "Epic Card Pack",
    CardRegion.LEGENDARY: "Legendary Card Pack",
    CardRegion.DESTINY_BASIC: "Destiny Basic Card Pack",
    CardRegion.DESTINY_RARE: "Destiny Rare Card Pack",
    CardRegion.DESTINY_EPIC: "Destiny Epic Card Pack",
    CardRegion.DESTINY_LEGENDARY: "Destiny Legendary Card Pack",
}

def create_location(world, region, name: str, code: int, excluded: bool = False):
    location = Location(world.player, name, code, region)
    if excluded:
        location.progress_type = LocationProgressType.EXCLUDED
    region.locations.append(location)

def add_locations(world, region, locations_dict):
    for (key, code) in locations_dict.items():
        create_location(world, region, key, code, False)

def create_card_locations(world, card_locs, region):
    for (key, data) in card_locs.items():
        if data.region != region.name:
            continue
        create_location(world, region, key, data.code, False)

def create_region(world, name: str, hint: str, locations_dict):
    region = Region(name, world.player, world.multiworld)
    add_locations(world, region, locations_dict)
    world.multiworld.regions.append(region)
    return region

def assign_random_level_location(world, region, shop_locs: list[dict[str, ShopLocation]], level_grouped_locs, shop_id, level):
    available_keys = list(shop_locs[shop_id].keys())
    if len(available_keys) == 0:
        return None, None
    random_key = world.random.choice(available_keys)
    #force cleanser to be in or before level 10
    if shop_id == 1 and level < 10 and "Cleanser" in shop_locs[shop_id]:
        if world.random.random() < 0.40:
            random_key = "Cleanser"
    else:
        if shop_id == 1 and "Cleanser" in shop_locs[shop_id]:
            random_key = "Cleanser"

    #if Card shop, reroll if key is a deck for shits and giggles to increase odds of card packs
    if shop_id == 0 and pg1_locations["Fire Battle Deck"].code <=shop_locs[shop_id][random_key].code <= pg1_locations["Wind Destiny Deck"].code:
        random_key = world.random.choice(available_keys)

    loc:ShopLocation = shop_locs[shop_id].pop(random_key)
    if loc.code not in level_grouped_locs[shop_id]:
        level_grouped_locs[shop_id][loc.code] = level

        return random_key, loc
    level_grouped_locs[shop_id].pop(loc.code)
    level_grouped_locs[shop_id][loc.code] = level
    return None, None


def create_level_region(world, name: str, hint: str, shop_locs: list[dict[str, ShopLocation]], level_grouped_locs, starting_region:bool = False, final_region:bool = False):
    region = Region(name, world.player, world.multiworld)
    match = re.search(r'\d+', name)
    level_number = int(match.group(0))

    if not final_region:
        licenses_per_region = world.options.licenses_per_region.value
        shop_order = [0, 1, 2, 3]  # shop 3 is TT
        assigned_locations = []

        shop_index = 0
        for i in range(licenses_per_region):
            shop_id = shop_order[shop_index % len(shop_order)]
            key, loc = assign_random_level_location(world, region, shop_locs, level_grouped_locs, shop_id, level_number)

            if key is not None and loc is not None:
                assigned_locations.append((key, loc, shop_id))
                if key.endswith(" Box"):
                    key2 = key[:-4] + " Pack"

                    loc2 = get_sell_loc(key2)
                    if loc2 is not None and loc2.code not in level_grouped_locs[shop_id]:
                        shop_locs[shop_id].pop(key2, None)
                        level_grouped_locs[shop_id][loc2.code] = level_number
                        assigned_locations.append((key2, loc2, shop_id))
            shop_index += 1

        # Add assigned locations to the region
        starting_assigned = []
        for idx, (key, loc, shop_id) in enumerate(assigned_locations):
            is_starting = starting_region and shop_id in [0, 1, 2] and len(world.starting_item_ids) < 3 and shop_id not in starting_assigned
            if is_starting:
                starting_assigned.append(shop_id)
            add_locations(world, region, locations.get_license_checks(world, key, loc, is_starting))
            if is_starting:
                world.starting_item_ids.append(loc.code)
    elif world.options.goal.value == 1:
        #If in collection goal, make sure any packs not in the world are at the final region
        shop_id = 0
        for name, loc in list(shop_locs[0].items()):
            if "Pack" not in name:
                continue

            box_name = name.replace("Pack", "Box")

            # Check if the pair is complete
            if box_name in shop_locs[0]:
                if loc.code not in level_grouped_locs[shop_id]:
                    shop_locs[shop_id].pop(name)
                    level_grouped_locs[shop_id][loc.code] = level_number
                    add_locations(world, region, locations.get_license_checks(world, name, loc))

    add_locations(world, region, locations.get_level_checks(world, level_number, final_region))

    world.multiworld.regions.append(region)
    return region

def create_pack_regions(world, card_region: CardRegion, hint: str, level, is_destiny: bool):
    if level is not None:
        create_region(world, card_region_names[card_region], hint, get_card_checks(world, card_region.value))
        if world.options.checks_selling_difficulty.value > 0:
            create_region(world, f"Sell {card_region_names[card_region]}" , f"Sell {card_region_names[card_region]}", locations.get_sell_card_checks(world, card_region.value))
        if world.options.checks_grading_difficulty.value > 0:
            create_region(world, f"Grade {card_region_names[card_region]}" , f"Grade {card_region_names[card_region]}", locations.get_grading_card_checks(world, card_region.value))


def create_regions(world):
    shop_locs: list[dict[str, ShopLocation]] = locations.get_shop_locations(world)
    level_grouped_locs: [list[dict[int, int]]] = [{},{},{},{}]

    create_region(world, "Menu", "Menu Region", {})
    for l in range(0,world.options.max_level.value+5, 5):
        if l == 0:
            create_level_region(world, "Level 1-4", "Level 1-4", shop_locs, level_grouped_locs, True)
            continue
        if world.options.max_level.value == l:
            if l == 100:
                create_level_region(world, "Level 100", "Level 100", shop_locs, level_grouped_locs, final_region=True)
            else:
                create_level_region(world, f"Level {l}-{l + 4}", f"Level {l}-{l + 4}", shop_locs, level_grouped_locs, final_region=True)
            continue
        create_level_region(world, f"Level {l}-{l+4}", f"Level {l}-{l+4}", shop_locs, level_grouped_locs)

    if world.options.checks_opening_difficulty > 0:
        create_pack_regions(world, CardRegion.BASIC, card_region_names[CardRegion.BASIC], min([level_grouped_locs[0][item_id] for item_id in [190, 1] if item_id in level_grouped_locs[0]], default=None), False)
        create_pack_regions(world, CardRegion.RARE, card_region_names[CardRegion.RARE], min([level_grouped_locs[0][item_id] for item_id in [2, 3] if item_id in level_grouped_locs[0]], default=None), False)
        create_pack_regions(world, CardRegion.EPIC, card_region_names[CardRegion.EPIC], min([level_grouped_locs[0][item_id] for item_id in [4, 5] if item_id in level_grouped_locs[0]], default=None), False)
        create_pack_regions(world, CardRegion.LEGENDARY, card_region_names[CardRegion.LEGENDARY], min([level_grouped_locs[0][item_id] for item_id in [6, 7] if item_id in level_grouped_locs[0]], default=None), False)
        create_pack_regions(world, CardRegion.DESTINY_BASIC, card_region_names[CardRegion.DESTINY_BASIC], min([level_grouped_locs[0][item_id] for item_id in [8, 9] if item_id in level_grouped_locs[0]], default=None), True)
        create_pack_regions(world, CardRegion.DESTINY_RARE, card_region_names[CardRegion.DESTINY_RARE], min([level_grouped_locs[0][item_id] for item_id in [10, 11] if item_id in level_grouped_locs[0]], default=None), True)
        create_pack_regions(world, CardRegion.DESTINY_EPIC, card_region_names[CardRegion.DESTINY_EPIC], min([level_grouped_locs[0][item_id] for item_id in [12, 13] if item_id in level_grouped_locs[0]], default=None), True)
        create_pack_regions(world, CardRegion.DESTINY_LEGENDARY, card_region_names[CardRegion.DESTINY_LEGENDARY], min([level_grouped_locs[0][item_id] for item_id in [14, 15] if item_id in level_grouped_locs[0]], default=None), True)
    if world.options.checks_selling_difficulty.value > 0:
        create_region(world, "Sell Cards", f"Sell Any Card",
                      locations.get_generic_sell_card_checks(world.options.checks_selling_difficulty.value))
    if world.options.checks_grading_difficulty.value > 0:
        create_region(world, "Grade Cards", f"Grade Any Card",
                     locations.get_generic_grading_card_checks(world.options.checks_grading_difficulty.value))

    if world.options.play_table_checks.value > 0:
        if world.options.no_formats:
            create_region(world, "Play Tables", "Play Tables", locations.get_play_table_checks(world, Format.NoFormat))
        else:
            create_region(world, "Play Tables", "Play Tables", {})
            create_region(world, "Standard Games", "Need Standard format", locations.get_play_table_checks(world, Format.Standard))
            create_region(world, "Pauper Games", "Need Pauper format", locations.get_play_table_checks(world, Format.Pauper))
            create_region(world, "FireCup Games", "Need FireCup format", locations.get_play_table_checks(world, Format.FireCup))
            create_region(world, "EarthCup Games", "Need EarthCup format", locations.get_play_table_checks(world, Format.EarthCup))
            create_region(world, "WaterCup Games", "Need WaterCup format", locations.get_play_table_checks(world, Format.WaterCup))
            create_region(world, "WindCup Games", "Need WindCup format", locations.get_play_table_checks(world, Format.WindCup))
            create_region(world, "First Edition Vintage Games", "Need First Edition Vintage format", locations.get_play_table_checks(world, Format.FirstEditionVintage))
            create_region(world, "Silver Border Games", "Need Silver Border format", locations.get_play_table_checks(world, Format.SilverBorder))
            create_region(world, "Gold Border Games", "Need Gold Border format", locations.get_play_table_checks(world, Format.GoldBorder))
            create_region(world, "Ex Border Games", "Need Ex Border format", locations.get_play_table_checks(world, Format.ExBorder))
            create_region(world, "Full Art Border Games", "Need Full Art Border format", locations.get_play_table_checks(world, Format.FullArtBorder))
            create_region(world, "Foil Games", "Need Foil format", locations.get_play_table_checks(world, Format.Foil))

    if world.options.bulk_box.value > 0:
        create_region(world, "Bulk Boxes", "Get Workbench", locations.get_bulk_box_checks(world, level_grouped_locs))

    return level_grouped_locs

def connect_regions(world, from_name: str, to_name: str, entrance_name: str) -> Entrance:
    entrance_region = world.get_region(from_name)
    exit_region = world.get_region(to_name)
    return entrance_region.connect(exit_region, entrance_name)

def connect_pack_region(world, card_region, itemids):
    if len(itemids) == 0:
        return

    for itemid in itemids:
        level = world.pg1_licenses[itemid]
        end_level = level+4 if level != 1 else 4
        item_name = world.item_id_to_name[itemid]
        entrance_name = item_name.replace("Progressive ", "")
        connect_regions(world, f"Level {level}-{end_level}", card_region_names[card_region], entrance_name)
    if world.options.checks_selling_difficulty.value > 0:
        connect_regions(world,  card_region_names[card_region], f"Sell {card_region_names[card_region]}",f"Sell {card_region_names[card_region]}")
        connect_regions(world, card_region_names[card_region],"Sell Cards",  f"Generic Sell {card_region_names[card_region]}")
    if world.options.checks_grading_difficulty.value > 0:
        connect_regions(world, card_region_names[card_region], f"Grade {card_region_names[card_region]}",f"Grade {card_region_names[card_region]}")
        connect_regions(world, card_region_names[card_region], "Grade Cards",f"Generic Grade {card_region_names[card_region]}")

def connect_sell_region(world, region_name, level):
    if level is None:
        return
    end_level = level + 4 if level != 1 else 4
    connect_regions(world, f"Level {level}-{end_level}", region_name, region_name)

def connect_entrances(world):
    if world.options.checks_opening_difficulty > 0:
        connect_pack_region(world, CardRegion.BASIC, [item_id for item_id in [190,1] if item_id in world.pg1_licenses])
        connect_pack_region(world, CardRegion.RARE, [item_id for item_id in [2,3] if item_id in world.pg1_licenses])
        connect_pack_region(world, CardRegion.EPIC, [item_id for item_id in [4,5] if item_id in world.pg1_licenses])
        connect_pack_region(world, CardRegion.LEGENDARY, [item_id for item_id in [6,7] if item_id in world.pg1_licenses])
        connect_pack_region(world, CardRegion.DESTINY_BASIC, [item_id for item_id in [8,9] if item_id in world.pg1_licenses])
        connect_pack_region(world, CardRegion.DESTINY_RARE, [item_id for item_id in [10,11] if item_id in world.pg1_licenses])
        connect_pack_region(world, CardRegion.DESTINY_EPIC, [item_id for item_id in [12,13] if item_id in world.pg1_licenses])
        connect_pack_region(world, CardRegion.DESTINY_LEGENDARY, [item_id for item_id in [14,15] if item_id in world.pg1_licenses])

    connect_regions(world, "Menu", "Level 1-4", "Level 1")
    if world.options.play_table_checks.value > 0:
        connect_regions(world, "Level 1-4", "Play Tables", "Play Table Found")
        if not world.options.no_formats:
            connect_regions(world, "Play Tables", "Standard Games", "Standard Games")
            connect_regions(world, "Play Tables", "Pauper Games", "Pauper Games")
            connect_regions(world, "Play Tables", "FireCup Games", "FireCup Games")
            connect_regions(world, "Play Tables", "EarthCup Games", "EarthCup Games")
            connect_regions(world, "Play Tables", "WaterCup Games", "WaterCup Games")
            connect_regions(world, "Play Tables", "WindCup Games", "WindCup Games")
            connect_regions(world, "Play Tables", "First Edition Vintage Games", "First Edition Vintage Games")
            connect_regions(world, "Play Tables", "Silver Border Games", "Silver Border Games")
            connect_regions(world, "Play Tables", "Gold Border Games", "Gold Border Games")
            connect_regions(world, "Play Tables", "Ex Border Games", "Ex Border Games")
            connect_regions(world, "Play Tables", "Full Art Border Games", "Full Art Border Games")
            connect_regions(world, "Play Tables", "Foil Games", "Foil Games")

    if world.options.bulk_box.value > 0:
        connect_regions(world, "Level 1-4", "Bulk Boxes", "WorkBench Found")

    for l in range(0,world.options.max_level.value, 5):
        if l == 0:
            connect_regions(world, "Level 1-4", "Level 5-9", "Level 5")
            continue
        if l == 95:
            connect_regions(world, "Level 95-99", "Level 100", "Level 100")
            continue
        connect_regions(world, f"Level {l}-{l+4}", f"Level {l+5}-{l+5+4}", f"Level {l+5}")


def ut_recreate_regions(world, pg1_licenses, pg2_licenses, pg3_licenses, tt_licenses):
    shop_locs: list[dict[str, ShopLocation]] = locations.get_shop_locations(world)
    level_grouped_locs: [list[dict[int, int]]] = [{}, {}, {}, {}]
    level_grouped_locs[0] = pg1_licenses
    level_grouped_locs[1] = pg2_licenses
    level_grouped_locs[2] = pg3_licenses
    level_grouped_locs[3] = tt_licenses

    create_region(world, "Menu", "Menu Region", {})
    for l in range(0, world.options.max_level.value + 5, 5):
        if l == 0:
            ut_recreate_level_region(world, "Level 1-4", "Level 1-4", shop_locs, level_grouped_locs, True)
            continue
        if world.options.max_level.value == l:
            if l == 100:
                ut_recreate_level_region(world, "Level 100", "Level 100", shop_locs, level_grouped_locs, final_region=True)
            else:
                ut_recreate_level_region(world, f"Level {l}-{l + 4}", f"Level {l}-{l + 4}",shop_locs, level_grouped_locs,
                                    final_region=True)
            continue
        ut_recreate_level_region(world, f"Level {l}-{l + 4}", f"Level {l}-{l + 4}", shop_locs, level_grouped_locs)
    if world.options.checks_opening_difficulty > 0:
        create_pack_regions(world, CardRegion.BASIC, card_region_names[CardRegion.BASIC],
                            min([level_grouped_locs[0][item_id] for item_id in [190, 1] if
                                 item_id in level_grouped_locs[0]], default=None), False)
        create_pack_regions(world, CardRegion.RARE, card_region_names[CardRegion.RARE],
                            min([level_grouped_locs[0][item_id] for item_id in [2, 3] if item_id in level_grouped_locs[0]],
                                default=None), False)
        create_pack_regions(world, CardRegion.EPIC, card_region_names[CardRegion.EPIC],
                            min([level_grouped_locs[0][item_id] for item_id in [4, 5] if item_id in level_grouped_locs[0]],
                                default=None), False)
        create_pack_regions(world, CardRegion.LEGENDARY, card_region_names[CardRegion.LEGENDARY],
                            min([level_grouped_locs[0][item_id] for item_id in [6, 7] if item_id in level_grouped_locs[0]],
                                default=None), False)
        create_pack_regions(world, CardRegion.DESTINY_BASIC, card_region_names[CardRegion.DESTINY_BASIC],
                            min([level_grouped_locs[0][item_id] for item_id in [8, 9] if item_id in level_grouped_locs[0]],
                                default=None), True)
        create_pack_regions(world, CardRegion.DESTINY_RARE, card_region_names[CardRegion.DESTINY_RARE],
                            min([level_grouped_locs[0][item_id] for item_id in [10, 11] if
                                 item_id in level_grouped_locs[0]], default=None), True)
        create_pack_regions(world, CardRegion.DESTINY_EPIC, card_region_names[CardRegion.DESTINY_EPIC],
                            min([level_grouped_locs[0][item_id] for item_id in [12, 13] if
                                 item_id in level_grouped_locs[0]], default=None), True)
        create_pack_regions(world, CardRegion.DESTINY_LEGENDARY, card_region_names[CardRegion.DESTINY_LEGENDARY],
                            min([level_grouped_locs[0][item_id] for item_id in [14, 15] if
                                 item_id in level_grouped_locs[0]], default=None), True)
    if world.options.checks_selling_difficulty.value > 0:
        create_region(world, "Sell Cards", f"Sell Any Card",
                      locations.get_generic_sell_card_checks(world.options.checks_selling_difficulty.value))
    if world.options.checks_grading_difficulty.value > 0:
        create_region(world, "Grade Cards", f"Grade Any Card",
                      locations.get_generic_grading_card_checks(world.options.checks_grading_difficulty.value))

    if world.options.play_table_checks.value > 0:
        if world.options.no_formats:
            create_region(world, "Play Tables", "Play Tables", locations.get_play_table_checks(world, Format.NoFormat))
        else:
            create_region(world, "Play Tables", "Play Tables", {})
            create_region(world, "Standard Games", "Need Standard format",
                          locations.get_play_table_checks(world, Format.Standard))
            create_region(world, "Pauper Games", "Need Pauper format",
                          locations.get_play_table_checks(world, Format.Pauper))
            create_region(world, "FireCup Games", "Need FireCup format",
                          locations.get_play_table_checks(world, Format.FireCup))
            create_region(world, "EarthCup Games", "Need EarthCup format",
                          locations.get_play_table_checks(world, Format.EarthCup))
            create_region(world, "WaterCup Games", "Need WaterCup format",
                          locations.get_play_table_checks(world, Format.WaterCup))
            create_region(world, "WindCup Games", "Need WindCup format",
                          locations.get_play_table_checks(world, Format.WindCup))
            create_region(world, "First Edition Vintage Games", "Need First Edition Vintage format",
                          locations.get_play_table_checks(world, Format.FirstEditionVintage))
            create_region(world, "Silver Border Games", "Need Silver Border format",
                          locations.get_play_table_checks(world, Format.SilverBorder))
            create_region(world, "Gold Border Games", "Need Gold Border format",
                          locations.get_play_table_checks(world, Format.GoldBorder))
            create_region(world, "Ex Border Games", "Need Ex Border format",
                          locations.get_play_table_checks(world, Format.ExBorder))
            create_region(world, "Full Art Border Games", "Need Full Art Border format",
                          locations.get_play_table_checks(world, Format.FullArtBorder))
            create_region(world, "Foil Games", "Need Foil format", locations.get_play_table_checks(world, Format.Foil))

    if world.options.bulk_box.value > 0:
        create_region(world, "Bulk Boxes", "Get Workbench", locations.get_bulk_box_checks(world, level_grouped_locs))



def ut_recreate_level_region(world, name: str, hint: str, shop_locs: list[dict[str, ShopLocation]],level_grouped_locs, starting_region:bool = False, final_region:bool = False):
    region = Region(name, world.player, world.multiworld)
    match = re.search(r'\d+', name)
    level_number = int(match.group(0))

    shop_order = [0, 1, 2, 3]  # shop 3 is TT

    if not final_region:
        starting_assigned = []
        for shop_id in shop_order:
            for code, level in level_grouped_locs[shop_id].items():
                if level != level_number:
                    continue
                loc = ShopLocation(code)
                key = next(
                    (k for k, v in shop_locs[shop_id].items() if v.code == code),
                    None
                )
                #print(world.starting_item_ids)
                add_locations(world, region, locations.get_license_checks(world, key, loc, loc.code in world.starting_item_ids))

    add_locations(world, region, locations.get_level_checks(world, level_number, final_region))

    world.multiworld.regions.append(region)
    return region