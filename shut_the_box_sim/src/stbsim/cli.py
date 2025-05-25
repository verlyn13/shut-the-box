"""
stbsim CLI for Shut the Box batch simulations.

Entrypoint: python -m stbsim.cli --help or uv run python -m stbsim.cli --n-games ...
Allows bulk parameterized games, stats, and reproducibility.
"""

import typer
from tqdm import tqdm

from stbsim.simulation import Simulation
from stbsim.stats import calculate_summary_stats
from stbsim.strategies import STRATEGY_MAP

app = typer.Typer()


@app.command()
def run(
    n_games: int = typer.Option(..., "--n-games", help="Number of games to simulate."),
    p1_strategy: str = typer.Option(
        "greedy_max",
        "--p1-strategy",
        help=f"Player 1 strategy. Options: {list(STRATEGY_MAP.keys())}",
    ),
    p2_strategy: str = typer.Option(
        "min_tiles",
        "--p2-strategy",
        help=f"Player 2 strategy. Options: {list(STRATEGY_MAP.keys())}",
    ),
    seed: int | None = typer.Option(None, "--seed", help="Random seed (optional)."),
    output_file: str | None = typer.Option(
        None,
        "--output-file",
        help="Output detailed log to CSV/Parquet (not implemented).",
    ),
) -> None:
    """
    Run and summarize bulk Shut the Box simulations.

    Args:
        n_games: Number of games to simulate
        p1_strategy: Strategy for Player 1 ('greedy_max', 'min_tiles', ...)
        p2_strategy: Strategy for Player 2
        seed: Optional random seed for reproducibility
        output_file: If specified, save detailed logs to CSV/Parquet (future)

    Example:
        uv run python -m stbsim.cli --n-games 100 \\
            --p1-strategy greedy_max --p2-strategy min_tiles --seed 42
    """
    if p1_strategy not in STRATEGY_MAP:
        typer.echo(
            f"Unknown p1-strategy: {p1_strategy}. "
            f"Available: {list(STRATEGY_MAP.keys())}"
        )
        raise typer.Exit(1)
    if p2_strategy not in STRATEGY_MAP:
        typer.echo(
            f"Unknown p2-strategy: {p2_strategy}. "
            f"Available: {list(STRATEGY_MAP.keys())}"
        )
        raise typer.Exit(1)

    typer.echo(f"Simulating {n_games} games: P1({p1_strategy}) vs P2({p2_strategy})")
    if seed is not None:
        typer.echo(f"Using random seed: {seed}")

    sim = Simulation()
    summaries = []
    for _ in tqdm(range(n_games), desc="Simulating"):
        # For now, Simulation.run expects to be told n_games at once; let's just run once
        # ...so single Simulation.run call outside tqdm is preferable for batching:
        pass

    # Actually use single Simulation.run call for batch efficiency
    summaries = sim.run(n_games, p1_strategy, p2_strategy, seed_start=seed)

    stats = calculate_summary_stats(summaries)
    typer.echo("==== Summary Stats ====")
    for k, v in stats.items():
        typer.echo(f"{k}: {v}")

    if output_file:
        typer.echo("[NOTE] Log output to file is not yet implemented.")
        # See: logger/events upgrade in Game/TurnManager for detailed event exports.


if __name__ == "__main__":
    app()
