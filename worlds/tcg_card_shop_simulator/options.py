from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions, OptionGroup, Range, Toggle, DefaultOnToggle, DeathLink


class MaxLevel(Range):
    """
    Maximum shop level to reach.
    Rounded up to the nearest multiple of 5.

    Hosts may limit this to 60 with a Host.yaml setting.
    """

    display_name = "Max Level"
    range_start = 10
    range_end = 100
    default = 20

class LicensesPerLevelGroup(Range):
    """
    Number of licenses available every 5 levels.

    Distributed as evenly as possible across all 4 shop pages.
    """

    display_name = "Licenses Per Level Group"
    range_start = 6
    range_end = 14
    default = 6

class RequiredLicensesForProgress(Range):
    """
    Number of sellable Product Licenses within your current level to unlock the next 5 levels.

    Lower values make progression easier.
    """

    display_name = "Required licenses Per Level Group"
    range_start = 2
    range_end = 10
    default = 5


class Goal(Choice):
    """
    Main victory condition.

    Max Level: Reach the max level
    Collection Builder: Unlock all packs and collect a target amount of cards.
    Sell Ghost Cards: Find and sell ghost cards hidden in the multiworld.
    """

    display_name = "Goal"
    option_reach_max_level = 0
    option_collection_builder = 1
    option_sell_ghost_cards = 2
    default = 0

class GhostGoalAmount(Range):
    """
    Number of ghost cards required for victory.

    Ghost card items will be added to the multiworld.
    """

    display_name = "Ghost Goal Amount"
    range_start = 5
    range_end = 80
    default = 40

class CollectionGoalPercentage(Range):
    """
    Collection percentage required after unlocking all packs.

    Hosts may limit this to 60% with a Host.yaml setting.
    """

    display_name = "Collection Goal Percentage"
    range_start = 10
    range_end = 100
    default = 40

class StartWithWorker(Choice):
    """
    Start with a hired worker.

    You must still pay their daily salary.
    """
    display_name = "Starting Worker"
    option_none = 0
    option_zachery = 1
    option_terence = 2
    option_dennis = 3
    option_clark = 4
    option_angus = 5
    option_benji = 6
    option_lauren = 7
    option_axel = 8
    option_alexander = 9
    default = 0

class AutoRenovate(DefaultOnToggle):
    """
    Automatically renovate shop expansions when received. Never look at RENO BIGG again!
    """
    display_name = "Auto Renovate"

class ExtraStartingItemChecks(Range):
    """
    Adds extra early checks to prevent generation failures on limited starts.

    Checks per item are capped at 16 regardless of this setting
    """

    display_name = "Extra Starting Item Checks"
    range_start = 4
    range_end = 8
    default = 4

class SellCheckAmount(Range):
    """
    Number of sell checks per product.

    Selling an entire box counts as one check.
    """
    display_name = "Sell Check Amount"
    range_start = 2
    range_end = 16
    default = 2

class CardOpeningCheckDifficulty(Choice):
    """
    Difficulty of achievement checks for opening cards.

    There are around 10 achievements for each difficulty. Harder options include easier achievements.

    Example achievements:
    Easy: First common foil
    Medium: Open 20 gold border foils from legendary packs
    Hard: Collect all 12 versions of a card
    Impossible: Collect 100 full arts from a pack
    """
    display_name = "Card Opening Check Difficulty"
    option_disabled = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_impossible = 4
    default = 2

class CardSanity(Choice):
    """
    Individual cards become location checks.

    Enabled:
    Different card variants count as separate checks based on Card Opening difficulty.

    Unique Foils:
    Foil cards also count as separate checks.

    Each enabled card variant adds 242 checks.
    Impossible difficulty with Unique Foils adds 2904 checks.

    This is based on your choice of card opening difficulty above.

    Card variants by opening difficulty:
    Easy: Basic
    Medium: Basic, 1st Edition, Silver Edition
    Hard: Basic, 1st Edition, Silver Edition, Gold Edition
    Impossible: All Cards
    """
    display_name = "Card Sanity"
    option_disabled = 0
    option_enabled = 1
    option_uniqueFoils = 2
    default = 0

class CardSellingCheckDifficulty(Choice):
    """
    Difficulty of achievement checks for selling cards.

    There are around 10 achievements for each difficulty. Harder options include easier achievements.

    Example goals:
    Easy: Sell 20 commons
    Medium: Sell 100 foils
    Hard: Sell 1000 cards
    Impossible: Sell 50 foil full arts
    """
    display_name = "Card Selling Check Difficulty"
    option_disabled = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_impossible = 4
    default = 1

class CardGradingCheckDifficulty(Choice):
    """
    Difficulty of achievement checks for grading cards.

    There are around 10 achievements for each difficulty. Harder options include easier achievements.

    Grading checks take much longer and are better for async games.

    Example goals:
    Easy: Grade 10 commons
    Medium: Grade 50 foils
    Hard: Grade 100 cards
    Impossible: Grade 20 foil full arts
    """
    display_name = "Card Grading Check Difficulty"
    option_disabled = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_impossible = 4
    default = 0

class BulkBoxChecks(Choice):
    """
    Selling bulk boxes from the workbench can grant checks.
    """
    display_name = "Bulk Box Checks"
    option_disabled = 0
    option_normal_bulk = 1
    default = 0

class NoFormats(Toggle):
    """
    All play table formats share one combined check pool.
    """
    display_name = "No Formats"

