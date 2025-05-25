from typing import Any

from .board import Board
from .dice import DiceManager
from .loggers import InMemoryEventLogger
from .player import Player
from .turn_manager import TurnManager


class Game:
    def __init__(
        self,
        players: list[Player],
        tiles: int = 9,
        variation: Any = None,
        *,
        sim_id: int = 0,
        game_id: int = 0,
        logger: InMemoryEventLogger | None = None,
    ):
        self.players = players
        self.board = Board(max_tile_number=tiles)
        self.dice_manager = DiceManager()
        self.current_player_idx = 0
        self.state = "SETUP"
        self.variation = variation
        self.sim_id = sim_id
        self.game_id = game_id
        self.logger = logger

    def initialize(self) -> None:
        self.board.reset()
        for p in self.players:
            p.update_score(0)
        self.state = "IN_PROGRESS"

    def start_game(self) -> None:
        self.initialize()
        if self.logger:
            self.logger.log_game_start(
                self.sim_id,
                self.game_id,
                [p.name for p in self.players],
                num_dice=2,  # Assume 2 dice init
            )
        for turn_idx, player in enumerate(self.players):
            self.current_player_idx = self.players.index(player)
            # Each player plays a full turn
            tm = TurnManager(
                player,
                self.board,
                self.dice_manager,
                self.logger,
                sim_id=self.sim_id,
                game_id=self.game_id,
                turn_idx=turn_idx,
                strategy="greedy",
            )
            score, shut_box = tm.play_turn()
            player.update_score(score)
        self.state = "COMPLETED"
        # Determine winner
        winner = self.determine_winner()
        scores = {p.name: p.score for p in self.players}
        # Print winner information
        print(f"Winner: {winner.name} with score {winner.score}")
        # After all turns, log game end event
        if self.logger:
            self.logger.log_game_end(
                self.sim_id,
                self.game_id,
                winner_id=winner.name if winner else None,
                player_scores=scores,
            )

    def next_turn(self) -> None:
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def is_game_over(self) -> bool:
        return self.state == "COMPLETED"

    def determine_winner(self) -> Player:
        return min(self.players, key=lambda p: p.score)
