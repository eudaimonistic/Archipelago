from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple, List, Optional, TypedDict
from BaseClasses import Location

class TCGSimulatorLocation(Location):
    game: str = "TCG Card Shop Simulator"


class LocData(NamedTuple):
    code: Optional[int]
    region: Optional[str]


@dataclass
class ShopLocation:
    code: int

@dataclass
class NamedItem:
    name: str
    id: int
    locData: LocData

class AchievementEntryJSON(TypedDict):
    type: str
    name: str
    difficulty: int
    threshold: int
    rarity: List[int]
    border: List[int]
    expansion: List[int]
    foil: List[int]
    id: int

pg1_locations: dict[str,ShopLocation] = {
    "Basic Card Pack": ShopLocation(190),#game id 0
    "Basic Card Box": ShopLocation(1),
    "Rare Card Pack": ShopLocation(2),
    "Rare Card Box": ShopLocation(3),
    "Epic Card Pack": ShopLocation(4),
    "Epic Card Box": ShopLocation(5),
    "Legendary Card Pack": ShopLocation(6),
    "Legendary Card Box": ShopLocation(7),
    "Basic Destiny Pack": ShopLocation(8),
    "Basic Destiny Box": ShopLocation(9),
    "Rare Destiny Pack": ShopLocation(10),
    "Rare Destiny Box": ShopLocation(11),
    "Epic Destiny Pack": ShopLocation(12),
    "Epic Destiny Box": ShopLocation(13),
    "Legendary Destiny Pack": ShopLocation(14),
    "Legendary Destiny Box": ShopLocation(15),
    "Fire Battle Deck": ShopLocation(55),
    "Earth Battle Deck": ShopLocation(56),
    "Water Battle Deck": ShopLocation(57),
    "Wind Battle Deck": ShopLocation(58),
    "Fire Destiny Deck": ShopLocation(59),
    "Earth Destiny Deck": ShopLocation(60),
    "Water Destiny Deck": ShopLocation(61),
    "Wind Destiny Deck": ShopLocation(62),
}
pg2_locations: dict[str,ShopLocation] = {
    "Cleanser": ShopLocation(23),
    "Card Sleeves (Clear)": ShopLocation(63),
    "Card Sleeves (Tetramon)": ShopLocation(64),
    "D20 Dice Red": ShopLocation(29),
    "D20 Dice Blue": ShopLocation(30),
    "D20 Dice Black": ShopLocation(31),
    "D20 Dice White": ShopLocation(32),
    "Card Sleeves (Fire)": ShopLocation(65),
    "Card Sleeves (Earth)": ShopLocation(66),
    "Card Sleeves (Water)": ShopLocation(67),
    "Card Sleeves (Wind)": ShopLocation(68),
    "Deck Box Red": ShopLocation(24),
    "Deck Box Green": ShopLocation(25),
    "Deck Box Blue": ShopLocation(26),
    "Deck Box Yellow": ShopLocation(27),
    "Collection Book": ShopLocation(28),
    "Premium Collection Book": ShopLocation(54),
    "Playmat (Drilceros)": ShopLocation(71),
    "Playmat (Clamigo)": ShopLocation(69),
    "Playmat (Wispo)": ShopLocation(75),
    "Playmat (Lunight)": ShopLocation(83),
    "Playmat (Kyrone)": ShopLocation(78),
    "Playmat (Duel)": ShopLocation(70),
    "Playmat (Dracunix1)": ShopLocation(74),
    "Playmat (The Four Dragons)": ShopLocation(73),
    "Playmat (Drakon)": ShopLocation(72),
    "Playmat (GigatronX Evo)": ShopLocation(76),
    "Playmat (Fire)": ShopLocation(79),
    "Playmat (Earth)": ShopLocation(80),
    "Playmat (Water)": ShopLocation(82),
    "Playmat (Wind)": ShopLocation(81),
    "Playmat (Tetramon)": ShopLocation(77),
    "Playmat (Dracunix2)": ShopLocation(109),
    "Playmat (GigatronX)": ShopLocation(110),
    "Playmat (Katengu Black)": ShopLocation(111),
    "Playmat (Katengu White)": ShopLocation(112),
    "Manga 1": ShopLocation(95),
    "Manga 2": ShopLocation(96),
    "Manga 3": ShopLocation(97),
    "Manga 4": ShopLocation(98),
    "Manga 5": ShopLocation(99),
    "Manga 6": ShopLocation(100),
    "Manga 7": ShopLocation(101),
    "Manga 8": ShopLocation(102),
    "Manga 9": ShopLocation(103),
    "Manga 10": ShopLocation(104),
    "Manga 11": ShopLocation(105),
    "Manga 12": ShopLocation(106),
}
pg3_locations: dict[str,ShopLocation] = {
    "Pigni Plushie": ShopLocation(33),
    "Nanomite Plushie": ShopLocation(34),
    "Minstar Plushie": ShopLocation(35),
    "Nocti Plushie": ShopLocation(36),
    "Burpig Figurine": ShopLocation(39),
    "Decimite Figurine": ShopLocation(42),
    "Trickstar Figurine": ShopLocation(45),
    "Lunight Figurine": ShopLocation(48),
    "Inferhog Figurine": ShopLocation(40),
    "Meganite Figurine": ShopLocation(43),
    "Princestar Figurine": ShopLocation(46),
    "Vampicant Figurine": ShopLocation(49),
    "Blazoar Plushie": ShopLocation(41),
    "Giganite Statue": ShopLocation(44),
    "Kingstar Plushie": ShopLocation(47),
    "Dracunix Figurine": ShopLocation(50),
    "Bonfiox Plushie": ShopLocation(52),
    "Drilceros Action Figure": ShopLocation(51),
    "ToonZ Plushie": ShopLocation(53),
}
tt_locations: dict[str,ShopLocation] = {
    "Penny Sleeves": ShopLocation(118),
    "Tower Deckbox": ShopLocation(124),
    "Magnetic Holder": ShopLocation(113),
    "Toploader": ShopLocation(117),
    "Card Preserver": ShopLocation(114),
    "Playmat Gray": ShopLocation(119),
    "Playmat Green": ShopLocation(120),
    "Playmat Purple": ShopLocation(121),
    "Playmat Yellow": ShopLocation(122),
    "Pocket Pages": ShopLocation(115),
    "Card Holder": ShopLocation(116),
    "Collectors Album": ShopLocation(123),
    "System Gate #1": ShopLocation(87),
    "System Gate #2": ShopLocation(88),
    "Mafia Works": ShopLocation(86),
    "Necromonsters": ShopLocation(84),
    "Claim!": ShopLocation(85),
}