class PlayTableChecks(Range):
    """
    Number of checks available per play table format.
    """
    display_name = "Number of PlayTable Checks"
    range_start = 0
    range_end = 15
    default = 10

class MoneyBags(Range):
    """
    Weight for filler items that give money.
    """
    display_name = "Money Filler"
    range_start = 0
    range_end = 100
    default = 50

class XpBoosts(Range):
    """
    Weight for filler items that give shop XP.
    """
    display_name = "XP Filler"
    range_start = 0
    range_end = 100
    default = 50


class RandomNewCard(Range):
    """
    Weight for filler items that give a random new card.
    """
    display_name = "Random Card Filler"
    range_start = 0
    range_end = 100
    default = 50

class CustomerWalletSize(Range):
    """
    Weight for filler items that increase customer spending money.
    """
    display_name = "Customer Wallet Size Filler"
    range_start = 0
    range_end = 100
    default = 50

class CardLuck(Range):
    """
     Weight for filler items that increase card luck.

    At max card luck (100) you have the same chance to open a non-foil basic card and a foil full art card
    """
    display_name = "Card Luck Filler"
    range_start = 0
    range_end = 100
    default = 50


class TrapFill(Range):
    """
    Percentage of junk items replaced with traps.
    """
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 80
    default = 0

class StinkTrap(Range):
    """
    You know what this does. Stinky.
    Weight for traps that are Stink Traps.

    Requires traps to be enabled.
    """
    display_name = "Stink Trap"
    range_start = 0
    range_end = 100
    default = 50

class PoltergeistTrap(Range):
    """
    Something is messing with the lights
    Weight for traps that are Poltergeist Traps.

    Requires traps to be enabled.
    """
    display_name = "Poltergeist Trap"
    range_start = 0
    range_end = 100
    default = 50

# class MarketChangeTrap(Range):
#     """
#     Not used
#     """
#     display_name = "Market Change Trap"
#     range_start = 0
#     range_end = 100
#     default = 50
# class CurrencyTrap(Range):
#     """
#     Not used
#     """
#     display_name = "Currency Trap"
#     range_start = 0
#     range_end = 100
#     default = 0

class DecreaseCardLuckTrap(Range):
    """
    Weight for traps that reduce card luck.

    Requires traps to be enabled.
    """
    display_name = "Reduce Card Luck Trap"
    range_start = 0
    range_end = 100
    default = 20

class CreditCardFailureTrap(Range):
    """
    Sometimes they only have cash.
    Weight for traps that disable credit card payments temporarily.

    Requires traps to be enabled.
    """
    display_name = "Credit Card Failure Trap"
    range_start = 0
    range_end = 100
    default = 50

@dataclass
class tcg_cardshop_simulator_option_groups(PerGameCommonOptions):
    OptionGroup("Goal Options", [
        MaxLevel,
        LicensesPerLevelGroup,
        RequiredLicensesForProgress,
        Goal,
        CollectionGoalPercentage,
        GhostGoalAmount,
    ]),
    OptionGroup("General", [
        StartWithWorker,
        AutoRenovate,
        ExtraStartingItemChecks,
        SellCheckAmount,
        BulkBoxChecks,
        PlayTableChecks,
        NoFormats,
        # DecoShop,
    ]),
    OptionGroup("Card Checks", [
        CardOpeningCheckDifficulty,
        CardSellingCheckDifficulty,
        CardGradingCheckDifficulty,
    ]),
    OptionGroup("Sanity", [
        CardSanity,
    ]),
    OptionGroup("Death Link", [
        DeathLink
    ])
    OptionGroup("Filler", [
        MoneyBags,
        XpBoosts,
        RandomNewCard,
        CustomerWalletSize,
        CardLuck
    ])
    OptionGroup("Traps", [
        TrapFill,
        StinkTrap,
        PoltergeistTrap,
        CreditCardFailureTrap,
        # MarketChangeTrap,
        # CurrencyTrap,
        DecreaseCardLuckTrap
    ])
    
@dataclass
class TCGSimulatorOptions(PerGameCommonOptions):
    max_level: MaxLevel
    licenses_per_region: LicensesPerLevelGroup
    required_licenses: RequiredLicensesForProgress
    goal: Goal
    collection_goal_percentage: CollectionGoalPercentage
    ghost_goal_amount: GhostGoalAmount
    start_with_worker: StartWithWorker
    auto_renovate: AutoRenovate
    sell_check_amount: SellCheckAmount
    bulk_box: BulkBoxChecks
    extra_starting_item_checks: ExtraStartingItemChecks
    play_table_checks: PlayTableChecks
    no_formats: NoFormats
    checks_opening_difficulty: CardOpeningCheckDifficulty
    card_sanity: CardSanity
    checks_selling_difficulty: CardSellingCheckDifficulty
    checks_grading_difficulty: CardGradingCheckDifficulty
    deathlink: DeathLink

    money_filler: MoneyBags
    xp_filler: XpBoosts
    card_filler: RandomNewCard
    wallet_filler: CustomerWalletSize
    luck_filler: CardLuck

    trap_fill: TrapFill
    stink_trap: StinkTrap
    poltergeist_trap: PoltergeistTrap
    credit_card_failure_trap: CreditCardFailureTrap
    # market_change_trap: MarketChangeTrap
    # currency_trap: CurrencyTrap
    decrease_card_luck_trap: DecreaseCardLuckTrap
