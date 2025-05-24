"""
Strategies for Shut the Box

Provides pluggable callable strategy functions (greedy_max_strategy, min_tiles_strategy)
that select tile combos to flip for a given dice roll and board state.

Each strategy accepts (roll_total: int, tiles_up: set[int]) and returns a tuple of tile numbers to flip,
or () if no valid move is possible.
Exported for use in CLI, simulation, or interactive analyses.
"""

from itertools import combinations


def greedy_max_strategy(roll_total: int, tiles_up: set[int]) -> tuple[int, ...]:
    """
    Greedy strategy: Select the largest valid single-tile or largest-sum combo move for given dice roll.

    Args:
        roll_total: Dice roll total for this move
        tiles_up: Set of tile numbers available to flip

    Returns:
        tuple: The tile numbers to flip, or () if no valid move
    """
    tiles_up = set(tiles_up)
    if not tiles_up:
        return ()
    if max(tiles_up) == roll_total:
        return (max(tiles_up),)
    combos = [
        combo
        for r in range(1, len(tiles_up) + 1)
        for combo in combinations(tiles_up, r)
        if sum(combo) == roll_total
    ]
    if not combos:
        return ()
    # Sort: biggest tile, biggest sum, then fewest tiles
    combos.sort(key=lambda c: (-max(c), -sum(c), len(c)))
    return combos[0]


def min_tiles_strategy(roll_total: int, tiles_up: set[int]) -> tuple[int, ...]:
    """
    Min-Tiles strategy: Select valid combo with the fewest tiles.
    Tie-breaks by smallest sum, then lowest tile value.

    Args:
        roll_total: Dice roll total for this move
        tiles_up: Set of tile numbers available to flip

    Returns:
        tuple: The tile numbers to flip, or () if no valid move
    """
    tiles_up = set(tiles_up)
    combos = [
        combo
        for r in range(1, len(tiles_up) + 1)
        for combo in combinations(tiles_up, r)
        if sum(combo) == roll_total
    ]
    if not combos:
        return ()
    combos.sort(key=lambda c: (len(c), sum(c), min(c)))
    return combos[0]


# For CLI/factory
STRATEGY_MAP = {
    "greedy_max": greedy_max_strategy,
    "min_tiles": min_tiles_strategy,
}


def select_combo(strategy: str, roll_total: int, tiles_up: set[int]) -> tuple[int, ...]:
    """
    Helper to select and run a strategy by name.
    Raises ValueError for unknown strategy.
    """
    if strategy not in STRATEGY_MAP:
        raise ValueError(f"Unknown strategy: {strategy}")
    return STRATEGY_MAP[strategy](roll_total, tiles_up)