class Rarity(Enum):
    Common = 1
    Rare = 2
    Epic = 3
    Legendary = 4


class MonsterData(NamedTuple):
    name: str
    rarity: Rarity

class Difficulty(Enum):
    Easy = 1
    Medium = 2
    Hard = 3
    Impossible = 4




class Expansion(Enum):
    Tetramon = 0
    Destiny = 1


class Border(Enum):
    Base = 0
    FirstEdition = 1
    Silver = 2
    Gold = 3
    EX = 4
    FullArt = 5


class Foil(Enum):
    NonFoil = 0
    Foil = 1

class Format(Enum):
    Standard = 0
    Pauper = 1
    FireCup = 2
    EarthCup = 3
    WaterCup = 4
    WindCup = 5
    FirstEditionVintage = 6
    SilverBorder = 7
    GoldBorder = 8
    ExBorder = 9
    FullArtBorder = 10
    Foil = 11
    NoFormat = 12

class TCGAchievement(NamedTuple):
    name: str
    difficulty: Difficulty
    id: int
    borders: List[Border]
    foils: List[Foil]


card_rarity: List[MonsterData] = [
    MonsterData("Pigni", Rarity.Common),
    MonsterData("Burpig", Rarity.Rare),
    MonsterData("Inferhog", Rarity.Epic),
    MonsterData("Blazoar", Rarity.Legendary),
    MonsterData("Kidsune", Rarity.Common),
    MonsterData("Bonfiox", Rarity.Rare),
    MonsterData("Honobi", Rarity.Epic),
    MonsterData("Kyuenbi", Rarity.Legendary),
    MonsterData("Nanomite", Rarity.Common),
    MonsterData("Decimite", Rarity.Rare),
    MonsterData("Meganite", Rarity.Epic),
    MonsterData("Giganite", Rarity.Legendary),
    MonsterData("Sapoling", Rarity.Common),
    MonsterData("Forush", Rarity.Rare),
    MonsterData("Timbro", Rarity.Epic),
    MonsterData("Mammotree", Rarity.Legendary),
    MonsterData("Minstar", Rarity.Common),
    MonsterData("Trickstar", Rarity.Rare),
    MonsterData("Princestar", Rarity.Epic),
    MonsterData("Kingstar", Rarity.Legendary),
    MonsterData("Shellow", Rarity.Common),
    MonsterData("Clamigo", Rarity.Rare),
    MonsterData("Aquariff", Rarity.Epic),
    MonsterData("Fistronk", Rarity.Legendary),
    MonsterData("Wurmgle", Rarity.Common),
    MonsterData("Pupazz", Rarity.Rare),
    MonsterData("Mothini", Rarity.Epic),
    MonsterData("Royalama", Rarity.Legendary),
    MonsterData("Nocti", Rarity.Common),
    MonsterData("Lunight", Rarity.Rare),
    MonsterData("Vampicant", Rarity.Epic),
    MonsterData("Dracunix", Rarity.Legendary),
    MonsterData("Minotos", Rarity.Rare),
    MonsterData("Drilceros", Rarity.Epic),
    MonsterData("Grizzaw", Rarity.Epic),
    MonsterData("Jelicleen", Rarity.Rare),
    MonsterData("Wispo", Rarity.Rare),
    MonsterData("Mummog", Rarity.Rare),
    MonsterData("Helio", Rarity.Common),
    MonsterData("Pixy", Rarity.Rare),
    MonsterData("Flory", Rarity.Epic),
    MonsterData("Magnoria", Rarity.Legendary),
    MonsterData("Werboo", Rarity.Common),
    MonsterData("Flami", Rarity.Common),
    MonsterData("Angez", Rarity.Rare),
    MonsterData("Moskit", Rarity.Epic),
    MonsterData("Kyrone", Rarity.Common),
    MonsterData("Twofrost", Rarity.Rare),
    MonsterData("Threeze", Rarity.Epic),
    MonsterData("Hydroid", Rarity.Legendary),
    MonsterData("Drakon", Rarity.Legendary),
    MonsterData("Bogon", Rarity.Legendary),
    MonsterData("Hydron", Rarity.Legendary),
    MonsterData("Raizon", Rarity.Legendary),
    MonsterData("Tortugor", Rarity.Epic),
    MonsterData("Lupup", Rarity.Common),
    MonsterData("Luphire", Rarity.Rare),
    MonsterData("Lucinder", Rarity.Epic),
    MonsterData("Lucadence", Rarity.Legendary),
    MonsterData("Gupi", Rarity.Common),
    MonsterData("Sharfin", Rarity.Rare),
    MonsterData("Gilgabass", Rarity.Epic),
    MonsterData("Jigajawr", Rarity.Legendary),
    MonsterData("Batrang", Rarity.Common),
    MonsterData("Dusko", Rarity.Rare),
    MonsterData("Wolgin", Rarity.Epic),
    MonsterData("Jacktern", Rarity.Legendary),
    MonsterData("Tetron", Rarity.Common),
    MonsterData("Raxx", Rarity.Rare),
    MonsterData("Gannon", Rarity.Epic),
    MonsterData("GigatronX", Rarity.Legendary),
    MonsterData("Clawop", Rarity.Common),
    MonsterData("Clawdos", Rarity.Rare),
    MonsterData("Clawaken", Rarity.Epic),
    MonsterData("Clawcifear", Rarity.Legendary),
    MonsterData("Sunflork", Rarity.Common),
    MonsterData("Scarlios", Rarity.Rare),
    MonsterData("Scarkgorus", Rarity.Epic),
    MonsterData("Crobib", Rarity.Common),
    MonsterData("Crosilisk", Rarity.Rare),
    MonsterData("Crorathian", Rarity.Epic),
    MonsterData("Nimblis", Rarity.Common),
    MonsterData("Nimboculo", Rarity.Rare),
    MonsterData("Nimbustrike", Rarity.Epic),
    MonsterData("Esmeri", Rarity.Common),
    MonsterData("Esmerock", Rarity.Rare),
    MonsterData("Esmerdios", Rarity.Epic),
    MonsterData("Litspire", Rarity.Epic),
    MonsterData("Voltrex", Rarity.Legendary),
    MonsterData("Crablox", Rarity.Rare),
    MonsterData("Clawvenger", Rarity.Epic),
    MonsterData("Flambrolly", Rarity.Legendary),
    MonsterData("Lumie", Rarity.Rare),
    MonsterData("Seedant", Rarity.Common),
    MonsterData("Budwing", Rarity.Rare),
    MonsterData("Buzzeed", Rarity.Epic),
    MonsterData("Beakai", Rarity.Rare), #should be common, bad game
    MonsterData("Talontsu", Rarity.Epic), #should be rare bad game
    MonsterData("Talonika", Rarity.Epic),
    MonsterData("Talonryu", Rarity.Legendary),
    MonsterData("Kataryu", Rarity.Epic),
    MonsterData("Katengu", Rarity.Legendary),
    MonsterData("Mufflin", Rarity.Common),
    MonsterData("Muffleur", Rarity.Rare),
    MonsterData("Mufflimax", Rarity.Epic),
    MonsterData("Anguifish", Rarity.Common),
    MonsterData("Amneshark", Rarity.Rare),
    MonsterData("Amnesilla", Rarity.Epic),
    MonsterData("Frizard", Rarity.Rare),
    MonsterData("Gekoflare", Rarity.Epic),
    MonsterData("Terradrakon", Rarity.Legendary),
    MonsterData("Flamchik", Rarity.Common),
    MonsterData("Pyropeck", Rarity.Rare),
    MonsterData("Poseia", Rarity.Common),
    MonsterData("Posteed", Rarity.Rare),
    MonsterData("Poseigon", Rarity.Epic),
    MonsterData("Poseidrake", Rarity.Legendary),
    MonsterData("Sludglop", Rarity.Common),
    MonsterData("Sludgetox", Rarity.Rare),
    MonsterData("Toxigoop", Rarity.Epic),
    MonsterData("Toximuck", Rarity.Legendary),
]
int_to_card_region = {
    0:"Basic Card Pack",
    1:"Rare Card Pack",
    2:"Epic Card Pack",
    3:"Legendary Card Pack",
    4:"Destiny Basic Card Pack",
    5:"Destiny Rare Card Pack",
    6:"Destiny Epic Card Pack",
    7:"Destiny Legendary Card Pack"
}

