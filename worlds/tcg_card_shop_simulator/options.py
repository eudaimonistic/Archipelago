from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions,OptionGroup, DeathLink,Range, Toggle, DefaultOnToggle

class MaxLevel(Range):
    """
    What is the maximum level you would like to reach?
    This will be rounded up to the nearest multiple of 5

    The host can limit this setting to 50 for syncs
    """

    display_name = "Max Level"
    range_start = 10
    range_end = 100
    default = 20

class LicensesPerLevelGroup(Range):
    """
    Every 5 levels, across all 4 shop pages, how many licenses will be available?
    these are spread evenly as possible across all 4 shops
    """

    display_name = "Licenses Per Level Group"
    range_start = 6
    range_end = 14
    default = 6

class RequiredLicensesForProgress(Range):
    """
    How many More Product Licenses are required to unlock the next 5 levels? low numbers are easier.

    Every 5 levels, you will stop leveling up until you have found this many more sellable licenses unlocked
    """

    display_name = "Required licenses Per Level Group"
    range_start = 2
    range_end = 10
    default = 5


class Goal(Choice):
    """
    The victory condition for your run.
    Collection Builder is about getting access to all card packs and collecting a percentage of cards. Minimum Max Level of 20.
    Sell Ghost Cards hides ghost cards in locations to be found
    """

    display_name = "Goal"
    option_reach_max_level = 0
    option_collection_builder = 1
    option_sell_ghost_cards = 2
    default = 0

class GhostGoalAmount(Range):
    """
    If on Ghost cards Goal, How many do you need to sell?
    This causes ghost card items to be seeded in the multiworld
    """

    display_name = "Ghost Goal Amount"
    range_start = 1
    range_end = 80
    default = 40

class CollectionGoalPercentage(Range):
    """
    If on Collection Goal, What percentage of the collection do you need to collect after you get all the packs?
    the host can limit this setting to 50%
    """

    display_name = "Collection Goal Percentage"
    range_start = 10
    range_end = 100
    default = 40

class StartWithWorker(Choice):
    """
    Choose a worker to start with.
    Reminder, you still have to pay their salary every day
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
    default = 0

class AutoRenovate(DefaultOnToggle):
    """
    This automatically renovates shop expansions for you when you receive expansions. Never look at RENO BIGG again!
    """
    display_name = "Auto Renovate"

class ExtraStartingItemChecks(Range):
    """
    This setting stops generation failures from very limited starts.
    The maximum checks per item are capped to 16 regardless of this setting
    """

    display_name = "Extra Starting Item Checks"
    range_start = 4
    range_end = 8
    default = 4

class SellCheckAmount(Range):
    """
    Selling all of a Box of an ordered product is a check. How many sell checks will each product have?

    The host can limit this to 8
    """
    display_name = "Sell Check Amount"
    range_start = 2
    range_end = 16
    default = 2

class CardOpeningCheckDifficulty(Choice):
    """
    Open Cards to complete goals for checks. How hard do you want these goals to be?

    examples of checks:
        "First common foil card" is an easy check.
        "open 20 gold border foils from legendary packs" is medium
        "Collect all 12 versions of one card" is hard
        "Collect all full arts from a pack" is impossible
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
    Enables each card to be a unique check.
    Normally foils will count the same as the non-foil card. "Unique foils" will cause the foil version to be a unique check


    This follows your card opening difficulty set above. Below is what happens depending on that option.
    Each version adds 242 checks

    Card Opening "Easy": Basic cards are checks
    Card Opening "Medium": Basic, 1st Edition, and Silver Edition cards are checks
    Card Opening "Hard": basic, 1st Edition, Silver Edition, gold edition are checks
    Card Opening "Impossible": All cards are checks

    At Card Opening Difficulty "Impossible" this adds 1452 checks. doubled to 2904 if on foil setting
    """
    display_name = "Card Sanity"
    option_disabled = 0
    option_enabled = 1
    option_uniqueFoils = 2
    default = 0

class CardSellingCheckDifficulty(Choice):
    """
    Sell Cards to complete goals for checks. How hard do you want these goals to be?

    examples of checks:
        "Sell 20 commons" is an easy check.
        "Sell 100 foils" is medium
        "sell 1000 cards" is hard
        "sell 50 foil full arts" is impossible
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
    Grade Cards to complete goals for checks. How hard do you want these goals to be?

    WARNING THESE TAKE A LONG TIME TO DO. WAYYYYYY BETTER FOR ASYNCS

    examples of checks:
        "Grade 20 commons" is an easy check.
        "Grade 100 foils" is medium
        "Grade 1000 cards" is hard
        "Grade 50 foil full arts" is impossible
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
    Will Selling bulk boxed made in the workbench be checks?

    currently any other o
    """
    display_name = "Bulk Box Checks"
    option_disabled = 0
    option_normal_bulk = 1
    default = 0

class NoFormats(Toggle):
    """
    Have any format count towards a single play table check pool
    """
    display_name = "No Formats"

class PlayTableChecks(Range):
    """
    How many checks are there for each format on play tables?
    """
    display_name = "Number of PlayTable Checks"
    range_start = 0
    range_end = 15
    default = 10

# class DecoShop(Toggle):
#     """
#     Turns the Deco Screen into a shop you can buy AP items in
#     """
#     display_name = "Decoration Shop"


