from stbsim import Game, Player
from stbsim.loggers import InMemoryEventLogger


def test_game_event_logging_schema_and_content():
    logger = InMemoryEventLogger()
    players = [Player("A"), Player("B")]
    g = Game(players, sim_id=11, game_id=42, logger=logger)
    g.start_game()
    df = logger.to_df()
    # There should be at least: 1 game_start + 2 turn_ends + 1 game_end
    event_types = set(df["event_type"])
    # Check for required event types
    assert "game_start" in event_types
    assert "game_end" in event_types
    assert "turn_end" in event_types
    # Each event should have timestamp, sim_id, game_id
    for _idx, row in df.iterrows():
        assert row["sim_id"] == 11
        assert row["game_id"] == 42
        assert "timestamp" in row and row["timestamp"]
        assert "event_type" in row and isinstance(row["event_type"], str)
    # Sanity check: at least 2 turn_end events (one per player)
    turn_end_count = (df["event_type"] == "turn_end").sum()
    assert turn_end_count == 2
