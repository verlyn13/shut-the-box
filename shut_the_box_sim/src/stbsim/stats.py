"""
Statistic aggregators for Shut the Box batch simulation.

Provides functions to summarize, tabulate, and analyze game result batches for reporting or CLI.
"""

from typing import Any


def calculate_summary_stats(game_results: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Compute win rates, mean scores, shut-box frequency from a set of simulation summaries.

    Args:
        game_results: List of per-game data dicts (see simulation.py)

    Returns:
        Dict with keys: p1_win_rate, p2_win_rate, p1_avg_score, p2_avg_score, shut_box_frequency, total_games
    """
    if not game_results:
        return {}
    total = len(game_results)
    p1_wins = sum(1 for g in game_results if g.get("winner") == "P1")
    p2_wins = sum(1 for g in game_results if g.get("winner") == "P2")
    p1_scores = [g.get("p1_score", 0) for g in game_results]
    p2_scores = [g.get("p2_score", 0) for g in game_results]
    shut_count = sum(1 for g in game_results if g.get("shut_box"))
    return {
        "p1_win_rate": p1_wins / total,
        "p2_win_rate": p2_wins / total,
        "p1_avg_score": sum(p1_scores) / total,
        "p2_avg_score": sum(p2_scores) / total,
        "shut_box_frequency": shut_count / total,
        "total_games": total,
    }
