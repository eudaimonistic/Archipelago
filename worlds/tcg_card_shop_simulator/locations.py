from typing import cast

from .data.LocationData import *

PLAY_TABLE_START_ID = 300
LEVEL_START_ID = 200
BULK_BOX_TETRA = 4000
BULK_BOX_DESTINY = 4020
CARD_OPEN_START_ID = 1000
CARD_SELL_START_ID = 500
CARD_GRADE_START_ID = 2000
SELL_CHECK_START_ID = 3000


def get_sell_loc(key):
    for d in (tt_locations, pg1_locations, pg2_locations, pg3_locations):
        if key in d:
            return d[key]
    return None

def get_shop_locations(world):
    return [pg1_locations.copy(), pg2_locations.copy(), pg3_locations.copy(), tt_locations.copy()]

def get_license_checks(world,item_key:str ,loc: ShopLocation, is_starting_item:bool = False):
    if item_key is None or loc is None:
        return {}
    return get_license_checks_internal(world.options.sell_check_amount.value,world.options.extra_starting_item_checks.value,
                                item_key, loc, is_starting_item)

def get_license_checks_internal(check_amount, starting_num, item_key:str ,loc: ShopLocation, is_starting_item:bool = False):
    sell_item_locs = {}
    for n in range(1, check_amount + (starting_num if is_starting_item else 0) + 1):
        sell_item_locs[f"Sell {n} {"Boxes" if n>1 else "Box"} of {item_key}"] = SELL_CHECK_START_ID + (loc.code * 16) + (n-1)
    return sell_item_locs

def get_play_table_checks(world, game_format: Format):
    return get_play_table_checks_internal(world.options.play_table_checks.value, game_format)

def get_play_table_checks_internal(game_check_count: int, gameformat: Format):
    play_table_locs = {}
    if game_check_count > 0:
        if gameformat == Format.NoFormat:
            for i in range(game_check_count):
                name = f"Play {i + 1} Event Games"
                hex_id = PLAY_TABLE_START_ID + gameformat.value * 15 + i
                play_table_locs[name] = hex_id

            return play_table_locs

        for i in range(game_check_count):
            name = f"Play {i + 1} Format {gameformat.name}"
            hex_id = PLAY_TABLE_START_ID + gameformat.value * 15 + i
            play_table_locs[name] = hex_id

    return play_table_locs

def get_level_checks(world, region_level, final_region: bool = False):
    return get_level_checks_internal(region_level, final_region, world.options.goal.value)

def get_level_checks_internal( region_level, final_region: bool = False, goal = 1):
    level_locs = {}
    if final_region:
        if goal == 0:
            level_locs[f"Level {region_level}"] = None
        else:
            level_locs[f"Level {region_level}"] = LEVEL_START_ID+region_level-1
        return level_locs


    end_level = region_level+5
    if region_level == 1:
        end_level = 5

    if region_level == 100:
        end_level = 101
    for l in range(region_level, end_level):
        if l == 1:
            continue
        level_locs[f"Level {l}"] = LEVEL_START_ID+l-1
    return level_locs

def decode_card(num):
    if not num:
        return None
    if (num & 0x10000) == 0:
        return None

    # Extract values
    expansion = (num >> 12) & 0xF
    border = (num >> 8) & 0xF
    foil = (num >> 7) & 0x1
    index = (num & 0x7F) - 1

    return expansion, border, foil, index

def generate_card(name, index, border, foil, expansion, rarity):
    return f"{name} {border.name} {'Foil' if foil else 'NonFoil'} {expansion.name}", 0x10000 | (expansion.value << 12) | (border.value << 8) | (foil << 7) | (index + 1)

def get_card_checks(world, card_region: int):
    ach, locations = get_card_checks_internal(world.options.card_sanity.value,
                                    world.options.checks_opening_difficulty.value, card_region, True, world)
    world.open_achievements.extend(ach)
    return locations

def get_card_checks_internal(card_sanity, difficulty: int, card_region: int, create_hints:bool = False, world = None):
    card_locs = {}
    if difficulty == 0:
        return card_locs

    expansion = Expansion(1 if card_region >= 4 else 0)
    rarity = Rarity((card_region % 4) + 1)

    if card_sanity > 0:
        for index, data in enumerate(card_rarity):
            data = cast(MonsterData, data)
            if data.rarity != rarity:
                continue
            for border in Border:
                if difficulty == 1 and border.value > 0:
                    continue
                if difficulty == 2 and border.value > 2:
                    continue
                if difficulty == 3 and border.value > 3:
                    continue

                name, code = generate_card(data.name, index, border, 0, expansion, rarity)
                card_locs[name] = code
                if create_hints and world:
                    world.hints[code] = f"Card is in {expansion.name} {rarity.name} Packs"
                if card_sanity == 2:
                    name, code = generate_card(data.name, index, border, 1, expansion, rarity)
                    card_locs[name] = code
                    if create_hints and world:
                        world.hints[code] = f"Card is in {expansion.name} {rarity.name} Packs"

    counter = CARD_OPEN_START_ID + rarity.value * 50 + expansion.value * 250

    ach_list: List[AchievementEntryJSON] = get_achievements_for_region(AchievementPrefix.Open, rarity, expansion, difficulty, counter)

    achievement_card_locs = {}
    for achievement in ach_list:

        achievement_card_locs[achievement["name"]] = achievement["id"]

    card_locs = card_locs | achievement_card_locs

    return ach_list, card_locs

