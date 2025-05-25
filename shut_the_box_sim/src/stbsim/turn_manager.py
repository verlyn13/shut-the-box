from .board import Board
from .dice import DiceManager
from .loggers import InMemoryEventLogger
from .player import Player


class TurnManager:
    """
    Handles a single player's turn: rolls, moves, and logs all events.
    """

    def __init__(
        self,
        player: Player,
        board: Board,
        dice_manager: DiceManager,
        logger: InMemoryEventLogger | None = None,
        sim_id: str | int | None = None,
        game_id: str | int | None = None,
        turn_idx: int = 0,
        strategy: str = "greedy",
    ):
        self.player = player
        self.board = board
        self.dice_manager = dice_manager
        self.logger = logger
        self.sim_id = sim_id
        self.game_id = game_id
        self.turn_idx = turn_idx
        self.strategy = strategy

    def play_turn(self) -> tuple[int, bool]:
        """Runs through a full turn for this player until bust/shut."""
        move_idx = 0
        shut_box = False
        while True:
            # Dice roll
            roll_values = self.dice_manager.roll(self.board)
            if self.logger:
                self.logger.log_dice_roll(
                    self.sim_id,
                    self.game_id,
                    self.player.name,
                    self.turn_idx,
                    roll_values,
                    [t.number for t in self.board.get_upright_tiles()],
                )
            roll_sum = sum(roll_values)
            tiles_up = [t.number for t in self.board.get_upright_tiles()]
            # Find possible combos
            combos = self.find_all_valid_combos(tiles_up, roll_sum)
            if not combos:
                if self.logger:
                    self.logger.log_move_attempt(
                        self.sim_id,
                        self.game_id,
                        self.player.name,
                        self.turn_idx,
                        move_idx,
                        self.strategy,
                        (),
                        tiles_up,
                        roll_sum,
                        False,
                    )
                break  # No valid move -> turn ends
            # Greedy pick (just for illustration, can replace)
            chosen_combo = combos[0]
            # Log move attempt
            if self.logger:
                self.logger.log_move_attempt(
                    self.sim_id,
                    self.game_id,
                    self.player.name,
                    self.turn_idx,
                    move_idx,
                    self.strategy,
                    chosen_combo,
                    tiles_up,
                    roll_sum,
                    True,
                    tiles_flipped=chosen_combo,
                    final_tiles_up=[n for n in tiles_up if n not in chosen_combo],
                )
            # Flip those tiles
            self.board.flip_tiles(list(chosen_combo))
            move_idx += 1
            # Check for shut box
            if self.board.are_all_tiles_down():
                shut_box = True
                break
        # End of turn: score and log
        turn_score = self.board.calculate_remaining_sum()
        if self.logger:
            self.logger.log_turn_end(
                self.sim_id,
                self.game_id,
                self.player.name,
                self.turn_idx,
                [t.number for t in self.board.get_upright_tiles()],
                turn_score,
                shut_box,
            )
        return turn_score, shut_box

    @staticmethod
    def find_all_valid_combos(tiles: list[int], target: int) -> list[tuple[int, ...]]:
        """
        Find all combinations of tiles that sum to the roll value.
        """
        from itertools import combinations

        result = []
        for r in range(1, len(tiles) + 1):
            for combo in combinations(tiles, r):
                if sum(combo) == target:
                    result.append(combo)
        return result