class TrapFill(Range):
    """
    Determines the percentage of the junk fill which is filled with traps.
    """
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 80
    default = 0

class StinkTrap(Range):
    """
    You know what this does. Stinky.
    Determines the percentage of Traps are Stink Traps.
    Traps must be enabled for this to have any effect.
    """
    display_name = "Stink Trap"
    range_start = 0
    range_end = 100
    default = 50

class PoltergeistTrap(Range):
    """
    Something is messing with the lights
    Determines the percentage of Traps are Poltergeist Traps.
    Traps must be enabled for this to have any effect.
    """
    display_name = "Poltergeist Trap"
    range_start = 0
    range_end = 100
    default = 50

class MarketChangeTrap(Range):
    """
    Causes prices to randomize
    Determines the percentage of Traps are Market Change Traps.
    Traps must be enabled for this to have any effect.
    """
    display_name = "Market Change Trap"
    range_start = 0
    range_end = 100
    default = 50
class CurrencyTrap(Range):
    """
    Causes Currency to Randomize
    Determines the percentage of Traps are Currency Traps.
    Traps must be enabled for this to have any effect.
    """
    display_name = "Currency Trap"
    range_start = 0
    range_end = 100
    default = 0

class DecreaseCardLuckTrap(Range):
    """
    Lowers your card luck
    Determines the percentage of Traps are Decrease Card Luck Traps.
    Traps must be enabled for this to have any effect.
    """
    display_name = "Reduce Card Luck Trap"
    range_start = 0
    range_end = 100
    default = 20

class CreditCardFailureTrap(Range):
    """
    Credit cards fail to work for a little while
    Determines the percentage of Traps are Credit Card Failure Traps.
    Traps must be enabled for this to have any effect.
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
    OptionGroup("Filler and Traps", [
        TrapFill,
        StinkTrap,
        PoltergeistTrap,
        CreditCardFailureTrap,
        MarketChangeTrap,
        CurrencyTrap,
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
    extra_starting_item_checks: ExtraStartingItemChecks
    sell_check_amount: SellCheckAmount
    checks_opening_difficulty: CardOpeningCheckDifficulty
    checks_selling_difficulty: CardSellingCheckDifficulty
    checks_grading_difficulty: CardGradingCheckDifficulty
    play_table_checks: PlayTableChecks
    no_formats: NoFormats
    bulk_box: BulkBoxChecks
    # deco_shop: DecoShop
    deathlink: DeathLink
    card_sanity: CardSanity
    trap_fill: TrapFill
    stink_trap: StinkTrap
    poltergeist_trap: PoltergeistTrap
    credit_card_failure_trap: CreditCardFailureTrap
    market_change_trap: MarketChangeTrap
    currency_trap: CurrencyTrap
    decrease_card_luck_trap: DecreaseCardLuckTrap