def get_generic_open_card_checks(difficulty: int):
    return {}

def get_sell_card_checks(world, card_region: int):
    ach, locations = get_sell_card_checks_internal(world.options.checks_selling_difficulty.value, card_region)
    world.sell_achievements.extend(ach)
    return locations

def get_sell_card_checks_internal(difficulty:int, card_region: int):
    expansion = Expansion(1 if card_region >= 4 else 0)
    rarity = Rarity((card_region % 4) + 1)

    counter = CARD_SELL_START_ID + rarity.value * 50 + expansion.value * 250
    ach_list: List[AchievementEntryJSON] = get_achievements_for_region(AchievementPrefix.Sell, rarity, expansion, difficulty, counter)
    achievement_card_locs = {}
    for achievement in ach_list:
        achievement_card_locs[achievement["name"]] = achievement["id"]
    return ach_list, achievement_card_locs

def get_generic_sell_card_checks(difficulty: int):
    return {}

def get_grading_card_checks(world, card_region: int):
    ach, locations = get_grading_card_checks_internal(world.options.checks_grading_difficulty.value, card_region)
    world.grade_achievements.extend(ach)
    return locations

def get_grading_card_checks_internal(difficulty:int, card_region: int):
    expansion = Expansion(1 if card_region >= 4 else 0)
    rarity = Rarity((card_region % 4) + 1)

    counter = CARD_GRADE_START_ID + rarity.value * 50 + expansion.value * 250
    ach_list: List[AchievementEntryJSON] = get_achievements_for_region(AchievementPrefix.Grade, rarity, expansion, difficulty, counter)
    achievement_card_locs = {}
    for achievement in ach_list:
        achievement_card_locs[achievement["name"]] = achievement["id"]
    return ach_list, achievement_card_locs

def get_generic_grading_card_checks(difficulty: int):
    return {}

def get_bulk_box_checks(world, level_grouped_locs):
    has_tetramon = any(item_id in level_grouped_locs[0] for item_id in [190, 1, 2, 3, 4, 5, 6, 7])
    has_destiny = any(item_id in level_grouped_locs[0] for item_id in [8, 9, 10, 11, 12, 13, 14, 15])
    return get_bulk_box_checks_internal(world.options.bulk_box.value, world.options.sell_check_amount.value, has_tetramon, has_destiny)

def get_bulk_box_checks_internal(bulk_box_option, sell_check_amount, has_tetramon, has_destiny):

    sell_bulk_locs = {}
    if bulk_box_option > 0:
        for n in range(1, sell_check_amount + 1):
            if has_tetramon:
                sell_bulk_locs[f"Sell {n} {"Boxes" if n > 1 else "Box"} of Tetramon Bulk Box"] = BULK_BOX_TETRA + n
            if has_destiny:
                sell_bulk_locs[f"Sell {n} {"Boxes" if n > 1 else "Box"} of Destiny Bulk Box"] = BULK_BOX_DESTINY + n
    return sell_bulk_locs

def get_all_locations():
    all_locations = {}

    for card_region_id in range(8):
        ach, open_ach_locs = get_card_checks_internal(2, 4, card_region_id, True)
        all_locations.update(open_ach_locs)
        ach, sell_ach_locs = get_sell_card_checks_internal(4, card_region_id)
        all_locations.update(sell_ach_locs)
        ach, grade_ach_locs = get_grading_card_checks_internal(4, card_region_id)
        all_locations.update(grade_ach_locs)

    all_locations.update(get_generic_sell_card_checks(4))
    all_locations.update(get_generic_grading_card_checks(4))

    for l in range(0, 105, 5):
        if l == 0:
            all_locations.update(get_level_checks_internal(1))
            continue
        all_locations.update(get_level_checks_internal(l))

    all_locations.update(get_play_table_checks_internal(15, Format.Standard))
    all_locations.update(get_play_table_checks_internal(15, Format.Pauper))
    all_locations.update(get_play_table_checks_internal(15, Format.FireCup))
    all_locations.update(get_play_table_checks_internal(15, Format.EarthCup))
    all_locations.update(get_play_table_checks_internal(15, Format.WaterCup))
    all_locations.update(get_play_table_checks_internal(15, Format.WindCup))
    all_locations.update(get_play_table_checks_internal(15, Format.FirstEditionVintage))
    all_locations.update(get_play_table_checks_internal(15, Format.SilverBorder))
    all_locations.update(get_play_table_checks_internal(15, Format.GoldBorder))
    all_locations.update(get_play_table_checks_internal(15, Format.ExBorder))
    all_locations.update(get_play_table_checks_internal(15, Format.FullArtBorder))
    all_locations.update(get_play_table_checks_internal(15, Format.Foil))
    all_locations.update(get_play_table_checks_internal(15, Format.NoFormat))

    for item_key, item_data in pg1_locations.items():
        license_checks = get_license_checks_internal(16, 2, item_key, item_data)
        all_locations.update(license_checks)

    for item_key, item_data in pg2_locations.items():
        license_checks = get_license_checks_internal(16, 2, item_key, item_data)
        all_locations.update(license_checks)

    for item_key, item_data in pg3_locations.items():
        license_checks = get_license_checks_internal(16, 2, item_key, item_data)
        all_locations.update(license_checks)

    for item_key, item_data in tt_locations.items():
        license_checks = get_license_checks_internal(16, 2, item_key, item_data)
        all_locations.update(license_checks)

    all_locations.update(get_bulk_box_checks_internal(1, 16, True, True))
    return all_locations