"""
Batch simulation runner for Shut the Box.

Provides Simulation class for fast batch evaluation of parametric games/strategies.
"""

import random
from typing import Any

from .game import Game
from .loggers import InMemoryEventLogger
from .player import Player


class Simulation:
    """
    Batch experiment runner for Shut the Box games.

    Example:
        sim = Simulation()
        results = sim.run(100, 'greedy_max', 'min_tiles', seed_start=42)
    """

    def __init__(self) -> None:
        pass

    def run(
        self,
        n_games: int,
        p1_strategy: str,
        p2_strategy: str,
        seed_start: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Simulate n_games between two strategies.

        Args:
            n_games (int): Number of games/batches to simulate.
            p1_strategy (str): Strategy for Player 1 (see strategies.STRATEGY_MAP).
            p2_strategy (str): Strategy for Player 2.
            seed_start (Optional[int]): Seed for reproducibility; each game seed
                increments from this value.

        Returns:
            List[Dict]: List of per-game summary stats/metadata for downstream analysis.
        """
        results = []
        for game_idx in range(n_games):
            if seed_start is not None:
                random.seed(seed_start + game_idx)
            logger = InMemoryEventLogger()
            players = [Player("P1"), Player("P2")]
            game = Game(
                players=players, tiles=9, sim_id=0, game_id=game_idx, logger=logger
            )
            game.start_game()
            winner = game.determine_winner()
            shut_box = any(p.score == 0 for p in players)
            results.append(
                {
                    "game_id": game_idx,
                    "winner": winner.name if winner else None,
                    "p1_score": players[0].score,
                    "p2_score": players[1].score,
                    "shut_box": shut_box,
                }
            )
        return results
