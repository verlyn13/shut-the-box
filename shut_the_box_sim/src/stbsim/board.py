class Tile:
    """One numbered tile, which can be upright (up) or flipped (down)."""

    def __init__(self, number: int):
        self.number = number
        self.is_upright = True

    def flip(self) -> None:
        self.is_upright = False

    def reset(self) -> None:
        self.is_upright = True

    def __repr__(self) -> str:
        return f"Tile({self.number}, up={self.is_upright})"


class Board:
    """Holds all tiles for a single Shut the Box game."""

    def __init__(self, max_tile_number: int = 9):
        self.tiles: list[Tile] = [Tile(n) for n in range(1, max_tile_number + 1)]

    def reset(self) -> None:
        for t in self.tiles:
            t.reset()

    def get_upright_tiles(self) -> list[Tile]:
        """Return a list of currently-up (unflipped) tiles."""
        return [t for t in self.tiles if t.is_upright]

    def are_all_tiles_down(self) -> bool:
        """True if all tiles have been flipped (shut)."""
        return all(not t.is_upright for t in self.tiles)

    def calculate_remaining_sum(self) -> int:
        """Sum of all upright (unflipped) tile numbers."""
        return sum(t.number for t in self.get_upright_tiles())

    def flip_tiles(self, numbers: list[int]) -> None:
        """Flips specified tiles by number, if currently upright (does not check validity here)."""
        tile_dict = {tile.number: tile for tile in self.tiles}
        for num in numbers:
            if tile_dict[num].is_upright:
                tile_dict[num].flip()
