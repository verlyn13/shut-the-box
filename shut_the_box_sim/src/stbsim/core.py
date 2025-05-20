from typing import Set, Tuple, Dict, Any


class TileRack:
    """
    Represents the set of numbered tiles still upright in Shut the Box.

    Args:
        tiles_up: The set of tile numbers currently up (available to flip).
    """

    def __init__(self, tiles_up: Set[int] | None = None):
        self.tiles_up: Set[int] = (
            set(tiles_up) if tiles_up is not None else set(range(1, 10))
        )

    def flip_tiles(self, combo: Tuple[int, ...]) -> None:
        """Flips (removes) the specified tiles if valid."""
        for tile in combo:
            self.tiles_up.remove(tile)

    def is_combo_valid(self, combo: Tuple[int, ...], roll_total: int) -> bool:
        """
        Check if combo uses only available tiles and sums to roll_total.
        """
        tile_set = set(combo)
        return tile_set <= self.tiles_up and sum(combo) == roll_total

    def score(self) -> int:
        """
        Compute the player's (bad) score: sum of all remaining up tiles.
        """
        return sum(self.tiles_up)

    def is_shut(self) -> bool:
        """Returns True if all tiles have been flipped (the box is shut)."""
        return not self.tiles_up

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes the rack state to a dictionary.
        """
        return {"tiles_up": sorted(self.tiles_up)}
