import random

from .board import Board


class Die:
    def __init__(self, faces: int = 6):
        self.faces = faces
        self.current_value: int = 0

    def roll(self) -> int:
        self.current_value = random.randint(1, self.faces)
        return self.current_value


class DiceManager:
    """
    Handles 1 or 2 dice according to Shut the Box rules.
    Automatically decides 1 or 2 dice when rolling, based on board state.
    """

    def __init__(self, die_faces: int = 6):
        self.dice: list[Die] = [Die(die_faces) for _ in range(2)]
        self.num_dice = 2  # Start with two dice

    def set_number_of_dice(self, count: int) -> None:
        self.num_dice = count

    def roll(self, board: Board | None = None) -> list[int]:
        """Rolls either 1 or 2 dice based on board state (if board is provided)."""
        if board is not None:
            # 1 die is allowed only if 7,8,9 are all down.
            upright = [t.number for t in board.get_upright_tiles()]
            if all(num not in upright for num in [7, 8, 9]):
                self.num_dice = 1
            else:
                self.num_dice = 2
        rolled = [self.dice[i].roll() for i in range(self.num_dice)]
        return rolled

    def get_sum(self) -> int:
        return sum(die.current_value or 0 for die in self.dice[: self.num_dice])