class AchievementPrefix(Enum):
    Open = 0,
    Sell = 1,
    Grade = 2

def get_generic_action_achievement(startingid: int, prefix: AchievementPrefix, descriptor: str, rar: Rarity, borders: List[Border], foils: List[Foil],
                                   easy_num: int, med_num: int, hard_num: int, imp_num: int):
    """Generalized version for open/sell/grade actions."""
    return [
        TCGAchievement(f"{prefix.name} {easy_num} {descriptor} {rar.name} Cards", Difficulty.Easy, startingid, borders, foils),
        TCGAchievement(f"{prefix.name} {med_num} {descriptor} {rar.name} Cards", Difficulty.Medium, startingid+1, borders, foils),
        TCGAchievement(f"{prefix.name} {hard_num} {descriptor} {rar.name} Cards", Difficulty.Hard, startingid+2, borders, foils),
        TCGAchievement(f"{prefix.name} {imp_num} {descriptor} {rar.name} Cards", Difficulty.Impossible, startingid+3, borders, foils),
    ]

def get_region_action_achievements(prefix: AchievementPrefix, rar: Rarity, expansion: Expansion, startingid) -> List[TCGAchievement]:
    """Generalized for open/sell/grade types — avoids duplication."""
    achievements: List[TCGAchievement] = []
    if prefix == AchievementPrefix.Sell:
        startingid = startingid + 4
        achievements.extend(
            get_generic_action_achievement(startingid, prefix, expansion.name, rar, list(Border), list(Foil), 25, 50,
                                           100, 150, ))
        startingid = startingid + 4
        achievements.extend(
            get_generic_action_achievement(startingid, prefix, f"{Foil.Foil.name} {expansion.name}", rar, list(Border),
                                           [Foil.Foil], 10, 20, 50, 100))
        startingid = startingid + 4
        achievements.extend(
            get_generic_action_achievement(startingid, prefix, f"{Border.Base.name} {expansion.name}", rar,
                                           [Border.Base], list(Foil), 10, 20, 50, 100))
        startingid = startingid + 4
        achievements.extend(
            get_generic_action_achievement(startingid, prefix, f"{Border.FirstEdition.name} {expansion.name}", rar,
                                           [Border.FirstEdition], list(Foil), 10, 20, 50, 100))
        startingid = startingid + 4
        achievements.extend(
            get_generic_action_achievement(startingid, prefix, f"{Border.Silver.name} {expansion.name}", rar,
                                           [Border.Silver], list(Foil), 10, 20, 40, 80))
        startingid = startingid + 4
        achievements.extend(
            get_generic_action_achievement(startingid, prefix, f"{Border.Gold.name} {expansion.name}", rar,
                                           [Border.Gold], list(Foil), 10, 20, 40, 80))
        startingid = startingid + 4
        achievements.extend(
            get_generic_action_achievement(startingid, prefix, f"{Border.EX.name} {expansion.name}", rar, [Border.EX],
                                           list(Foil), 5, 10, 20, 50))
        startingid = startingid + 4
        achievements.extend(
            get_generic_action_achievement(startingid, prefix, f"{Border.FullArt.name} {expansion.name}", rar,
                                           [Border.FullArt], list(Foil), 5, 10, 20, 50))
    if prefix == AchievementPrefix.Grade:
        startingid = startingid + 4
        achievements.extend(
            get_generic_action_achievement(startingid, prefix, expansion.name, rar, list(Border), list(Foil), 10, 20,
                                           40, 80, ))
        startingid = startingid + 4
        achievements.extend(
            get_generic_action_achievement(startingid, prefix, f"{Foil.Foil.name} {expansion.name}", rar, list(Border),
                                           [Foil.Foil], 5, 10, 25, 50))
        startingid = startingid + 4
        achievements.extend(
            get_generic_action_achievement(startingid, prefix, f"{Border.Base.name} {expansion.name}", rar,
                                           [Border.Base], list(Foil), 5, 10, 25, 50))
        startingid = startingid + 4
        achievements.extend(
            get_generic_action_achievement(startingid, prefix, f"{Border.FirstEdition.name} {expansion.name}", rar,
                                           [Border.FirstEdition], list(Foil), 5, 10, 25, 50))
        startingid = startingid + 4
        achievements.extend(
            get_generic_action_achievement(startingid, prefix, f"{Border.Silver.name} {expansion.name}", rar,
                                           [Border.Silver], list(Foil), 4, 8, 20, 40))
        startingid = startingid + 4
        achievements.extend(
            get_generic_action_achievement(startingid, prefix, f"{Border.Gold.name} {expansion.name}", rar,
                                           [Border.Gold], list(Foil), 4, 8, 20, 40))
        startingid = startingid + 4
        achievements.extend(
            get_generic_action_achievement(startingid, prefix, f"{Border.EX.name} {expansion.name}", rar, [Border.EX],
                                           list(Foil), 2, 5, 10, 25))
        startingid = startingid + 4
        achievements.extend(
            get_generic_action_achievement(startingid, prefix, f"{Border.FullArt.name} {expansion.name}", rar,
                                           [Border.FullArt], list(Foil), 2, 5, 10, 25))
    elif prefix == AchievementPrefix.Open:
        startingid = startingid + 4
        achievements.extend(get_generic_action_achievement(startingid, prefix, expansion.name, rar,list(Border), list(Foil),  50, 100, 500, 1000, ))
        startingid = startingid + 4
        achievements.extend(get_generic_action_achievement(startingid, prefix, f"{Foil.Foil.name} {expansion.name}", rar, list(Border), [Foil.Foil], 20, 50, 200, 500))
        startingid = startingid + 4
        achievements.extend(get_generic_action_achievement(startingid, prefix, f"{Border.Base.name} {expansion.name}", rar,[Border.Base], list(Foil), 20, 50, 200, 500))
        startingid = startingid + 4
        achievements.extend(get_generic_action_achievement(startingid, prefix, f"{Border.FirstEdition.name} {expansion.name}", rar,[Border.FirstEdition], list(Foil), 20, 50, 200, 500))
        startingid = startingid + 4
        achievements.extend(get_generic_action_achievement(startingid, prefix, f"{Border.Silver.name} {expansion.name}", rar,[Border.Silver], list(Foil), 10, 25, 100, 250))
        startingid = startingid + 4
        achievements.extend(get_generic_action_achievement(startingid, prefix, f"{Border.Gold.name} {expansion.name}", rar,[Border.Gold], list(Foil), 10, 25, 100, 250))
        startingid = startingid + 4
        achievements.extend(get_generic_action_achievement(startingid, prefix, f"{Border.EX.name} {expansion.name}", rar,[Border.EX], list(Foil), 4, 10, 40, 100))
        startingid = startingid + 4
        achievements.extend(get_generic_action_achievement(startingid, prefix, f"{Border.FullArt.name} {expansion.name}", rar,[Border.FullArt], list(Foil), 2, 5, 20, 50))

    return achievements

def extract_threshold(name: str) -> int:
    parts = name.split(" ")
    for part in parts:
        if part.isdigit():
            return int(part)
    return 0


# --- JSON Conversion ---
def build_achievement_objects(prefix: AchievementPrefix, difficulty: int, startingid: int) -> List[AchievementEntryJSON]:
    """
    Creates all non-generic achievements for open/sell/grade actions,
    """
    achievements_json: List[AchievementEntryJSON] = []
    for expansion in Expansion:
        for rar in Rarity:
            region_achievements = get_region_action_achievements(prefix, rar, expansion, startingid)
            for ach in region_achievements:
                if ach.difficulty.value > difficulty:
                    continue
                entry: AchievementEntryJSON = {
                    "type": prefix.name,
                    "name": ach.name,
                    "difficulty": ach.difficulty.value,
                    "threshold": extract_threshold(ach.name),
                    "rarity": [rar.value],
                    "border": [b.value for b in ach.borders],
                    "expansion": [expansion.value],
                    "foil": [f.value for f in ach.foils],
                    "id": ach.id
                }
                achievements_json.append(entry)
    return achievements_json

def get_achievements_for_region(prefix: AchievementPrefix, rar: Rarity, expansion: Expansion, difficulty:int, startingid: int) -> List[AchievementEntryJSON]:
    achievements_json: List[AchievementEntryJSON] = []
    region_achievements = get_region_action_achievements(prefix, rar, expansion, startingid)
    for ach in region_achievements:
        if ach.difficulty.value > difficulty:
            continue
        entry: AchievementEntryJSON = {
            "type": prefix.name,
            "name": ach.name,
            "difficulty": ach.difficulty.value,
            "threshold": extract_threshold(ach.name),
            "rarity": [rar.value],
            "border": [b.value for b in ach.borders],
            "expansion": [expansion.value],
            "foil": [f.value for f in ach.foils],
            "id": ach.id
        }
        achievements_json.append(entry)

    return achievements_json